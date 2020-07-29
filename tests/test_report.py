from datetime import datetime

from nose.tools import (assert_equal, assert_false, assert_in, assert_is_none,
                        assert_not_in, assert_true)

from iris_shim.blacklist import emails
from iris_shim.models import Report


class TestReport(object):
    BLACKLIST = 'blacklist'
    VALID = 'valid subject'

    def __init__(self):
        self._report = Report('1235', 'PHISHING', 'dcuinternal@godaddy.com', datetime(2017, 11, 29, 8, 38, 47, 420000))
        self._report1 = Report('1236', 'PHISHING', 'test@theaaronbean.com', datetime(2017, 11, 29, 8, 38, 47, 420000))
        self._report2 = Report('1237', 'NETWORK_ABUSE', 'test@theaaronbean.com', datetime(2017, 11, 29, 8, 38, 47, 420000))
        self._report3 = Report('1238', 'CONTENT', 'test@theaaronbean.com', datetime(2017, 11, 29, 8, 38, 47, 420000))
        self._report4 = Report('1239', 'SPAM', 'donotreply@radix.support', datetime(2020, 7, 27, 1, 2, 3, 420000))

    def test_validate_blacklist_reporter(self):
        self._report.reporter_email = next(iter(emails))  # generic retrieval of a blacklist email
        self._report.validate(self.VALID)

        assert_false(self._report.valid)
        assert_equal(self._report.invalid_reason, self.BLACKLIST)

    def test_validate_blacklist_email_address(self):
        self._report4.validate(self.VALID)

        assert_false(self._report4.valid)
        assert_equal(self._report4.invalid_reason, self.BLACKLIST)

    def test_validate_blacklist_full_subject(self):
        self._report.validate('we received your feedback')

        assert_false(self._report.valid)
        assert_equal(self._report.invalid_reason, self.BLACKLIST)

    def test_validate_blacklist_partial_subject(self):
        self._report.validate('godaddy monitoring: http://wfswholesalefloors.com - security warning')

        assert_false(self._report.valid)
        assert_equal(self._report.invalid_reason, self.BLACKLIST)

    def test_validate_blacklist_no_matching_subject(self):
        self._report.validate(self.VALID)

        assert_true(self._report.valid)
        assert_is_none(self._report.invalid_reason)

    def test_str(self):
        assert_equal(str(self._report), "Report 1235 for reporter dcuinternal@godaddy.com")

    def test_repr(self):
        expected = "Report('1235', 'PHISHING', 'dcuinternal@godaddy.com', datetime.datetime(2017, 11, 29, 8, 38, 47, 420000))"
        assert_equal(repr(self._report), expected)

    def test_parse(self):
        email_body = 'http://www.comicsn.beer http://dcuinternal@godaddy.com more text example.com, riskiq.com, theaaronbean.com'
        email_body2 = '190.168.1.1, plus some random works and this ip: 191.168.1.0'
        self._report1.parse(email_body)
        self._report2.parse(email_body2)
        self._report3.parse(email_body)
        self._report4.parse(email_body2)

        assert_not_in('theaaronbean.com', self._report1.sources_valid)
        assert_in('http://www.comicsn.beer', self._report1.sources_valid)
        assert_in('riskiq.com', self._report1.sources_blacklist)
        assert_in('191.168.1.0', self._report2.sources_valid)
        assert_equal(self._report3.sources_reportable, set([]))
        assert_equal(self._report4.sources_reportable, set([]))

    def test_parse_uppercase_url(self):
        email_body1 = 'http://www.comicsN.beer http://dcuinternal@Godaddy.com more text example.com, Riskiq.com, theaaronbean.com'
        self._report1.parse(email_body1)

        assert_in('http://www.comicsN.beer', self._report1.sources_valid)
        assert_in('riskiq.com', self._report1.sources_blacklist)

    def test_parse_subdomain(self):
        email_body1 = 'http://www.comicsN.beer http://dcuinternal@Godaddy.com http://www.godaddy.com www.godaddy.com www.riskiq.net'
        self._report1.parse(email_body1)

        assert_in('http://www.comicsN.beer', self._report1.sources_valid)
        assert_in('www.riskiq.net', self._report1.sources_blacklist)
