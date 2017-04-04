import requests
import logging


class APITicket:

    URL = {
        'dev': 'http://abuse.api.int.dev-godaddy.com/v1/abuse/tickets',
        'ote': 'http://abuse.api.int.ote-godaddy.com/v1/abuse/tickets '
    }

    # Constructor expects to receive an environment string variable of 'dev' or 'ote'
    def __init__(self, environment):
        if environment not in ('dev', 'ote'):
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
            }
            return requests.post(self._url, json=payload, headers=headers)
        except Exception as e:
            print 'Error posting ticket for {}: {}', format(dict_of_values.get('url'), e.message)

