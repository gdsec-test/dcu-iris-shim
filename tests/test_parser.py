from nose.tools import assert_equal

from iris_shim.parser import Parser


class TestParser:

    def __init__(self):
        self._parser = Parser()

    def test_parse_phish_malware_remove_reporter_domain(self):
        email = '''
                This is an email that contains valid domains impcat.net and Coolexample.com. It also
                contains valid reporter domain comicsN.beer which we want to match regardless of case and
                be removed from the reportable domains list.  We also want to ensure subdomains that contain
                the domain of the reporter email are not processed, such as dont.process.me.CoMiCsN.bEeR
                '''
        _, domains, _ = self._parser.parse_phish_malware(email, 'paddy@Comicsn.beer')
        assert_equal(domains, {'impcat.net', 'coolexample.com'})
        _, domains, _ = self._parser.parse_phish_malware(email, None)
        assert_equal(domains, {'impcat.net', 'coolexample.com', 'comicsn.beer', 'dont.process.me.comicsn.beer'})
        _, domains, _ = self._parser.parse_phish_malware(email, 'tesaaronbean.com')
        assert_equal(domains, {'impcat.net', 'coolexample.com', 'comicsn.beer', 'dont.process.me.comicsn.beer'})

    def test_parse_phish_malware_remove_domain_in_url(self):
        email = '''
                This is an email that contains valid domains impcat.net and coolexample.com. It also
                contains valid urls http://Coolexample.com/phishing and http://abc.com/phishing .
                Also godaddy.com is blacklisted.
                '''
        urls, domains, domains_blacklist = self._parser.parse_phish_malware(email, None)
        assert_equal(domains, {'impcat.net'})
        assert_equal(urls, {'http://Coolexample.com/phishing', 'http://abc.com/phishing'})
        assert_equal(domains_blacklist, {'godaddy.com'})

    def test_parse_netabuse(self):
        email = '''
                This is an email that contains valid ips 255.255.255.0 and 127.0.0.1 .
                '''
        ips = self._parser.parse_netabuse(email)
        assert_equal(ips, {'255.255.255.0', '127.0.0.1'})
