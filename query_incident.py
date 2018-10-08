import HTMLParser
import logging
import re
import suds.client


class QueryIncident:

    duplicate_report = 'an identical url/ip being reported'
    no_parsed_ips = 'no parsable ips'
    no_parsed_urls = 'no parsable urls'

    reason_msg = 'This ticket has been closed by Digital Crimes Unit (DCU) for {}. Do not re-open the ticket without ' \
                 'first contacting DCU. If you have any issues or questions, please contact us via our Slack channel,' \
                 ' #duceng. Abuse reports should be submitted using the following abuse form: ' \
                 'https://supportcenter.godaddy.com/AbuseReport'
    standard_msg = 'This ticket has been closed by Digital Crimes Unit (DCU). Do not re-open the ticket without first' \
                   ' contacting DCU. If you have any issues or questions, please contact us via our Slack channel, ' \
                   '#duceng. Abuse reports should be submitted using the following abuse form: ' \
                   'https://supportcenter.godaddy.com/AbuseReport'

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
        notes_text = p.sub(' ', notes_text)
        return incident_info, notes_text

    def close_incident(self, incident, reason=None):
        if incident not in self._closed_tickets:
            try:
                if reason:
                    self._client.service.AddIncidentNote(
                        incident,
                        self.reason_msg.format(reason), 'phishtory')
                else:
                    self._client.service.AddIncidentNote(
                        incident,
                        self.standard_msg, 'phishtory')
                self._client.service.QuickCloseIncident(
                    int(incident),
                    15550,)
                self._logger.info("%s closed successfully", incident)
                self._closed_tickets.add(incident)
            except Exception as e:
                self._logger.error("Auto Close failed on IID: %s, %s", incident, e)
