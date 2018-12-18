from collections import defaultdict, namedtuple
from datetime import datetime

from mock import patch
from nose.tools import assert_equal, assert_false, assert_true

from iris_shim.manager import ReportManager
from iris_shim.models import Report, Reporter

IncidentInfo = namedtuple('IncidentInfo', 'Subject')


class MockMailer(object):
    def report_successfully_parsed(self, reporter_email):
        pass

    def report_failed_to_parse(self, reporter_email):
        pass


class MockIrisSoap(object):
    note_successfully_parsed = None
    note_failed_to_parse = None

    def get_customer_notes(self, report_id):
        pass

    def get_report_info_by_id(self, report_id):
        pass

    def notate_report_and_close(self, report_id, note):
        pass


class MockAbuseAPI(object):
    def create_ticket(self, type, source, report_id, reporter_email, modify_date):
        pass


class TestReportManager:
    reporter_email = 'dcuinternal@godaddy.com'

    def __init__(self):
        self._manager = ReportManager(MockIrisSoap(), MockMailer(), MockAbuseAPI())
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

    @patch.object(MockMailer, 'report_failed_to_parse', side_effect=[False, True])
    def test_send_customer_interaction_failed_to_parse(self, report_failed_to_parse):
        assert_false(self._manager._send_customer_interaction(self._reporter))
        assert_true(self._manager._send_customer_interaction(self._reporter))

    @patch.object(MockMailer, 'report_successfully_parsed', side_effect=[False, True])
    def test_send_customer_interaction_successfully_parsed(self, report_successfully_parsed):
        self._reporter.reports_valid = [self._report]

        assert_false(self._manager._send_customer_interaction(self._reporter))
        assert_true(self._manager._send_customer_interaction(self._reporter))

    @patch.object(ReportManager, '_create_abuse_report', side_effect=[([('malicious-url.com', 'DCU1234')], [])])
    @patch.object(ReportManager, '_send_customer_interaction')
    def test_action_reports(self, _send_customer_interaction, _create_abuse_report):
        self._report.sources_reportable = {'malicious-url.com'}
        self._reporter.reports_reportable = [self._report]

        actual = self._manager._action_reports({self.reporter_email: self._reporter})

        ticket_for_reporters = defaultdict(dict)
        ticket_for_reporters['1234']['success'] = [('malicious-url.com', 'DCU1234')]
        ticket_for_reporters['1234']['fail'] = []

        assert_equal(actual, {self.reporter_email: ticket_for_reporters})