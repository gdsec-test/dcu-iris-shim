import abc

from iris_shim.models import Reporter


class ReportManager(object):
    """
    Abstract base class for Report Managers for different Abuse types
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, datastore, api):
        self._datastore = datastore
        self._api = api

    def _action_reports(self, reporters):
        """
        Take the appropriate action for all incidents that we've parsed or failed to parse.
        First check which single type of email we should send the reporter for all the reports they've submitted this batch.
        After, iterate over all invalid Iris incidents and notate and close them, next the reportable sources and submit
        them to the Abuse API for processing.
        :param reporters: a mapping of unique reporter emails and their associated Reporter object
        """

    @abc.abstractmethod
    def process(self, iris_incidents):
        """
        Process the IRIS Incidents
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

        :param iris_incidents:
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
        """
        Perform basic validation on this report before attempting to parse the report itself.
        This should filter out reports that are submitted by spammers, known bad subjects, etc.
        :param report:
        :return:
        """
        data = self._datastore.get_report_info_by_id(report.report_id)
        email_subject = data.Subject.strip() if data.Subject else ''

        return report.validate(email_subject)
