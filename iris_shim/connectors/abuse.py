import abc
import logging
from json import loads

import requests


class AbuseAPI(object, metaclass=abc.ABCMeta):
    def create_ticket(self, type, source, report_id, reporter_email, create_date):
        pass


class PhishstoryAPI(AbuseAPI):

    def __init__(self, abuse_api_url: str, sso_url: str, sso_user: str, sso_password: str, reporter: str):
        self._logger = logging.getLogger(__name__)
        self._url = abuse_api_url
        self._sso_endpoint = f'{sso_url}/v1/api/token'
        self._user = sso_user
        self._password = sso_password
        self._reporter = reporter
        self._headers = {'Content-Type': 'application/json', 'Authorization': self._get_jwt()}

    def create_ticket(self, type, source, report_id, reporter_email, create_date):
        """
        Connects to API and attempted to create an API ticket from parsed IRIS ticket data
        :param type: abuse type determined from IRIS ticket
        :param source:  abuse url parsed from IRIS ticket
        :param report_id: Iris incident number
        :param reporter_email: reporter email address from iris ticket
        :param create_date: iris ticket create date
        :return: returns ticket id on success or empty dict on failure to create ticket
        """
        try:
            payload = {
                'type': type,
                'source': source,
                'metadata': {
                    'iris_id': report_id,
                    'iris_reporter': reporter_email,
                    'iris_created': create_date.strftime('%Y-%m-%d %H:%M:%S')
                },
                'reporter': f'{self._reporter}'
            }

            response = requests.post(self._url, json=payload, headers=self._headers)
            response.raise_for_status()

            response_body = response.json()
            return response_body.get('u_number') if response_body else None
        except Exception as e:
            if type == 'CHILD_ABUSE':
                self._logger.error('Error posting ticket for CSAM IRIS ID: {} - {}'.format(report_id, e))
            else:
                self._logger.error('Error posting ticket for {} {}'.format(source, e))
            return None

    def _get_jwt(self):
        """
        Pull down JWT via username/password.
        """
        try:
            response = requests.post(
                self._sso_endpoint,
                json={'username': self._user, 'password': self._password},
                params={'realm': 'idp'}
            )
            response.raise_for_status()
            body = loads(response.text)
            return body.get('data')
        except Exception as e:
            self._logger.error(e)
        return None
