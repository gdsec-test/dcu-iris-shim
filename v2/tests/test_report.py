from datetime import datetime

from nose.tools import assert_equal, assert_false, assert_is_none, assert_true

from v2.iris_shim.blacklist import emails
from v2.iris_shim.models import Report


class TestReport(object):
    def __init__(self):
        self._report = Report('1235', 'PHISHING', 'dcuinternal@godaddy.com', datetime(2017, 11, 29, 8, 38, 47, 420000))

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
        assert False
