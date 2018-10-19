import logging


class CustomerEmail:

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def send_report_parsed_successfully(self, reporter_email):
        # TODO implement functionality for communicating to Hermes to send report parse successfully emails
        pass

    def send_unable_to_parse_report(self, reporter_email):
        # TODO implement functionality for communicating to Hermes to send unable to parse report emails
        pass
