from nose.tools import assert_equal
from match_domains import MatchDomain

class TestMatchUrls:
    def __init__(self): self.match = MatchDomain()

    def test_get_domains_invalid(self):
        data = 'There is no domain name here.'
        actual = self.match.get_domains(data)
        assert_equal(actual, [])

    def test_get_domains(self):
        data = 'godaddy.com is a valid domain name'
        actual = self.match.get_domains(data)
        assert_equal(actual, ['godaddy.com'])
