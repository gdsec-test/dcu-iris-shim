from nose.tools import assert_true
from mock import patch

from api_ticket import APITicket
from datetime import datetime

class TestEnrichment:

    @classmethod
    def setup(cls):
        cls._apiticket = APITicket('dev')

    @patch('api_ticket.requests.post')
    def test_post_ticket(self, fakerequest):
        fakerequest.return_value = True
        ret = self._apiticket.post_ticket({'jwt': 'fakejwt', 'create_date': datetime.now()})
        assert_true(ret)