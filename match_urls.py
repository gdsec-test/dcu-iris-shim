import re
import logging

class MatchURL:
    URL = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE | re.MULTILINE)

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_urls(self, text):
        if not text:
            self._logger.debug('None passed to get_urls')
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
        post_replace = re.findall(self.URL, text)
        return post_replace
