import blacklist


class Report:

    def __init__(self, report_id, report_type, reporter_email, modify_date):
        self.report_id = report_id
        self.type = report_type
        self.reporter_email = reporter_email
        self.modify_date = modify_date

        self.sources_valid = {}  # Valid sources found in this incident
        self.sources_reportable = {}  # A subset of sources_valid that are actually reportable
        self.sources_blacklist = {}  # Any blacklisted sources found in this incident

        self.valid = True  # Assume an incident is valid until otherwise determined
        self.invalid_reason = None

    def validate(self, email_subject):
        """
        Perform basic validation on this report before attempting to parse the report itself.
        This should filter out reports that are submitted by spammers, known bad subjects, etc.
        """
        if self.reporter_email in blacklist.reporters or email_subject in blacklist.subjects:
            self.valid, self.invalid_reason = False, 'blacklist'
        return self.valid

    def parse(self, email_body):
        '''
        Extract Domains, URLs, etc.
        Determine if any of these URLs are 'blacklisted' and add them to sources_blacklist
        This may include any sources that aren't necessarily 'blacklisted' but we don't want to submit reports for e.g. godaddy.com
        Any other valid sources should be added to sources_valid
        Domains that have the same domain as in reporter_email should be added to sources_blacklist
        This will likely use an external library that is extracted out of the ALF project
        :param email_body:
        :return:
        '''
        pass


class Reporter:
    def __init__(self, reporter_email):
        self.email = reporter_email
        self.reports_valid = []
        self.reports_invalid = []
        self.reports_reportable = []

    def add_incident(self, iris_report):
        """
        Mutually exclusively add incidents to one of three lists.
        :param iris_report:
        :return:
        """
        if not iris_report.valid:
            self.reports_invalid.append(iris_report)
        elif iris_report.sources_reportable:
            self.reports_reportable.append(iris_report)
        else:  # Combine sources_valid and sources_blacklist as a successful parse but not reportable
            self.reports_valid.append(iris_report)

    def successfully_parsed(self):
        return self.reports_valid or self.reports_reportable
