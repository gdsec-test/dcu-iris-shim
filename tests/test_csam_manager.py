from collections import defaultdict, namedtuple
from datetime import datetime

from mock import patch
from nose.tools import assert_equal

from iris_shim.managers.csam_manager import CSAMReportManager
from iris_shim.models import Report, Reporter

IncidentInfo = namedtuple('IncidentInfo', 'Subject')


class MockIrisSoap(object):
    note_successfully_parsed = None
    note_csam_failed_to_parse = None
    note_csam_failed_to_submit_to_api = None

    def notate_report_and_close(self, report_id, note):
        pass

    def notate_report(self, report_id, note):
        pass

    def get_customer_notes(self, report_id):
        pass

    def get_report_info_by_id(self, report_id):
        pass


class MockAbuseAPI(object):
    def create_ticket(self, type, source, report_id, reporter_email, modify_date):
        pass


class TestCSAMReportManager:
    reporter_email = 'dcuinternal@godaddy.com'

    def __init__(self):
        self._csam_manager = CSAMReportManager(MockIrisSoap, MockAbuseAPI)
        self._reporter = Reporter('dcuinternal@godaddy.com')
        self._csam_report = Report('1234', 'CHILD_ABUSE', self.reporter_email,
                                   datetime(2017, 11, 29, 8, 38, 47, 420000))
        self._csam_report_invalid = Report('2111', 'CHILD_ABUSE', self.reporter_email,
                                           datetime(2017, 11, 29, 8, 38, 47, 420000))

    def test_gather_reports_empty(self):
        assert_equal(self._csam_manager._gather_reports({}), {})

    @patch.object(MockIrisSoap, 'get_report_info_by_id', return_value=IncidentInfo('we received your feedback'))
    def test_gather_reports_invalid_report(self, get_report_info_by_id):
        actual = self._csam_manager._gather_reports({self._csam_report_invalid})
        self._reporter.reports_invalid = [self._csam_report_invalid]

        assert_equal(actual, {self.reporter_email: self._reporter})

    @patch.object(MockIrisSoap, 'get_report_info_by_id', return_value=IncidentInfo('test subject'))
    @patch.object(MockIrisSoap, 'get_customer_notes', return_value='malicious-url.com')
    def test_gather_reports(self, get_customer_notes, get_report_info_by_id):
        self._csam_report.sources_valid = self._csam_report.sources_reportable = {'malicious-url.com'}

        actual = self._csam_manager._gather_reports([self._csam_report])
        self._reporter.reports_reportable = [self._csam_report]

        assert_equal(actual, {self.reporter_email: self._reporter})

    def test_action_reports_none(self):
        assert_equal(self._csam_manager._action_reports({}), {})

    @patch.object(MockIrisSoap, 'notate_report')
    @patch.object(MockIrisSoap, 'notate_report_and_close')
    @patch.object(CSAMReportManager, '_create_abuse_report',
                  side_effect=[([('malicious-url.com', 'DCU1234')], [])])
    def test_action_csam_reports(self, _create_abuse_report, notate_report_and_close, notate_report):
        self._reporter.reports_invalid = [self._csam_report_invalid]
        self._csam_report.sources_reportable = ['malicious-url.com']
        self._reporter.reports_reportable = [self._csam_report]

        actual = self._csam_manager._action_reports({self.reporter_email: self._reporter})

        report_summary = defaultdict(list)
        report_summary['successfully_submitted_to_api'] = ['1234']
        report_summary['needs_investigator_review'] = ['2111']

        assert_equal(actual.get('successfully_submitted_to_api'), report_summary.get('successfully_submitted_to_api'))
        assert_equal(actual.get('needs_investigator_review'), report_summary.get('needs_investigator_review'))

    @patch.object(MockIrisSoap, 'notate_report')
    @patch.object(CSAMReportManager, '_create_abuse_report',
                  side_effect=[([()], ['needs-review.com', 'also-needs-review.com'])])
    def test_action_csam_reports_fail(self, _create_abuse_report, notate_report):
        self._csam_report.sources_reportable = ['needs-review.com', 'also-needs-review.com']
        self._reporter.reports_reportable = [self._csam_report]

        actual = self._csam_manager._action_reports({self.reporter_email: self._reporter})

        report_summary = defaultdict(list)
        report_summary['needs_investigator_review'] = ['1234']

        assert_equal(actual.get('needs_investigator_review'), report_summary.get('needs_investigator_review'))

    @patch.object(MockAbuseAPI, 'create_ticket', side_effect=['1', None])
    def test_csam_create_abuse_report(self, create_ticket):
        self._csam_report.sources_reportable = ['malicious-url.com', 'malicious-url.com/1/']
        actual_success, actual_fail = self._csam_manager._create_abuse_report(self._csam_report)

        assert_equal(actual_success, [('malicious-url.com', '1')])
        assert_equal(actual_fail, ['malicious-url.com/1/'])
