import os
import requests
import logging
import traceback
from pprint import pformat


class EmailReporter(object):
    """
    Builds and sends email to the hosting provider.
    @initparam message_type string message template to use
    @initparam namespace string typically the group to which the
    template belongs
    """

    NON_PROD_EMAIL_RECIPIENT = 'dcueng@godaddy.com'
    DEFAULT_ENV = "dev"

    def __init__(self, logger):
        self._logger = logger
        certificate_file_path = os.environ.get('shim_messaging_cert', None)
        private_key_file_path = os.environ.get('shim_messaging_key', None)
        if certificate_file_path is None or private_key_file_path is None:
            self._logger.fatal('Cannot determine certificates location')
            return
        self.cert = (certificate_file_path, private_key_file_path)
        self.headers = {"X-Private-Label-Id": "1"}
        self.params = {"templateNamespaceKey": "Hosting", "templateTypeKey": "AbuseHostToReporterFP"}
        self.messaging_endpoint = 'https://messaging.api.int.dev-godaddy.com/v1/messaging/messages/sendNonShopper'
        if os.environ.get('sysenv', self.DEFAULT_ENV) == 'prod':
            self.messaging_endpoint = 'https://messaging.api.int.godaddy.com/v1/messaging/messages/sendNonShopper'

    def route_mail(self, params):
        # Determines which template to send
        # :param params: The parameters provided:  email and incident
        # :return: None

        error_message = ""
        if "email" not in params:
            error_message = "/Email address not provided"
        if "incident" not in params:
            error_message += "/Incident number not provided"
        if len(error_message) > 0:
            self._logger.fatal(error_message)
            return

        # The EmailTeam does not have a way for us to test in the OTE environment
        #  per Crystal O'Brien
        if os.environ.get('sysenv', self.DEFAULT_ENV) == 'ote':
            self._logger.fatal('Unable to test template emails for OTE: {}')
            return

        # Only send to actual recipients when in the prod system env
        if os.environ.get('sysenv', self.DEFAULT_ENV) != 'prod':
            self.params['recipients'] = [{"email": self.NON_PROD_EMAIL_RECIPIENT}]

        # Only send to email address in IRIS if we are in the prod env
        if os.environ.get('sysenv', self.DEFAULT_ENV) == 'prod':
            self.params['recipients'] = [{"email": params.get('email')}]

        # Set the incident number in substitutionValues
        self.params['substitutionValues'] = {"INCIDENTID": params.get('incident')}

        # Seeing the params that were passed in as a printed dictionary will be helpful
        self._logger.info('route_mail() Params provided: {}'.format(pformat(self.params)))

        # Sends email to address associated with IRIS ticket, notifying we have received their feedback
        # Uses Template #3128
        # :return: None
        #
        # The payload sent will resemble the following:
        # {
        #     "recipients": [{"email": "some@email.com"}],
        #     "substitutionValues": {
        #         "INCIDENTID": "##INCIDENTID##"
        #     },
        #     "templateNamespaceKey": "Hosting",
        #     "templateTypeKey": "AbuseHostToReporterFP",
        # }
        try:
            # send "We received your feedback" email to reporting entity
            response = requests.post(self.messaging_endpoint, headers=self.headers, json=self.params, cert=self.cert)
            self._logger.info(response.text)
        except Exception as e:
            self._logger.fatal('Fatal Exception: {}\n{}'.format(e.message, traceback.format_exc()))
