from collections import defaultdict, namedtuple
from datetime import datetime

from mock import patch
from nose.tools import assert_equal

from iris_shim.managers.csam_manager import CSAMReportManager
from iris_shim.models import Report, Reporter
from tests.test_mocks import MockAbuseAPI, MockIrisSoap

IncidentInfo = namedtuple('IncidentInfo', 'Subject')


class TestCSAMReportManager:
    """Testing the CSAM Implementation of the Report Manager"""

    reporter_email = 'dcuinternal@godaddy.com'

    def __init__(self):
        self._csam_manager = CSAMReportManager(MockIrisSoap, MockAbuseAPI)
        self._reporter = Reporter('dcuinternal@godaddy.com')
        self._csam_report = Report('1234', 'CHILD_ABUSE', self.reporter_email,
                                   datetime(2017, 11, 29, 8, 38, 47, 420000))
        self._csam_report_invalid = Report('2111', 'CHILD_ABUSE', self.reporter_email,
                                           datetime(2017, 11, 29, 8, 38, 47, 420000))

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
