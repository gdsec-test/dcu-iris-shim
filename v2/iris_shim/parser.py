from utils.match_sources import MatchSources


class Parser:

    match_sources = MatchSources()

    def parse_phish_malware(self, email_body, reporter_email):
        """
        Calls all actions to parse valid sources from IRIS Phishing tickets.
        :param email_body: IRIS email body
        :param reporter_email: IRIS reporting email address
        :return:
        """
        urls = self.match_sources.get_urls(email_body)
        domains, blacklist = self.match_sources.get_domains(email_body)
        reportable_domains = self.remove_reporter_domain(domains, reporter_email)
        return set(urls), set(reportable_domains), set(blacklist)

    def parse_netabuse(self, email_body):
        """
        Calls all actions to parse valid sources from IRIS Network Abuse tickets.
        :param email_body: IRIS email body
        :return:
        """
        return set(self.match_sources.get_ip(email_body))

    def remove_reporter_domain(self, domain_list, reporter_email):
        """
        Check to see if a parsed domain matches the reporters email domain
        :param domain_list: List of domains
        :param reporter_email: Reporters email address
        :return: domain list with matching domains removed
        """
        email_domain = reporter_email.split('@')[1]
        return [domain for domain in domain_list if domain != email_domain]
