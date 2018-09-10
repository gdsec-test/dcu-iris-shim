import re
import logging
from tld import get_tld

class MatchDomain:
    DOMAIN_NAMES = re.compile(r'(?i)\b[a-z0-9\-\.]+\.[a-z]{2,63}', re.IGNORECASE | re.MULTILINE)

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def is_valid_domain(self, domain_name):
        if not domain_name:
            return False
        if not get_tld(domain_name, fail_silently=True, fix_protocol=True):
            self._logger.debug('Domain : {} is not a valid domain'.format(domain_name))
            return False
        return True

    def get_domains(self, text):
        if not text:
            return
        self._logger.debug('Before replace: %s', text)
        text = text.replace('&#xA;', '\n').\
            replace('&nbsp;', '\n').\
            replace(',', '%2c').\
            replace('[dot]', '.').\
            replace('hxxp', 'http').\
            replace('[.]', '.').\
            replace('(.)', '.').\
            replace('hXXp', 'http').\
            replace('URL: www', 'http://www')
        self._logger.debug('After replace: %s', text)
        return list(set(re.findall(self.DOMAIN_NAMES, text)))
