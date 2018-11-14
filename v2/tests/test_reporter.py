from datetime import datetime

from nose.tools import assert_equal

from v2.iris_shim.models import Report, Reporter


class TestReporter(object):
    def __init__(self):
        self._reporter = Reporter('dcuinternal@godaddy.com')
        self._report = Report('1235', 'PHISHING', 'dcuinternal@godaddy.com', datetime(2017, 11, 29, 8, 38, 47, 420000))

    def test_add_incident_reportable(self):
        self._report.sources_reportable = {'malicious-url.com'}
        self._reporter.add_incident(self._report)

        expected = Reporter('dcuinternal@godaddy.com')
        expected.reports_reportable = [self._report]

        assert_equal(self._reporter, expected)

    def test_add_incident_invalid(self):
        self._report.valid = False
        self._reporter.add_incident(self._report)

        expected = Reporter('dcuinternal@godaddy.com')
        expected.reports_invalid = [self._report]

        assert_equal(self._reporter, expected)

    def test_add_incident_valid(self):
        self._report.sources_valid = {'malicious-url.com'}
        self._reporter.add_incident(self._report)

        expected = Reporter('dcuinternal@godaddy.com')
        expected.reports_valid = [self._report]

        assert_equal(self._reporter, expected)

    def test_str(self):
        assert_equal(str(self._reporter), "Reporter dcuinternal@godaddy.com, reports reportable: [], reports invalid: []")

    def test_repr(self):
        assert_equal(repr(self._reporter), "Reporter('dcuinternal@godaddy.com')")
