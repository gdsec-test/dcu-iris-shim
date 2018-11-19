import abc
import os

from iris_shim.connectors.abuse import PhishstoryAPI
from iris_shim.connectors.iris import IrisDB, IrisSoap
from iris_shim.connectors.ocm import Mailer
from iris_shim.manager import ReportManager


class Handler(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, app_settings):
        self._iris_soap = IrisSoap(app_settings.IRIS_WSDL)
        self._iris_db = IrisDB(app_settings.IRIS_SERVER, app_settings.IRIS_PORT, app_settings.IRIS_DATABASE,
                               app_settings.IRIS_USERNAME, app_settings.IRIS_PASSWORD)

    @abc.abstractmethod
    def run(self):
        pass


class Phishing(Handler):
    def __init__(self, app_settings):
        super(Phishing, self).__init__(app_settings)
        self._api = PhishstoryAPI(app_settings.ABUSE_API_URL, app_settings.API_KEY, app_settings.API_SECRET)
        self._mailer = Mailer(os.getenv('sysenv', 'dev'), app_settings.OCM_CERT, app_settings.OCM_KEY, app_settings.NON_PROD_EMAIL)

    def run(self):
        """
        Retrieves all Phishing reports from Iris. Performs a variety of checks to determine if this report is valid
        including looking for URLs, Domains, etc. Depending on validation steps we may not create an Abuse Report
        and in turn will send feedback to the Customer that we were unable to process their request.
        Ultimately, all valid reports will be submitted to the Abuse API with the corresponding Iris metadata.
        """
        iris_reports = self._iris_db.get_phishing_reports()
        manager = ReportManager(self._iris_soap, self._mailer, self._api)
        manager.process(iris_reports)


class NetworkAbuse(Handler):
    def __init__(self, app_settings):
        super(NetworkAbuse, self).__init__(app_settings)
        self._api = PhishstoryAPI(app_settings.ABUSE_API_URL, app_settings.API_KEY, app_settings.API_SECRET)
        self._mailer = Mailer(os.getenv('sysenv', 'dev'), app_settings.OCM_CERT, app_settings.OCM_KEY, app_settings.NON_PROD_EMAIL)

    def run(self):
        """
        Retrieves all Network Abuse incidents from Iris. Performs a variety of checks to determine if this report is valid
        including looking for URLs, Domains, IPs, etc. Depending on validation steps we may not create an Abuse Report
        and in turn will send feedback to the Customer that we were unable to process their request.
        Ultimately, all valid reports will be submitted to the Abuse API with the corresponding Iris metadata.
        """
        iris_reports = self._iris_db.get_network_abuse_reports()
        manager = ReportManager(self._iris_soap, self._mailer, self._api)
        manager.process(iris_reports)


class Malware(Handler):
    def __init__(self, app_settings):
        super(Malware, self).__init__(app_settings)
        self._api = PhishstoryAPI(app_settings.ABUSE_API_URL, app_settings.API_KEY, app_settings.API_SECRET)
        self._mailer = Mailer(os.getenv('sysenv', 'dev'), app_settings.OCM_CERT, app_settings.OCM_KEY, app_settings.NON_PROD_EMAIL)

    def run(self):
        """
        Retrieves all Malware incidents from Iris. Performs a variety of checks to determine if this report is valid
        including looking for URLs, Domains, etc. Depending on validation steps we may not create an Abuse Report
        and in turn will send feedback to the Customer that we were unable to process their request.
        Ultimately, all valid reports will be submitted to the Abuse API with the corresponding Iris metadata.
        """
        iris_reports = self._iris_db.get_malware_reports()
        manager = ReportManager(self._iris_soap, self._mailer, self._api)
        manager.process(iris_reports)


class CSAM(Handler):
    def __init__(self, app_settings):
        super(CSAM, self).__init__(app_settings)
        self._api = PhishstoryAPI(app_settings.ABUSE_API_URL, app_settings.API_KEY, app_settings.API_SECRET)

    def run(self):
        """
        Retrieves all CSAM incidents from Iris. Performs a variety of checks to determine if this report is valid
        including looking for URLs, Domains, etc. Depending on validation steps we may not create an Abuse Report
        and in turn will send feedback to the Customer that we were unable to process their request.
        Ultimately, all valid reports will be submitted to the Abuse API with the corresponding Iris metadata.
        """
        iris_reports = self._iris_db.get_child_abuse_reports()
        raise Exception('unimplemented')
