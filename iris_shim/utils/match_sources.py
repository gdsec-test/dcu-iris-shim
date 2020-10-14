import logging
import re

from iris_shim import blacklist
from tld import get_fld, get_tld


class MatchSources:
    domain_names = re.compile(r'\b[a-z0-9\-\.]+\.[a-z]{2,63}\b', re.IGNORECASE | re.MULTILINE)
    ip_regex = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
    url = re.compile(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', re.IGNORECASE | re.MULTILINE)
    email_id_regex = re.compile(r'\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,63}\b', re.IGNORECASE | re.MULTILINE)
    url_filter_pattern = re.compile(r"(" + '|'.join(blacklist.url_filters) + r")", re.IGNORECASE | re.MULTILINE)
    subdomain_filter_pattern = re.compile(r"(" + '|'.join(blacklist.subdomain_filters) + r")", re.IGNORECASE | re.MULTILINE)

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_domains(self, text):
        """
        Takes in IRIS email text and replaces any obfuscation etc. with preferred characters, and then regex is used
        to pull out any domain names.
        :param text:
        :return: List of valid domain names
        """
        if not text:
            self._logger.debug('No email body (Text) was passed to get_domains')
            return []
        found_domains = re.findall(self.domain_names, self._text_cleanup(text))
        return self.is_valid_domain(found_domains)

    def get_ip(self, text):
        """
        Takes in IRIS email text and then regex is used to pull out any ip addresses
        :param text:
        :return: list of IP addresses
        """
        if not text:
            self._logger.debug('No email body (Text) was passed to get_ip')
            return []

        return re.findall(self.ip_regex, text.replace('DNS: ', ''))

    def get_urls(self, text):
        """
        Takes in IRIS email text and replaces any obfuscation etc. with preferred characters, and then regex is used
        to pull out any URLs with duplicates removed when converting to set.
        :param text:
        :return: set of URLs
        """
        if not text:
            self._logger.debug('No email body (Text) was passed to get_urls')
            return set()

        return set(re.findall(self.url, self._text_cleanup(text, 'redacted@redacted.tld')))

    def is_valid_domain(self, domain_list):
        """
        Checks to see if a domain name in the domain name list is a valid TLD
        :param domain_list:
        :return: the domain list with any invalid domain names removed
        """
        valid_domains = set()
        if not domain_list:
            return valid_domains

        for domain_name in domain_list:
            if get_tld(domain_name, fail_silently=True, fix_protocol=True):
                valid_domains.add(domain_name.lower())
        return valid_domains

    def separate_blacklisted_domains(self, domain_list):
        """
        Iterates through provided domain names list and pulls out any blacklisted domain names into their own set
        :param domain_list:
        :return: set of valid domains with blacklisted domains removed, and set containing the blacklisted domains.
        """
        domains_valid, domains_blacklist = set(), set()

        if not domain_list:
            return domains_valid, domains_blacklist

        for domain in domain_list:
            parent_domain = self.get_parent_domain(domain)
            if parent_domain and parent_domain.lower() in blacklist.domains:
                domains_blacklist.add(domain)
            else:
                domains_valid.add(domain)

        return domains_valid, domains_blacklist

    def remove_urls_via_regex(self, url_list):
        """
        Iterates through provided URLs and removes any URL matching entries in blacklist url_filters
        :param url_list:
        :return: a set of URLs minus any filter matches
        """
        urls_valid = set()

        if not url_list:
            return urls_valid

        for domain in url_list:
            if not re.findall(self.url_filter_pattern, domain):
                urls_valid.add(domain)

        return urls_valid

    def remove_domains_via_regex(self, domain_list):
        """
        Iterates through provided domain names and removes any domain matching entries in blacklist subdomain_filters
        :param domain_list: a list of all domains from the email
        :return: a set of domains minus any filter matches
        """
        domains_valid = set()

        if not domain_list:
            return domains_valid

        for domain in domain_list:
            if not re.findall(self.subdomain_filter_pattern, domain):
                domains_valid.add(domain)

        return domains_valid

    def get_parent_domain(self, domain):
        """
        Extracts the parent domain from a domain having subdomains.
        :param domain:
        :return: parent domain
        """
        return get_fld(domain, fail_silently=True, fix_protocol=True)

    def _text_cleanup(self, text, replacement_string=''):
        """
        Replaces obfuscated code from email body into text that regex can more easily go through
        :param text:
        :return: cleaned up email text body
        """
        self._logger.debug('Before replace: %s', text)
        new_text = text.replace('&#xA;', '\n'). \
            replace('&nbsp;', '\n'). \
            replace(',', '%2c'). \
            replace('[dot]', '.'). \
            replace('hxxp', 'http'). \
            replace('[.]', '.'). \
            replace('(.)', '.'). \
            replace('hXXp', 'http'). \
            replace('URL: www', 'http://www')
        new_text = re.sub(self.email_id_regex, replacement_string, new_text)
        self._logger.debug('After replace: %s', new_text)
        return new_text
