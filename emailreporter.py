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
        self._parse = {'templateNamespaceKey': "Hosting", "templateTypeKey": "AbuseHostToReporterFP"}
        self._no_parse = {"templateNamespaceKey": "Iris", "templateTypeKey": "ReportAbuse", 'substitutionValues': {}}
        self.messaging_endpoint = 'https://messaging.api.int.dev-godaddy.com/v1/messaging/messages/sendNonShopper'
        if os.environ.get('sysenv', self.DEFAULT_ENV) == 'prod':
            self.messaging_endpoint = 'https://messaging.api.int.godaddy.com/v1/messaging/messages/sendNonShopper'

    def route_mail(self, params, nothing_parsed=False):
        '''
        # Determines which template to send
        :param params: The parameters provided:  email and incident
        :param nothing_parsed: Set to true if not URLs/IPs were able to be parsed from IRIS email
        :return: None
        '''
        template_dict = {}
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

        # Only send to email address in IRIS if we are in the prod env
        if os.environ.get('sysenv', self.DEFAULT_ENV) == 'prod':
            email_dict = {'recipients': [{"email": params.get('email')}]}
        else:
            email_dict = {'recipients': [{"email": self.NON_PROD_EMAIL_RECIPIENT}]}

        # Set the incident number in substitutionValues
        self._parse['substitutionValues'] = {'INCIDENTID': params.get('incident')}

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
            if nothing_parsed:
                template_dict = dict(self._no_parse, **email_dict)
            else:
                template_dict = dict(self._parse, **email_dict)
            # Seeing the params that were passed in as a printed dictionary will be helpful
            self._logger.info('route_mail() Params provided: {}'.format(pformat(template_dict)))

            response = requests.post(self.messaging_endpoint, headers=self.headers, json=template_dict, cert=self.cert)
            self._logger.info(response.text)
        except Exception as e:
            self._logger.fatal('Fatal Exception: {}\n{}'.format(e.message, traceback.format_exc()))
