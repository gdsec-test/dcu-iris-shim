from nose.tools import assert_equal, assert_true, assert_false
from match_domains import MatchDomain

class TestMatchDomains:
    def __init__(self): self.match = MatchDomain()

    def test_get_domains_invalid(self):
        data = 'There is no domain name here.'
        actual = self.match.get_domains(data)
        assert_equal(actual, [])

    def test_get_domains_null_value(self):
        data = None
        assert_false(self.match.get_domains(data))

    def test_get_domains(self):
        data = 'godaddy.com is a valid domain name'
        actual = self.match.get_domains(data)
        assert_equal(actual, ['godaddy.com'])

    def test_is_valid_domain_success(self):
        data = 'godaddy.com'
        assert_true(self.match.is_valid_domain(data))

    def test_is_valid_domain_failure(self):
        data = 'godaddy.php'
        assert_false(self.match.is_valid_domain(data))


    def test_is_valid_domain_null_value(self):
        data = None
        assert_false(self.match.is_valid_domain(data))