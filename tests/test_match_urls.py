from nose.tools import assert_equal

from match_urls import MatchURL


class TestMatchUrls:
    def __init__(self): self.match = MatchURL()

    def test_get_urls_plain(self):
        data = 'https://pypi.python.org/pypi/stringtheory'
        actual = self.match.get_urls(data)
        assert_equal(actual, ['https://pypi.python.org/pypi/stringtheory'])

    def test_get_urls_munged(self):
        data = 'hxxps://pypi[dot]python[dot]org/pypi/stringtheory'
        actual = self.match.get_urls(data)
        assert_equal(actual, ['https://pypi.python.org/pypi/stringtheory'])

