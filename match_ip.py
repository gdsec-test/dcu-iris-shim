import logging
import re


class MatchIP:
    REGEX = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_ip(self, text):
        return re.findall(self.REGEX, text.replace('DNS: ', ''))
