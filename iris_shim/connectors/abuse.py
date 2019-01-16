import abc
import logging

import requests


class AbuseAPI(object):
    __metaclass__ = abc.ABCMeta

    def create_ticket(self, type, source, report_id, reporter_email, create_date):
        pass


class PhishstoryAPI(AbuseAPI):

    def __init__(self, abuse_api_url, sso_key, sso_secret):
        self._logger = logging.getLogger(__name__)
        self._url = abuse_api_url
        self._headers = {'Content-Type': 'application/json', 'Authorization': 'sso-key ' + sso_key + ':' + sso_secret}

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
            payload = {'type': type,
                       'source': source,
                       'metadata': {
                           'iris_id': report_id,
                           'iris_reporter': reporter_email,
                           'iris_created': create_date.strftime('%Y-%m-%d %H:%M:%S')}}

            response = requests.post(self._url, json=payload, headers=self._headers)
            response.raise_for_status()

            response_body = response.json()
            return response_body.get('u_number') if response_body else None
        except Exception as e:
            if type is 'CHILD_ABUSE':
                self._logger.error('Error posting ticket for CSAM IRIS ID: {} - {}'.format(report_id, e.message))
            else:
                self._logger.error('Error posting ticket for {} {}'.format(source, e.message))
            return None
