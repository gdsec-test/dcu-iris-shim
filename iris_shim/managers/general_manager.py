import logging
from collections import defaultdict

from iris_shim.managers.interface import ReportManager


class GeneralManager(ReportManager):
    """A Report Manager to handle the transmission of Phishing, Malware, & Netabuse IRIS tickets into the Abuse API"""

    def __init__(self, datastore, mailer, api):
        """
        :param datastore: The backend datastore to retrieve information about reports e.g. Iris
        :param mailer: The mailer that we should use to send feedback emails to reporters e.g. OCM
        :param api: The API that we should submit abuse ticket creation requests to.
        """
        super(GeneralManager, self).__init__(datastore, api)

        self._logger = logging.getLogger(__name__)
        self._mailer = mailer

    def process(self, iris_incidents):
        super(GeneralManager, self).process(iris_incidents)

    def _action_reports(self, reporters):
        """
        Take the appropriate action for all incidents that we've parsed or failed to parse.
        First check which single type of email we should send the reporter for all the reports they've submitted this batch.
        After, iterate over all invalid Iris incidents and notate and close them, next the reportable sources and submit
        them to the Abuse API for processing.
        :param reporters: a mapping of unique reporter emails and their associated Reporter object
        """
        report_summary = {}

        for email, reporter in reporters.items():
            # Check if any reports associated with a reporter was parseable and send the corresponding notice
            if not self._send_customer_interaction(reporter):
                self._logger.error('Unable to send customer interaction for {}'.format(email))

            # Notate and close all invalid iris report(s)
            for iris_report in reporter.reports_invalid:
                self._datastore.notate_report_and_close(iris_report.report_id, self._datastore.note_failed_to_parse)

            # Submit all reportable sources to the Abuse API and close the corresponding iris report(s)
            tickets_for_reporter = defaultdict(dict)
            for iris_report in reporter.reports_reportable:
                success, fail = self._create_abuse_report(iris_report)
                tickets_for_reporter[iris_report.report_id]['success'] = success
                tickets_for_reporter[iris_report.report_id]['fail'] = fail

                self._datastore.notate_report_and_close(iris_report.report_id, self._datastore.note_successfully_parsed)

            for iris_report in reporter.reports_valid:
                self._datastore.notate_report_and_close(iris_report.report_id, self._datastore.note_successfully_parsed)

            self._logger.info('Reporter Summary for {}: {}'.format(email, tickets_for_reporter))
            report_summary[email] = tickets_for_reporter
        return report_summary

    def _send_customer_interaction(self, reporter):
        """
        Send the appropriate reporter interaction based on whether or not we were able to parse any sources.
        :param reporter:
        :return:
        """
        if reporter.successfully_parsed():
            return self._mailer.report_successfully_parsed(reporter.email)
        return self._mailer.report_failed_to_parse(reporter.email)
