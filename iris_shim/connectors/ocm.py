import logging

from hermes.messenger import send_mail


class Mailer:
    """
    Mailer is responsible for sending feedback to reporters regarding their abuse reports they've submitted to Iris.
    It provides the ability to send various feedback such as:
        1) we were able to parse their report
        2) we were unable to parse their report
    """

    hermes_failed_to_parse = 'iris_shim.failed_to_parse_report'
    hermes_successfully_parsed = 'iris_shim.report_successfully_parsed'

    def __init__(self, env, cert, key, test_email=None):
        self._logger = logging.getLogger(__name__)
        self._env = env
        self._cert = cert
        self._key = key

        self._recipients = [{'email': test_email}] if env != 'prod' else []

    def _generate_kwargs_for_hermes(self):
        """
        Generates additional information needed by Hermes in order to send emails through OCM.
        Currently this includes the environment in which we'd like to send the email, as well as our credentials
        for authenticating with OCM (a certificate and key associated with phishstory).

        This purposefully creates a new dictionary every time as different templates may manipulate this dictionary
        in various ways. This ensures provides a consistent and isolated baseline utilized by all templates.
        :return:
        """
        return {'env': self._env, 'cert': self._cert, 'key': self._key}

    def report_successfully_parsed(self, reporter_email):
        """
        Given a reporter email, send a notice that notifies the reporter that we were able to successfully parse
        their report and we will be actioning their claims as soon as possible.
        :param reporter_email:
        :return:
        """
        if not reporter_email:
            return False

        kwargs = self._generate_kwargs_for_hermes()
        kwargs['recipients'] = self._recipients or [{'email': reporter_email}]

        try:
            resp = send_mail(self.hermes_successfully_parsed, [], **kwargs)  # pass an empty list for substitutionValues
            self._logger.info('Sent "report successfully parsed" email to reporter {}: {}'.format(reporter_email, resp))
        except Exception as e:
            self._logger.error('Unable to send "report successfully parsed" email to reporter {}: {}'.format(reporter_email, e.message))
            return False
        return True

    def report_failed_to_parse(self, reporter_email):
        """
        Given a reporter email, send a notice that notifies the reporter that we were unable to successfully parse
        their report and we require more information to action their claims.
        :param reporter_email:
        :return:
        """
        if not reporter_email:
            return False

        kwargs = self._generate_kwargs_for_hermes()
        kwargs['recipients'] = self._recipients or [{'email': reporter_email}]

        try:
            resp = send_mail(self.hermes_failed_to_parse, [], **kwargs)  # pass an empty list for substitutionValues
            self._logger.info('Sent "failed to parse" email to reporter {}: {}'.format(reporter_email, resp))
        except Exception as e:
            self._logger.error('Unable to send "failed to parse" email to reporter {}: {}'.format(reporter_email, e.message))
            return False
        return True
