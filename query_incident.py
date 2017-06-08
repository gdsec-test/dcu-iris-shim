import HTMLParser
import logging
import re
import suds.client


class QueryIncident:

    def __init__(self, wsdl):
        self._logger = logging.getLogger(__name__)
        self._client = suds.client.Client(wsdl)
        self._closed_tickets = set()

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
        xml_string = suds.sax.text.Raw("<ns0:IncidentId>" + str(incident) +
                                       "</ns0:IncidentId>")
        incident_info = self._client.service.GetIncidentInfoByIncidentId(
            xml_string)
        # self._logger.debug('Ticket info: %s', incident_info)
        # Decode any HTML Entities characters
        h = HTMLParser.HTMLParser()
        notes_text = h.unescape(notes_text)
        # Remove any HTML markup
        p = re.compile(r'<.*?>')
        notes_text = p.sub('', notes_text)
        return incident_info, notes_text

    def close_incident(self, incident):
        try:
            self._client.service.AddIncidentNote(
                incident,
                "This ticket has been closed by DCU-ENG. "
                " If you have any issues or questions please"
                " contact a member of the Digital Crimes Unit Engineers via"
                " Lync/Slack or email dcu@", 'phishtory')
                # NTLogin was misspelled when added to IRIS, above mispelling is intentional due to that
            self._client.service.QuickCloseIncident(
                int(incident),
                15550,)
            self._logger.info("%s closed successfully", incident)
        except Exception as e:
            self._logger.error("Auto Close failed on IID: %s, %s", incident, e)
