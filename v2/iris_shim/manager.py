from v2.iris_shim.connectors.iris import IrisSoap
from v2.iris_shim.models import Reporter


class ReportManager:
    def __init__(self, iris_wsdl):
        self.iris_soap = IrisSoap(iris_wsdl)

    def process(self, iris_incidents):
        reporters = self._validate_reports(iris_incidents)
        self._action_reports(reporters)

    def _validate_reports(self, iris_incidents):
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
        sources_seen = {}  # {<source1>, <source2>, ...,}

        for report in iris_incidents:
            if report.reporter_email not in reporters:
                reporters[report.reporter_email] = Reporter(report.reporter_email)

            data = self.iris_soap.get_report_info_by_id(report.incident_id)
            email_subject = data.Subject.strip() if data.Subject else ''
            if not report.validate(email_subject):
                reporters[report.reporter_email].add_incident(report)
                continue

            email_body = self.iris_soap.get_customer_notes(report.incident_id)
            report.parse(email_body)

            # Store all sources that we haven't seen yet in reportable_urls
            report.sources_reportable = report.sources_seen.difference_update(sources_seen)
            sources_seen.update(report.sources_reportable)  # Update the set to store any newly seen sources

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
        for reporter_email, reporter in reporters.iteritems():
            # First check for which type of email we should sent for all reports parsed for this reporter
            if reporter.successfully_parsed():
                # Send one email for n Iris incidents
                pass
            else:
                # Send one email for n Iris incidents that we were unable to parse
                pass

            # Next iterate all of the invalid and successfully parsed domains
            for iris_report in reporter.reports_invalid:
                # notate and close Iris incident
                pass

            for iris_report in reporter.reports_reportable:
                for source in iris_report.sources_reportable:
                    # Submit to the Abuse API
                    # notate and close Iris incident
                    pass
                pass
