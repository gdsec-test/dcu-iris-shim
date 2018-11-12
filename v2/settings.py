import os


class AppConfig(object):
    IRIS_WSDL = None
    IRIS_SERVER = None

    IRIS_PORT = 1433
    IRIS_DATABASE = 'iris'

    IRIS_SERVICE_ID_PHISHING = None
    IRIS_SERVICE_ID_MALWARE = None
    IRIS_SERVICE_ID_NETWORK_ABUSE = None
    IRIS_GROUP_ID_CSA = None

    def __init__(self):
        self.IRIS_USERNAME = os.getenv('IRIS_USERNAME')
        self.IRIS_PASSWORD = os.getenv('IRIS_PASSWORD')

        self.API_KEY = os.getenv('API_KEY')
        self.API_SECRET = os.getenv('API_SECRET')

        self.OCM_CERT = os.getenv('OCM_CERT')
        self.OCM_KEY = os.getenv('OCM_KEY')


class ProductionAppConfig(AppConfig):
    IRIS_WSDL = "https://iris-ws.int.godaddy.com/iriswebservice.asmx?WSDL"
    IRIS_SERVER = '10.32.146.30'

    IRIS_SERVICE_ID_PHISHING = 226
    IRIS_SERVICE_ID_MALWARE = 225
    IRIS_SERVICE_ID_NETWORK_ABUSE = 232
    IRIS_GROUP_ID_CSA = 443

    def __init__(self):
        super(ProductionAppConfig, self).__init__()


class DevelopmentAppConfig(AppConfig):
    IRIS_WSDL = "https://iris-ws.dev.int.godaddy.com/iriswebservice.asmx?WSDL"
    IRIS_SERVER = 'P3DWSQL07\CSS'

    IRIS_SERVICE_ID_PHISHING = 212
    IRIS_SERVICE_ID_MALWARE = 213
    IRIS_SERVICE_ID_NETWORK_ABUSE = 260
    IRIS_GROUP_ID_CSA = 510

    def __init__(self):
        super(DevelopmentAppConfig, self).__init__()


config_by_name = {'dev': DevelopmentAppConfig, 'prod': ProductionAppConfig}
