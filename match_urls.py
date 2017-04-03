import re
import logging


class MatchURL:
    URL = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE | re.MULTILINE)

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_urls(self, text):
        return re.findall(self.URL, text.replace('&#xA;', '\n').
                          replace('&nbsp;', '\n').
                          replace(',', '%2c').
                          replace('[dot]', '.').
                          replace('hxxp', 'http').
                          replace('[.]', '.').
                          replace('(.)', '.'))
