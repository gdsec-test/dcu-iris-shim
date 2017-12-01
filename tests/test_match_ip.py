from nose.tools import assert_equal

from match_ip import MatchIP


class TestMatchIp:

    def test_get_ip_real(self):
        match = MatchIP()
        data = '208.109.52.189'
        actual = match.get_ip(data)
        assert_equal(actual, ['208.109.52.189'])

    def test_get_ip_imagined(self):
        match = MatchIP()
        data = '101.254.52.189'
        actual = match.get_ip(data)
        assert_equal(actual, ['101.254.52.189'])
