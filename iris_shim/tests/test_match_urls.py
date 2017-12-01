from nose.tools import assert_equal

from match_urls import MatchURL


class TestMatchUrls:

    def test_get_urls_plain(self):
        match = MatchURL()
        data = 'https://pypi.python.org/pypi/stringtheory'
        actual = match.get_urls(data)
        assert_equal(actual, ['https://pypi.python.org/pypi/stringtheory'])

    def test_get_urls_munged(self):
        match = MatchURL()
        data = 'hxxps://pypi[dot]python[dot]org/pypi/stringtheory'
        actual = match.get_urls(data)
        assert_equal(actual, ['https://pypi.python.org/pypi/stringtheory'])
