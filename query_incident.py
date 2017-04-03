import HTMLParser
import logging
import suds.client
import re


class QueryIncident:

    def __init__(self, wsdl):
        self._logger = logging.getLogger(__name__)
        self._client = suds.client.Client(wsdl)

    def get_incident_info(self, incident):
        """
        Gathers the customer notes and incident information
        :param incident:
        :return:
        """
        self._logger.info('Gathering info for: %s', incident)
        # Get ticket text as string
        notes_text = self._client.service.GetIncidentCustomerNotes(incident, 0)
        # Get reporter email address
        xml_string = suds.sax.text.Raw("<ns0:IncidentId>" + str(incident) + "</ns0:IncidentId>")
        incident_info = self._client.service.GetIncidentInfoByIncidentId(xml_string)
        self._logger.debug('Ticket info: %s', incident_info)
        # Decode any HTML Entities characters
        h = HTMLParser.HTMLParser()
        notes_text = h.unescape(notes_text)
        # Remove any HTML markup
        p = re.compile(r'<.*?>')
        notes_text = p.sub('', notes_text)
        return incident_info, notes_text
