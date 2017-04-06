import requests
import logging


class APITicket:

    URL = {
        'dev': 'http://api.dev-godaddy.com/v1/abuse/tickets',
        'ote': 'https://api.ote-godaddy.com/v1/abuse/tickets',
        'prod': 'https://api.godaddy.com/v1/abuse/tickets'
    }

    # Constructor expects to receive an environment string variable of 'dev' or 'ote'
    def __init__(self, environment):
        self._logger = logging.getLogger(__name__)
        if environment not in ('dev', 'ote', 'prod'):
            environment = 'dev'
        self._url = self.URL.get(environment)

    # This method expects dict_of_values to be a dictionary, with the minimal key set as follows:
    #  - jwt (SSO JWT)
    #  - type (Abuse type being submitted.  ie: PHISHING, SPAM, MALWARE)
    #  - url (The URL of the abuse)
    def post_ticket(self, dict_of_values):
        try:
            headers = {'Authorization': dict_of_values.get('jwt')}
            payload = {
                "type": dict_of_values.get('type'),
                "source": dict_of_values.get('url'),
                "metadata": {
                    'iris_id': dict_of_values.get('iid'),
                    'iris_reporter': dict_of_values.get('email'),
                    'iris_created': dict_of_values.get('create_date').strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            return requests.post(self._url, json=payload, headers=headers)
        except Exception as e:
            self._logger.error('Error posting ticket for {}: {}'.format(dict_of_values.get('url'), e.message))
