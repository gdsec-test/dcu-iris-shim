import os


class AppConfig(object):
    IRIS_WSDL = None
    IRIS_SERVER = None
    IRIS_PORT = None

    IRIS_DATABASE = 'iris'

    IRIS_SERVICE_ID_PHISHING = None
    IRIS_SERVICE_ID_MALWARE = None
    IRIS_SERVICE_ID_NETWORK_ABUSE = None
    IRIS_GROUP_ID_CSA = None
    IRIS_GROUP_ID_OPS_DIGITAL_CRIMES = None

    ABUSE_API_URL = None

    NON_PROD_EMAIL = os.getenv('EMAIL_RECIPIENT', 'dcuinternal@godaddy.com')

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
    IRIS_PORT = 1433

    IRIS_SERVICE_ID_PHISHING = 226
    IRIS_SERVICE_ID_MALWARE = 225
    IRIS_SERVICE_ID_NETWORK_ABUSE = 232
    IRIS_SERVICE_ID_CHILD_ABUSE = 221
    IRIS_GROUP_ID_CSA = 443
    IRIS_GROUP_ID_OPS_DIGITAL_CRIMES = 409

    ABUSE_API_URL = "https://api.godaddy.com/v1/abuse/tickets"

    NON_PROD_EMAIL = None

    def __init__(self):
        super(ProductionAppConfig, self).__init__()


class DevelopmentAppConfig(AppConfig):
    IRIS_WSDL = "https://iris-ws.dev.int.godaddy.com/iriswebservice.asmx?WSDL"
    # IRIS_SERVER = 'P3DWSQL07\\CSS'
    IRIS_SERVER = '10.32.76.23\\CSS'

    IRIS_SERVICE_ID_PHISHING = 212
    IRIS_SERVICE_ID_MALWARE = 213
    IRIS_SERVICE_ID_NETWORK_ABUSE = 260
    IRIS_SERVICE_ID_CHILD_ABUSE = 214
    IRIS_GROUP_ID_CSA = 510
    IRIS_GROUP_ID_OPS_DIGITAL_CRIMES = 510

    ABUSE_API_URL = "https://api.dev-godaddy.com/v1/abuse/tickets"

    def __init__(self):
        super(DevelopmentAppConfig, self).__init__()


config_by_name = {'dev': DevelopmentAppConfig, 'prod': ProductionAppConfig}
