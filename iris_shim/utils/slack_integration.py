import json
import logging
import os

import requests


class SlackIntegration:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._url = os.getenv('SLACK_HANDLER')

    def send_message(self, message):
        """
        Sends a message that contains the IRIS IID for a failed parse to the slack api
        This message will appear in the child-safety channel.
        Param: Message - String
        Return: None
        """
        data = {
            'text': message,
            'username': 'iris',
        }
        response = requests.post(self._url, data=json.dumps(data))
        if response.status_code != 200:
            self._logger.error('sending message to slack channel failed: {}'.format(response.status_code))
        else:
            self._logger.info('message sent to slack')
