import logging
from collections import defaultdict

from iris_shim.models import Reporter


class ReportManager:
    def __init__(self, datastore, mailer, api):
        """
        :param datastore: The backend datastore to retrieve information about reports e.g. Iris
        :param mailer: The mailer that we should use to send feedback emails to reporters e.g. OCM
        :param api: The API that we should submit abuse ticket creation requests to.
        """
        self._logger = logging.getLogger(__name__)

        self._datastore = datastore
        self._mailer = mailer
        self._api = api

    def process(self, iris_incidents):
        reporters = self._gather_reports(iris_incidents)
        return self._action_reports(reporters)

    def _gather_reports(self, iris_incidents):
        """
        Iterate over all Iris incidents and validate basic data about each report. Afterward, attempt to parse the email
        body and extract sources. An unsuccessful parse will mark an iris incident as invalid. A successful parse will
        result in a combination of valid, reportable, and blacklisted sources.

        Blacklisted sources are sources which we wish to never create Abuse Reports for.
        Valid sources are sources which meet the criteria for a valid Domain/URL/etc but have already been seen in another report.
        Reportable sources are valid sources that have not been seen before in other reports.
        :return:
        """
        reporters = {}  # {<reporter_email>: Reporter}
        sources_seen = set()  # {<source1>, <source2>, ...,}

        for report in iris_incidents:
            if report.reporter_email not in reporters:
                reporters[report.reporter_email] = Reporter(report.reporter_email)

            if not self._validate_report(report):
                reporters[report.reporter_email].add_incident(report)
                continue

            email_body = self._datastore.get_customer_notes(report.report_id)
            report.parse(email_body)

            # Update report's sources_reportable to contain all sources we haven't seen and update the master list.
            report.sources_reportable = report.sources_valid.difference(sources_seen)
            sources_seen.update(report.sources_reportable)

            reporters[report.reporter_email].add_incident(report)
        return reporters

    def _action_reports(self, reporters):
        """
        Take the appropriate action for all incidents that we've parsed or failed to parse.
        First check which single type of email we should send the reporter for all the reports they've submitted this batch.
        After, iterate over all invalid Iris incidents and notate and close them, next the reportable sources and submit
        them to the Abuse API for processing.
        :param reporters: a mapping of unique reporter emails and their associated Reporter object
        """
        report_summary = {}

        for email, reporter in reporters.iteritems():
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

    def _create_abuse_report(self, iris_report):
        """
        Attempts to create an abuse report for all reportable sources contained within an Iris Report.
        :param iris_report:
        :return: tuple containing success and failure e.g. ((<source>, <DCU Ticket>), ...), (<source>, ...)
        """
        success, fail = [], []

        for source in iris_report.sources_reportable:
            ticket = self._api.create_ticket(iris_report.type, source, iris_report.report_id,
                                             iris_report.reporter_email, iris_report.modify_date)
            success.append((source, ticket)) if ticket else fail.append(source)

        return success, fail

    def _send_customer_interaction(self, reporter):
        """
        Send the appropriate reporter interaction based on whether or not we were able to parse any sources.
        :param reporter:
        :return:
        """
        if reporter.successfully_parsed():
            return self._mailer.report_successfully_parsed(reporter.email)
        return self._mailer.report_failed_to_parse(reporter.email)

    def _validate_report(self, report):
        data = self._datastore.get_report_info_by_id(report.report_id)
        email_subject = data.Subject.strip() if data.Subject else ''

        return report.validate(email_subject)


class CSAMReportManager:
    """A Report Manager to handle the transmission of CSAM specific IRIS tickets into the Abuse API"""
    def __init__(self, datastore, api):
        """
        :param datastore: The backend datastore to retrieve information about reports e.g. Iris
        :param api: The API that we should submit abuse ticket creation requests to.
        """
        self._logger = logging.getLogger(__name__)

        self._datastore = datastore
        self._api = api

    def process(self, iris_incidents):
        """
        Gather all CSAM IRIS Reports, parse for domains/URLS and submit them to the API
        :param iris_incidents:
        :return:
        """
        reporters = self._gather_reports(iris_incidents)
        return self._action_reports(reporters)

    def _gather_reports(self, iris_incidents):
        """
        Iterate over all Iris incidents and validate basic data about each report. Afterward, attempt to parse the email
        body and extract sources. An unsuccessful parse will mark an iris incident as invalid. A successful parse will
        result in a combination of valid, reportable, and blacklisted sources.

        Blacklisted sources are sources which we wish to never create Abuse Reports for.
        Valid sources are sources which meet the criteria for a valid Domain/URL/etc but have already been seen in another report.
        Reportable sources are valid sources that have not been seen before in other reports.
        :return:
        """
        reporters = {}  # {<reporter_email>: Reporter}
        sources_seen = set()  # {<source1>, <source2>, ...,}

        for report in iris_incidents:
            if report.reporter_email not in reporters:
                reporters[report.reporter_email] = Reporter(report.reporter_email)

            if not self._validate_report(report):
                reporters[report.reporter_email].add_incident(report)
                continue

            email_body = self._datastore.get_customer_notes(report.report_id)
            report.parse(email_body)

            # Update report's sources_reportable to contain all sources we haven't seen and update the master list.
            report.sources_reportable = report.sources_valid.difference(sources_seen)
            sources_seen.update(report.sources_reportable)

            reporters[report.reporter_email].add_incident(report)
        return reporters

    def _action_reports(self, reporters):
        """
        Take the appropriate action for all CSAM incidents that we've parsed or failed to parse.
        Iterate over all invalid Iris incidents and notate and leave them open, next the reportable sources and submit
        them to the Abuse API for processing.
        :param reporters: a mapping of unique reporter emails and their associated Reporter object
        :return: A defaultdict(list) with 2 possible keys that contain a list of IRIS ID's
        """
        report_summary = defaultdict(list)

        for email, reporter in reporters.iteritems():
            # Notate, but leave open invalid iris report(s)
            for iris_report in reporter.reports_invalid:
                self._datastore.notate_report(iris_report.report_id, self._datastore.note_csam_failed_to_parse)
                report_summary['needs_investigator_review'].append(iris_report.report_id)

            # Submit all reportable sources to the Abuse API. Leave IRIS ID open if a report fails; otherwise, close it.
            for iris_report in reporter.reports_reportable:
                success, fail = self._create_abuse_report(iris_report)
                if len(fail) > 0:
                    self._datastore.notate_report(iris_report.report_id,
                                                  self._datastore.note_csam_failed_to_submit_to_api)
                    report_summary['needs_investigator_review'].append(iris_report.report_id)
                else:
                    self._datastore.notate_report_and_close(iris_report.report_id,
                                                            self._datastore.note_csam_successfully_parsed)
                    report_summary['successfully_submitted_to_api'].append(iris_report.report_id)

        self._logger.info('CSAM Report Summary - {}'.format(report_summary))
        return report_summary

    def _create_abuse_report(self, iris_report):
        """
        Attempts to create an abuse report for all reportable sources contained within an Iris Report.
        :param iris_report:
        :return: tuple containing success and failure e.g. ((<source>, <DCU Ticket>), ...), (<source>, ...)
        """
        success, fail = [], []

        for source in iris_report.sources_reportable:
            ticket = self._api.create_ticket(iris_report.type, source, iris_report.report_id,
                                             iris_report.reporter_email, iris_report.modify_date)
            success.append((source, ticket)) if ticket else fail.append(source)

        return success, fail

    def _validate_report(self, report):
        data = self._datastore.get_report_info_by_id(report.report_id)
        email_subject = data.Subject.strip() if data.Subject else ''

        return report.validate(email_subject)
