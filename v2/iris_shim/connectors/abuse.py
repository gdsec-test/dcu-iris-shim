import logging

import requests


class AbuseAPI:
    headers = {'Authorization': None}

    def __init__(self, abuse_api_url):
        self._logger = logging.getLogger(__name__)
        self._url = abuse_api_url

    def post(self, type, source, report_id, reporter_email, create_date):
        if not self.headers.get('Authorization'):
            self.headers['Authorization'] = self._get_jwt()

        payload = {'type': type,
                   'source': source,
                   'metadata': {
                       'iris_id': report_id,
                       'iris_reporter': reporter_email,
                       'iris_created': create_date.strftime('%Y-%m-%d %H:%M:%S')}}

        try:
            response = requests.post(self._url, json=payload, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            self._logger.error('Error posting ticket for {} {}'.format(source, e.message))

    def _get_jwt(self):
        """
        :return:
        """
        # TODO implement mechanism to programmatically retrieve JWT for Abuse API
        pass
