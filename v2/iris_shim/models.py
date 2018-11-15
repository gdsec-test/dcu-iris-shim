import logging
from parser import Parser

import blacklist


class Report:

    def __init__(self, report_id, report_type, reporter_email, modify_date):
        self._logger = logging.getLogger(__name__)
        self.report_id = report_id
        self.type = report_type
        self.reporter_email = reporter_email
        self.modify_date = modify_date

        self.sources_valid = set()  # Valid sources found in this incident
        self.sources_reportable = set()  # A subset of sources_valid that are actually reportable
        self.sources_blacklist = set()  # Any blacklisted sources found in this incident

        self.valid = True  # Assume an incident is valid until otherwise determined
        self.invalid_reason = None

    def __str__(self):
        return 'Report {} for reporter {}'.format(self.report_id, self.reporter_email)

    def __repr__(self):
        return 'Report({!r}, {!r}, {!r}, {!r})'.format(self.report_id, self.type, self.reporter_email, self.modify_date)

    def validate(self, email_subject):
        """
        Perform basic validation on this report before attempting to parse the report itself.
        This should filter out reports that are submitted by spammers, known bad subjects, etc.
        """
        if self.reporter_email in blacklist.emails or email_subject in blacklist.subjects:
            self.valid, self.invalid_reason = False, 'blacklist'
        return self.valid

    def parse(self, email_body):
        """
        Extract Domains, URLs, etc.
        Determine if any of these URLs are 'blacklisted' and add them to sources_blacklist
        This may include any sources that aren't necessarily 'blacklisted' but we don't want to submit reports for e.g. godaddy.com
        Any other valid sources should be added to sources_valid
        Domains that have the same domain as in reporter_email should be added to sources_blacklist
        This will likely use an external library that is extracted out of the ALF project
        :param email_body:
        :return:
        """
        parser = Parser()
        if self.type in ['PHISHING', 'MALWARE']:
            urls, domains, black_list = parser.parse_phish_malware(email_body, self.reporter_email)
            self.sources_valid.update(urls)
            self.sources_valid.update(domains)
            self.sources_blacklist.update(black_list)

        elif self.type == 'NETWORK_ABUSE':
            self.sources_valid.update(parser.parse_netabuse(email_body))

        else:
            self._logger.error("IRIS ID: {}. {} is an unsupported abuse type".format(self.report_id, self.type))


class Reporter:
    def __init__(self, reporter_email):
        self.email = reporter_email
        self.reports_valid = []
        self.reports_invalid = []
        self.reports_reportable = []

    def __str__(self):
        return 'Reporter {}, reports reportable: {}, reports invalid: {}'.format(self.email, self.reports_reportable,
                                                                                 self.reports_invalid)

    def __repr__(self):
        return 'Reporter({!r})'.format(self.email)

    def __eq__(self, other):
        return (self.email == other.email and
                self.reports_valid == other.reports_valid and
                self.reports_invalid == other.reports_invalid and
                self.reports_reportable == other.reports_reportable)

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
