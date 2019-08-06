from collections import defaultdict, namedtuple
from datetime import datetime

from mock import patch
from nose.tools import assert_equal, assert_false, assert_true

from iris_shim.managers.general_manager import GeneralManager
from iris_shim.models import Report, Reporter
from tests.test_mocks import MockAbuseAPI, MockIrisSoap, MockMailer

IncidentInfo = namedtuple('IncidentInfo', 'Subject')


class TestGeneralReportManager:
    """Testing the General Implementation of the Report Manager"""

    reporter_email = 'dcuinternal@godaddy.com'

    def __init__(self):
        self._manager = GeneralManager(MockIrisSoap(), MockMailer(), MockAbuseAPI())
        self._reporter = Reporter('dcuinternal@godaddy.com')
        self._report = Report('1234', 'PHISHING', self.reporter_email, datetime(2017, 11, 29, 8, 38, 47, 420000))

    @patch.object(MockMailer, 'report_failed_to_parse', side_effect=[False, True])
    def test_send_customer_interaction_failed_to_parse(self, report_failed_to_parse):
        assert_false(self._manager._send_customer_interaction(self._reporter))
        assert_true(self._manager._send_customer_interaction(self._reporter))

    @patch.object(MockMailer, 'report_successfully_parsed', side_effect=[False, True])
    def test_send_customer_interaction_successfully_parsed(self, report_successfully_parsed):
        self._reporter.reports_valid = [self._report]

        assert_false(self._manager._send_customer_interaction(self._reporter))
        assert_true(self._manager._send_customer_interaction(self._reporter))

    @patch.object(GeneralManager, '_create_abuse_report', side_effect=[([('malicious-url.com', 'DCU1234')], [])])
    @patch.object(GeneralManager, '_send_customer_interaction')
    def test_action_reports(self, _send_customer_interaction, _create_abuse_report):
        self._report.sources_reportable = {'malicious-url.com'}
        self._reporter.reports_reportable = [self._report]

        actual = self._manager._action_reports({self.reporter_email: self._reporter})

        ticket_for_reporters = defaultdict(dict)
        ticket_for_reporters['1234']['success'] = [('malicious-url.com', 'DCU1234')]
        ticket_for_reporters['1234']['fail'] = []

        assert_equal(actual, {self.reporter_email: ticket_for_reporters})
