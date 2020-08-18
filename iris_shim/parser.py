from .blacklist import domains as blacklist
from .utils.match_sources import MatchSources


class Parser:

    match_sources = MatchSources()

    def parse_phish_malware(self, email_body, reporter_email):
        """
        Calls all actions to parse valid sources from IRIS Phishing tickets.
        :param email_body: IRIS email body
        :param reporter_email: IRIS reporting email address
        :return:
        """
        if reporter_email:
            reporter_email = reporter_email.lower()

        urls = self.match_sources.get_urls(email_body)
        # Remove any URLs that match regex
        urls = self.match_sources.remove_urls_via_regex(urls)
        urls_blacklist, urls_valid, domains_in_urls = set(), set(), set()

        for url in urls:
            domains = [x.lower() for x in self.match_sources.get_domains(url)]

            if domains:
                domains_in_urls.update(set(domains))

            parent_domains = set()
            for domain in domains:
                parent_domains.add(self.match_sources.get_parent_domain(domain))
            urls_blacklist.add(url) if parent_domains & blacklist else urls_valid.add(url)

        domains = self.match_sources.get_domains(email_body)
        # Remove any domains that match regex
        domains = self.match_sources.remove_domains_via_regex(domains)
        domains_valid, domains_blacklist = self.match_sources.separate_blacklisted_domains(domains)
        reportable_domains = Parser._remove_reporter_domain(domains_valid, reporter_email)
        reportable_domains.difference_update(domains_in_urls)
        return urls_valid, reportable_domains, domains_blacklist.union(urls_blacklist)

    def parse_netabuse(self, email_body):
        """
        Calls all actions to parse valid sources from IRIS Network Abuse tickets.
        :param email_body: IRIS email body
        :return:
        """
        return set(self.match_sources.get_ip(email_body))

    @staticmethod
    def _remove_reporter_domain(domain_list, reporter_email):
        """
        Check to see if a parsed domain ends with the reporters email domain, which covers sub-domains
        :param domain_list: List of domains
        :param reporter_email: Reporters email address
        :return: domain set with matching domains removed
        """
        if not isinstance(reporter_email, str) or '@' not in reporter_email:
            return domain_list
        reporter_email_domain = reporter_email.split('@')[1]
        return {domain for domain in domain_list if not domain.endswith(reporter_email_domain)}
