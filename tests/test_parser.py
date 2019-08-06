from nose.tools import assert_equal

from iris_shim.parser import Parser


class TestParser:

    def __init__(self):
        self._parser = Parser()

    def test_parse_phish_malware_remove_reporter_domain(self):
        email = '''
                This is an email that contains valid domains impcat.net and coolexample.com. It also
                contains valid reporter domain comicsn.beer
                '''
        _, domains, _ = self._parser.parse_phish_malware(email, 'paddy@comicsn.beer')
        assert_equal(domains, {'impcat.net', 'coolexample.com'})
        _, domains, _ = self._parser.parse_phish_malware(email, None)
        assert_equal(domains, {'impcat.net', 'coolexample.com', 'comicsn.beer'})
        _, domains, _ = self._parser.parse_phish_malware(email, 'tesaaronbean.com')
        assert_equal(domains, {'impcat.net', 'coolexample.com', 'comicsn.beer'})

    def test_parse_phish_malware_remove_domain_in_url(self):
        email = '''
                This is an email that contains valid domains impcat.net and coolexample.com. It also
                contains valid urls http://coolexample.com/phishing and http://abc.com/phishing .
                Also godaddy.com is blacklisted.
                '''
        urls, domains, domains_blacklist = self._parser.parse_phish_malware(email, None)
        assert_equal(domains, {'impcat.net'})
        assert_equal(urls, {'http://coolexample.com/phishing', 'http://abc.com/phishing'})
        assert_equal(domains_blacklist, {'godaddy.com'})

    def test_parse_netabuse(self):
        email = '''
                This is an email that contains valid ips 255.255.255.0 and 127.0.0.1 .
                '''
        ips = self._parser.parse_netabuse(email)
        assert_equal(ips, {'255.255.255.0', '127.0.0.1'})
