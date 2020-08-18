import logging
from collections import defaultdict

from iris_shim.managers.interface import ReportManager

from ..utils.slack_integration import SlackIntegration


class CSAMReportManager(ReportManager):
    """A Report Manager to handle the transmission of CSAM specific IRIS tickets into the Abuse API"""

    def __init__(self, datastore, api):
        """
        :param datastore: The backend datastore to retrieve information about reports e.g. Iris
        :param api: The API that we should submit abuse ticket creation requests to.
        """
        super(CSAMReportManager, self).__init__(datastore, api)

        self._logger = logging.getLogger(__name__)

    def process(self, iris_incidents):
        super(CSAMReportManager, self).process(iris_incidents)

    def _action_reports(self, reporters):
        """
        Take the appropriate action for all CSAM incidents that we've parsed or failed to parse.
        Iterate over all invalid Iris incidents and notate and leave them open, next the reportable sources and submit
        them to the Abuse API for processing.
        :param reporters: a mapping of unique reporter emails and their associated Reporter object
        :return: A defaultdict(list) with 2 possible keys that contain a list of IRIS ID's
        """
        report_summary = defaultdict(list)
        si = SlackIntegration()
        for email, reporter in reporters.items():
            # Notate, but leave open invalid iris report(s)
            for iris_report in reporter.reports_invalid:
                self._datastore.notate_report(iris_report.report_id, self._datastore.note_csam_failed_to_parse)
                report_summary['needs_investigator_review'].append(iris_report.report_id)

            # Submit all reportable sources to the Abuse API. Leave IRIS ID open if a report fails; otherwise, close it.
            for iris_report in reporter.reports_reportable:
                success, fail = self._create_abuse_report(iris_report)
                if fail:
                    si.send_message("Failed to parse iris ticket: {}".format(iris_report.report_id))
                    self._datastore.notate_report(iris_report.report_id,
                                                  self._datastore.note_csam_failed_to_submit_to_api)

                    report_summary['needs_investigator_review'].append(iris_report.report_id)
                else:
                    self._datastore.notate_report_and_close(iris_report.report_id,
                                                            self._datastore.note_successfully_parsed)
                    report_summary['successfully_submitted_to_api'].append(iris_report.report_id)

        self._logger.info('CSAM Report Summary - {}'.format(report_summary))
        return report_summary
