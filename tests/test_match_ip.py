from nose.tools import assert_equal

from match_ip import MatchIP


class TestMatchIp:
    def __init__(self): self.match = MatchIP()

    def test_get_ip_real(self):
        data = '208.109.52.189'
        actual = self.match.get_ip(data)
        assert_equal(actual, ['208.109.52.189'])

    def test_get_ip_imagined(self):
        data = '101.254.52.189'
        actual = self.match.get_ip(data)
        assert_equal(actual, ['101.254.52.189'])
