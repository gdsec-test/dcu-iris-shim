from nose.tools import assert_true
from mock import patch

from emailreporter import EmailReporter
import os
import logging


class TestEmailReporter:

    @classmethod
    def setup(cls):
        os.environ['shim_messaging_cert'] = '/dev/null'
        os.environ['shim_messaging_key'] = '/dev/null'
        cls.emailreporter = EmailReporter(logging.getLogger(__name__))

    @patch('emailreporter.requests.post')
    def test_route_method(self, fakerequest):
        self.emailreporter.route_mail({'email': 'dcuinternal@godaddy.com', 'incident': 1234})
        fakerequest.assert_called_once()

        self.emailreporter.route_mail({}) #should bail early and not attempt an API call
        os.environ['sysenv'] = 'ote' #should bail early due to being OTE, and not attempt an API call
        self.emailreporter.route_mail({'email': 'dcuinternal@godaddy.com', 'incident': 1234})
        fakerequest.assert_called_once() #ensure no more API calls have happened

    @patch('emailreporter.requests.post')
    def test_no_parse_route_mail(self, fakerequest):
        self.emailreporter.route_mail({'email': 'dcuinternal@godaddy.com', 'incident': 1234}, nothing_parsed=True)
        fakerequest.assert_called_once()
