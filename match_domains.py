import re
import logging


class MatchDomain:
    DOMAIN_NAMES = re.compile(r'(?i)\b[a-z0-9\-\.]+\.[a-z]{2,63}', re.IGNORECASE | re.MULTILINE)

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_domains(self, text):
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
        post_replace = re.findall(self.DOMAIN_NAMES, text)
        return post_replace
