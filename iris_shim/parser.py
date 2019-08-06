from utils.match_sources import MatchSources

from .blacklist import domains as blacklist


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
        urls_blacklist, urls_valid, domains_in_urls = set(), set(), set()

        for url in urls:
            parent_domains = set()
            domains = map(lambda x: x.lower(), self.match_sources.get_domains(url))

            if domains:
                domains_in_urls.update(set(domains))

            for domain in domains:
                parent_domains.add(self.match_sources.get_parent_domain(domain))
            urls_blacklist.add(url) if parent_domains & blacklist else urls_valid.add(url)

        domains = self.match_sources.get_domains(email_body)
        domains_valid, domains_blacklist = self.match_sources.separate_blacklisted_domains(domains)
        reportable_domains = self._remove_reporter_domain(domains_valid, reporter_email)
        reportable_domains.difference_update(domains_in_urls)
        return urls_valid, reportable_domains, domains_blacklist.union(urls_blacklist)

    def parse_netabuse(self, email_body):
        """
        Calls all actions to parse valid sources from IRIS Network Abuse tickets.
        :param email_body: IRIS email body
        :return:
        """
        return set(self.match_sources.get_ip(email_body))

    def _remove_reporter_domain(self, domain_list, reporter_email):
        """
        Check to see if a parsed domain matches the reporters email domain
        :param domain_list: List of domains
        :param reporter_email: Reporters email address
        :return: domain set with matching domains removed
        """
        if not isinstance(reporter_email, basestring) or '@' not in reporter_email:
            return domain_list
        return {domain for domain in domain_list if domain != reporter_email.split('@')[1]}
