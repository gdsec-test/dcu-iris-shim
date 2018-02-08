from nose.tools import assert_true, assert_equal
from mock import create_autospec

from query_incident import QueryIncident

class TestQueryIncident:

    @classmethod
    def setup(cls):
        cls.queryincident = QueryIncident('https://iris-ws.dev.int.godaddy.com/iriswebservice.asmx?wsdl')
        #By using the actual WSDL here, we can then easily autospec / mock out the calls to the service
        service = cls.queryincident._client.service

        real_AddIncidentNote = service.AddIncidentNote
        service.AddIncidentNote = create_autospec(real_AddIncidentNote)

        real_QuickCloseIncident = service.QuickCloseIncident
        service.QuickCloseIncident = create_autospec(real_QuickCloseIncident)

        real_GetIncidentCustomerNotes = service.GetIncidentCustomerNotes
        service.GetIncidentCustomerNotes = create_autospec(real_GetIncidentCustomerNotes)

        real_GetIncidentInfoByIncidentId = service.GetIncidentInfoByIncidentId
        service.GetIncidentInfoByIncidentId = create_autospec(real_GetIncidentInfoByIncidentId)

    def test_get_incident_info(self):
        fake_GetIncidentCustomerNotes = self.queryincident._client.service.GetIncidentCustomerNotes
        fake_GetIncidentInfoByIncidentId = self.queryincident._client.service.GetIncidentInfoByIncidentId

        fake_GetIncidentCustomerNotes.return_value = 'URL: http://impcat.com/?i=1&amp;o=2<br/></p>Thank you'
        fake_GetIncidentInfoByIncidentId.return_value = 'anything'

        incident_info, notes_text = self.queryincident.get_incident_info(1337)
        assert_equal(incident_info, 'anything')
        assert_equal(notes_text, "URL: http://impcat.com/?i=1&o=2  Thank you")

    def test_close_incident(self):
        fake_AddIncidentNote = self.queryincident._client.service.AddIncidentNote
        fake_QuickCloseIncident = self.queryincident._client.service.QuickCloseIncident

        self.queryincident.close_incident(1234)
        fake_AddIncidentNote.assert_called_with(1234, self.queryincident.standard_msg, 'phishtory')
        fake_QuickCloseIncident.assert_called_with(1234, 15550)

        self.queryincident.close_incident(1235, 'my reason')
        fake_AddIncidentNote.assert_called_with(
            1235,
            self.queryincident.reason_msg.format('my reason'),
            'phishtory')
        fake_QuickCloseIncident.assert_called_with(1235, 15550)

        fake_QuickCloseIncident.reset_mock()
        self.queryincident.close_incident(1236)
        self.queryincident.close_incident(1236)
        #while we call close_incident 3 times, 2 of those use the same IID, so QuickCloseIncident
        #should only get called twice total.
        fake_QuickCloseIncident.assert_called_once_with(1236, 15550)