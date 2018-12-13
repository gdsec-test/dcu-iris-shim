from nose.tools import assert_equal, assert_false

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
        assert_equal(actual, ['https://pypi.python.org/pypi/stringtheory'])

    def test_get_urls_munged(self):
        data = 'hxxps://pypi[dot]python[dot]org/pypi/stringtheory'
        actual = self.match.get_urls(data)
        assert_equal(actual, ['https://pypi.python.org/pypi/stringtheory'])

    '''Test Domain Matching'''

    def test_get_domains_invalid(self):
        data = 'There is no domain name here.'
        actual = self.match.get_domains(data)
        assert_equal(actual, ([]))

    def test_get_domains_null_value(self):
        data = None
        assert_false(self.match.get_domains(data))

    def test_get_domains(self):
        data = 'comicsn.beer is a valid domain name'
        actual = self.match.get_domains(data)
        assert_equal(actual, ['comicsn.beer'])

    def test_is_valid_domain_success(self):
        data = ['comicsn.beer']
        actual = self.match.is_valid_domain(data)
        assert_equal(actual, ['comicsn.beer'])

    def test_is_valid_domain_failure(self):
        data = ['godaddy.php']
        actual = self.match.is_valid_domain(data)
        assert_equal(actual, [])

    def test_is_valid_domain_null_value(self):
        data = None
        assert_false(self.match.is_valid_domain(data))

    def test_separate_blacklisted_domains_both_valid(self):
        data = ['godaddy.com', 'notblacklisted.com']
        actual = self.match.separate_blacklisted_domains(data)
        assert_equal(actual, (['notblacklisted.com'], ['godaddy.com']))

    def test_separate_blacklisted_domains_one_valid(self):
        data = ['godaddy.com']
        actual = self.match.separate_blacklisted_domains(data)
        assert_equal(actual, ([], ['godaddy.com']))

    def test_separate_blacklisted_domains_one_empty(self):
        data = ['godaddy.com', '']
        actual = self.match.separate_blacklisted_domains(data)
        assert_equal(actual, ([''], ['godaddy.com']))

    def test_separate_blacklisted_domains_null_list(self):
        data = []
        actual = self.match.separate_blacklisted_domains(data)
        assert_equal(actual, ([], []))
