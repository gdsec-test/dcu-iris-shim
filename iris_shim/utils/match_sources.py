import logging
import re

from tld import get_tld

from iris_shim import blacklist


class MatchSources:
    domain_names = re.compile(r'(?i)\b[a-z0-9\-\.]+\.[a-z]{2,63}', re.IGNORECASE | re.MULTILINE)
    ip_regex = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
    url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE | re.MULTILINE)

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
        to pull out any URLs.
        :param text:
        :return: list of URLs
        """
        if not text:
            self._logger.debug('No email body (Text) was passed to get_urls')
            return []

        return re.findall(self.url, self._text_cleanup(text))

    def is_valid_domain(self, domain_list):
        """
        Checks to see if a domain name in the domain name list is a valid TLD
        :param domain_list:
        :return: the domain list with any invalid domain names removed
        """
        valid_domains = []
        if not domain_list:
            return valid_domains

        for domain_name in domain_list:
            if get_tld(domain_name, fail_silently=True, fix_protocol=True):
                valid_domains.append(domain_name)
        return valid_domains

    def separate_blacklisted_domains(self, domain_list):
        """
        Iterates through provided domain names list and pulls out any blacklisted domain names into their own list
        :param domain_list:
        :return: domain list with blacklisted domains removed, and list containing the blacklisted domains.
        """
        found_blacklist = []
        if not domain_list:
            return [], found_blacklist
        for domain in domain_list:
            if domain and domain.lower() in blacklist.domains:
                found_blacklist.append(domain)
                domain_list.remove(domain)

        return domain_list, found_blacklist

    def _text_cleanup(self, text):
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
        self._logger.debug('After replace: %s', text)
        return new_text
