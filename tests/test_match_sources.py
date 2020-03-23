import re

from nose.tools import assert_equal, assert_false, assert_set_equal

from iris_shim.utils.match_sources import MatchSources


class TestMatchSources:
    def __init__(self):
        self.match = MatchSources()

    '''Test IP Matching'''

    def test_get_ip_real(self):
        data = '208.109.52.189'
        actual = self.match.get_ip(data)
        assert_equal(actual, ['208.109.52.189'])

    def test_get_ip_imagined(self):
        data = '101.254.52.189'
        actual = self.match.get_ip(data)
        assert_equal(actual, ['101.254.52.189'])

    '''Test URL Matching'''

    def test_get_urls_plain(self):
        data = 'https://pypi.python.org/pypi/stringtheory'
        actual = self.match.get_urls(data)
        assert_equal(actual, {'https://pypi.python.org/pypi/stringtheory'})

    def test_get_urls_munged(self):
        data = 'hxxps://pypi[dot]python[dot]org/pypi/stringtheory'
        actual = self.match.get_urls(data)
        assert_equal(actual, {'https://pypi.python.org/pypi/stringtheory'})

    def test_get_urls_with_emails(self):
        data = 'https://pypi.python.org/pypi?e=reporter@company.tld'
        actual = self.match.get_urls(data)
        assert_equal(actual, {'https://pypi.python.org/pypi?e=redacted@redacted.tld'})

    '''Test Domain Matching'''

    def test_get_domains_invalid(self):
        data = 'There is no domain name here.'
        actual = self.match.get_domains(data)
        assert_equal(actual, set())

    def test_get_domains_null_value(self):
        data = None
        assert_false(self.match.get_domains(data))

    def test_get_domains(self):
        data = 'comicsn.beer is a valid domain name and sample@abc.com is an email address'
        actual = self.match.get_domains(data)
        assert_equal(actual, {'comicsn.beer'})

    def test_is_valid_domain_success(self):
        data = ['comicsn.beer']
        actual = self.match.is_valid_domain(data)
        assert_equal(actual, {'comicsn.beer'})

    def test_is_valid_domain_failure(self):
        data = ['godaddy.php']
        actual = self.match.is_valid_domain(data)
        assert_equal(actual, set())

    def test_is_valid_domain_null_value(self):
        data = None
        assert_false(self.match.is_valid_domain(data))

    def test_separate_blacklisted_domains_both_valid(self):
        data = ['godaddy.com', 'notblacklisted.com']
        actual = self.match.separate_blacklisted_domains(data)
        assert_equal(actual, ({'notblacklisted.com'}, {'godaddy.com'}))

    def test_separate_blacklisted_domains_one_valid(self):
        data = ['godaddy.com']
        actual = self.match.separate_blacklisted_domains(data)
        assert_equal(actual, (set(), {'godaddy.com'}))

    def test_separate_blacklisted_domains_one_empty(self):
        data = ['godaddy.com', '']
        actual = self.match.separate_blacklisted_domains(data)
        assert_equal(actual, ({''}, {'godaddy.com'}))

    def test_separate_blacklisted_domains_null_list(self):
        data = []
        actual = self.match.separate_blacklisted_domains(data)
        assert_equal(actual, (set(), set()))

    def test_separate_blacklisted_domains_uppercase_domain(self):
        data = ['GoDaddy.com', 'NotBlackListed.com']
        actual = self.match.separate_blacklisted_domains(data)
        assert_equal(actual, ({'NotBlackListed.com'}, {'GoDaddy.com'}))

    def test_valid_domain_names_regex(self):
        data = 'sample1.com sample2.co.au'
        actual = re.findall(self.match.domain_names, data)
        assert_equal(actual, ['sample1.com', 'sample2.co.au'])

    def test_invalid_domain_names_regex(self):
        data = "1-Bad-Domain#.com 1-bad-domain.-com"
        actual = re.findall(self.match.domain_names, data)
        assert_equal(actual, [])

    def test_valid_ip_regex(self):
        data = '192.168.255.255 10.0.0.0'
        actual = re.findall(self.match.ip_regex, data)
        assert_equal(actual, ['192.168.255.255', '10.0.0.0'])

    def test_invalid_ip_regex(self):
        data = '1234.1231.132.3125 abc.123.456.cde'
        actual = re.findall(self.match.ip_regex, data)
        assert_equal(actual, [])

    def test_valid_url_regex(self):
        data = 'http://foo.com https://www.bar.com'
        actual = re.findall(self.match.url, data)
        assert_equal(actual, ['http://foo.com', 'https://www.bar.com'])

    def test_invalid_url_regex(self):
        data = 'http:// shouldfail.com'
        actual = re.findall(self.match.url, data)
        assert_equal(actual, [])

    def test_valid_email_regex(self):
        data = 'sample@foo.com sample2@foo.bar.com'
        actual = re.findall(self.match.email_id_regex, data)
        assert_equal(actual, ['sample@foo.com', 'sample2@foo.bar.com'])

    def test_invalid_email_regex(self):
        data = '#@%^%#$@#$@#.com thisis"notallowed"@example.com'
        actual = re.findall(self.match.email_id_regex, data)
        assert_equal(actual, [])

    '''Test Regex Domain Filtering'''

    def test_domains_with_regex_match(self):
        data = {'252fimagesak.secureserver.net',
                '2fimagesak.secureserver.net',
                '50analytics.secureserver.net',
                'a2nlsmtp01-02.prod.iad2.secureserver.net',
                'bounce.secureserver.net',
                'bounces.em.secureserver.net',
                'certs.secureserver.net',
                'checkspam.secureserver.net',
                'em.secureserver.net',
                'fimagesak.secureserver.net',
                'imagesak.secureserver.net',
                'img.secureserver.net',
                'm117.em.secureserver.net',
                'mailstore1.europe.secureserver.net',
                'mailstore1.secureserver.net',
                'ns1.secureserver.net',
                'ns2.secureserver.net',
                'p3plgemwbe27-01.prod.phx3.secureserver.net',
                'p3plibsmtp01-10.prod.phx3.secureserver.net',
                'p3plibsmtp03-14.prod.phx3.secureserver.net',
                'p3plsmtp02-03-25.prod.phx3.secureserver.net',
                'p3plwbeout01-01.prod.phx3.secureserver.net',
                'secureserver.net',
                'smtp.asia.secureserver.net',
                'smtp.secureserver.net',
                'smtpout.secureserver.net',
                'sso.secureserver.net',
                'supportcenter.secureserver.net',
                'wbeout.secureserver.net',
                'www.secureserver.net',
                'impcat.com'}
        expected = {'impcat.com'}
        assert_equal(self.match.remove_domains_via_regex(data), expected)

    '''Test Regex URL Filtering'''

    # Will filter out all URLs
    def test_data_with_all_regex_match(self):
        data = {'http://www.secureserver.net/whois', 'http://secureserver.net/whois'}
        assert_false(self.match.remove_urls_via_regex(data))

    # Will filter out some URLs
    def test_data_with_some_regex_match(self):
        data = {'http://www.secureserver.net/whois', 'http://secureserver.net/whois', 'http://secureserver.net/'}
        assert_equal(self.match.remove_urls_via_regex(data), {'http://secureserver.net/'})

    # Wont filter out any URLs
    def test_data_with_no_regex_match(self):
        data = {'https://mysecureserver.net/whois', 'http://www.secureserver.net'}
        assert_equal(self.match.remove_urls_via_regex(data), data)
