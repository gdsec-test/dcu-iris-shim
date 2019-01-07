from collections import namedtuple
from datetime import datetime

from mock import patch
from nose.tools import assert_equal
from tests.test_mocks import MockAbuseAPI, MockIrisSoap, MockMailer

from iris_shim.managers.general_manager import GeneralManager
from iris_shim.models import Report, Reporter

IncidentInfo = namedtuple('IncidentInfo', 'Subject')


class TestReportManager:
    """Testing Methods that are shared between implementations of the Report Manager"""

    reporter_email = 'dcuinternal@godaddy.com'

    def __init__(self):
        self._manager = GeneralManager(MockIrisSoap(), MockMailer(), MockAbuseAPI())
        self._reporter = Reporter('dcuinternal@godaddy.com')
        self._report = Report('1234', 'PHISHING', self.reporter_email, datetime(2017, 11, 29, 8, 38, 47, 420000))

    def test_gather_reports_empty(self):
        assert_equal(self._manager._gather_reports({}), {})

    @patch.object(MockIrisSoap, 'get_report_info_by_id', return_value=IncidentInfo('we received your feedback'))
    def test_gather_reports_invalid_report(self, get_report_info_by_id):
        actual = self._manager._gather_reports({self._report})
        self._reporter.reports_invalid = [self._report]

        assert_equal(actual, {self.reporter_email: self._reporter})

    @patch.object(MockIrisSoap, 'get_report_info_by_id', return_value=IncidentInfo('test subject'))
    @patch.object(MockIrisSoap, 'get_customer_notes', return_value='malicious-url.com')
    def test_gather_reports(self, get_customer_notes, get_report_info_by_id):
        self._report.sources_valid = self._report.sources_reportable = {'malicious-url.com'}

        actual = self._manager._gather_reports([self._report])
        self._reporter.reports_reportable = [self._report]

        assert_equal(actual, {self.reporter_email: self._reporter})

    def test_action_reports_none(self):
        assert_equal(self._manager._action_reports({}), {})

    def test_create_abuse_report_none(self):
        actual_success, actual_fail = self._manager._create_abuse_report(self._report)

        assert_equal(actual_success, [])
        assert_equal(actual_fail, [])

    @patch.object(MockAbuseAPI, 'create_ticket', side_effect=['1', None])
    def test_create_abuse_report(self, create_ticket):
        self._report.sources_reportable = ['malicious-url.com', 'malicious-url.com/1/']
        actual_success, actual_fail = self._manager._create_abuse_report(self._report)

        assert_equal(actual_success, [('malicious-url.com', '1')])
        assert_equal(actual_fail, ['malicious-url.com/1/'])
