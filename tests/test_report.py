from datetime import datetime

from nose.tools import (assert_equal, assert_false, assert_in, assert_is_none,
                        assert_not_in, assert_true)

from iris_shim.blacklist import emails
from iris_shim.models import Report


class TestReport(object):
    def __init__(self):
        self._report = Report('1235', 'PHISHING', 'dcuinternal@godaddy.com', datetime(2017, 11, 29, 8, 38, 47, 420000))
        self._report1 = Report('1236', 'PHISHING', 'test@theaaronbean.com', datetime(2017, 11, 29, 8, 38, 47, 420000))
        self._report2 = Report('1237', 'NETWORK_ABUSE', 'test@theaaronbean.com', datetime(2017, 11, 29, 8, 38, 47, 420000))
        self._report3 = Report('1238', 'CONTENT', 'test@theaaronbean.com', datetime(2017, 11, 29, 8, 38, 47, 420000))

    def test_validate_blacklist_reporter(self):
        self._report.reporter_email = next(iter(emails))  # generic retrieval of a blacklist email
        self._report.validate('valid subject')

        assert_false(self._report.valid)
        assert_equal(self._report.invalid_reason, 'blacklist')

    def test_validate_blacklist_subject(self):
        self._report.validate('we received your feedback')

        assert_false(self._report.valid)
        assert_equal(self._report.invalid_reason, 'blacklist')

    def test_validate(self):
        self._report.validate('valid subject')

        assert_true(self._report.valid)
        assert_is_none(self._report.invalid_reason)

    def test_str(self):
        assert_equal(str(self._report), "Report 1235 for reporter dcuinternal@godaddy.com")

    def test_repr(self):
        expected = "Report('1235', 'PHISHING', 'dcuinternal@godaddy.com', datetime.datetime(2017, 11, 29, 8, 38, 47, 420000))"
        assert_equal(repr(self._report), expected)

    def test_parse(self):
        email_body = 'http://www.comicsn.beer more text example.com, riskiq.com, theaaronbean.com'
        email_body2 = '190.168.1.1, plus some random works and this ip: 191.168.1.0'
        self._report1.parse(email_body)
        self._report2.parse(email_body2)
        self._report3.parse(email_body)

        assert_not_in('theaaronbean.com', self._report1.sources_valid)
        assert_in('http://www.comicsn.beer', self._report1.sources_valid)
        assert_in('191.168.1.0', self._report2.sources_valid)
        assert_equal(self._report3.sources_reportable, set([]))
