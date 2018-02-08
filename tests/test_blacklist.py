from nose.tools import assert_true

from blacklist import blacklist, invalid_email_subject

class TestBlacklist:

    def test_invalid_email_subject(self):
        matched = False
        for reg in invalid_email_subject:
            if reg.search('We received your feedback regarding this report'):
                matched = True
        assert_true(matched)
        