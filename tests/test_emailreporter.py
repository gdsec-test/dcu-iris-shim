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
