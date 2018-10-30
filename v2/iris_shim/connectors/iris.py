import HTMLParser
import logging
import re
from datetime import datetime, timedelta

import pyodbc
import suds
import suds.client

from v2.iris_shim.models import Report


class IrisDB:
    _service_id_mappings = {226: 'PHISHING', 225: 'MALWARE', 232: 'NETWORK_ABUSE'}
    _connection_string = 'DRIVER={FreeTDS};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password};TDS_VERSION=8.0'

    def __init__(self, server, port, database, username, password):
        self._logger = logging.getLogger(__name__)
        self._database_url = self._connection_string.format(server=server, port=port, database=database,
                                                            username=username, password=password)

    def _rows(self, query, size=500):
        """
        Initializes a cursor and communicates with the Iris backend for a given query limited by size.
        :param query: The query to execute on the initialized cursor
        :param size: Integer representing the number of results to return in the cursor
        """
        try:
            connection = pyodbc.connect(self._database_url)
            connection.autocommit = True
            connection.timeout = 0
            cursor = connection.cursor()
            cursor.execute(query)
            while True:
                data = cursor.fetchmany(size)
                if not data:
                    break
                else:
                    for report_id, report_type, reporter_email, modify_date in data:
                        yield Report(report_id, self._service_id_mappings.get(report_type), reporter_email, modify_date)
        except Exception as e:
            self._logger.error('Error processing query {} {}'.format(query, e.message))

    def _get_reports(self, group_id, service_id, hours):
        """
        Constructs a common query for interacting with the Iris backend. Callers should provide the group_id and corresponding service_id.
        :param group_id: The Iris GroupID (Integer)
        :param service_id: The corresponding Iris Service ID (Integer) for services such as phishing, malware, etc.
        :param hours: The number of hours to look back in time since now
        """
        modify_time = (datetime.now() - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
        query = 'SELECT iris_incidentID, iris_serviceID, OriginalEmailAddress, ModifyDate ' \
                'FROM IRISIncidentMain WHERE iris_groupID = "{group_id}" AND (iris_serviceID = "{service_id}") ' \
                'AND (SPAM = "False") AND iris_statusID = 1 AND ModifyDate < "{time}"'.format(group_id=group_id,
                                                                                              service_id=service_id,
                                                                                              time=modify_time)
        return self._rows(query)

    def get_phishing_reports(self, hours=1):
        """
        Retrieves all Phishing specific incidents from Iris for a given time frame
        :param hours: The number of hours to look back in time since now
        """
        # TODO abstract group_id and service_id into some non-magic number variable/structure
        return [] if hours < 0 else self._get_reports(443, 226, hours)

    def get_network_abuse_reports(self, hours=1):
        """
        Retrieves all Network Abuse specific incidents from Iris for a given time frame
        :param hours: The number of hours to look back in time since now
        """
        # TODO abstract group_id and service_id into some non-magic number variable/structure
        return [] if hours < 0 else self._get_reports(443, 232, hours)

    def get_malware_reports(self, hours=1):
        """
        Retrieves all Malware specific incidents from Iris for a given time frame
        :param hours: The number of hours to look back in time since now
        """
        # TODO abstract group_id and service_id into some non-magic number variable/structure
        return [] if hours < 0 else self._get_reports(443, 225, hours)


class IrisSoap:
    _new_abuse_reports = 'New GoDaddy abuse reports should be submitted via https://supportcenter.godaddy.com/AbuseReport'

    note_successfully_parsed = 'Do not re-open this incident.\n' \
                               'This report has been successfully parsed by our Digital Crimes Unit and will be processed as soon as possible.\n' \
                               'If you have questions please contact us in Slack (#dcueng). ' + _new_abuse_reports

    note_failed_to_parse = 'Do not re-open this incident.\n' \
                           'Our Digital Crimes Unit was not able to automatically determine any valid sources of abuse and have notified the reporter.\n' \
                           'If you believe this ticket has been closed in error please contact us in Slack (#dcueng). ' + _new_abuse_reports

    approved_notes = [note_successfully_parsed, note_failed_to_parse]

    def __init__(self, wsdl_url):
        self._logger = logging.getLogger(__name__)
        self._client = suds.client.Client(wsdl_url)

    def get_customer_notes(self, report_id):
        """
        Utilizes the GetIncidentCustomerNotes endpoint to retrieve the body of the email.
        :param report_id: The Iris Report ID to retrieve the customer notes from.
        """
        # TODO revisit this logic and see if it can be simplified. Add Exception logic.
        notes_text = self._client.service.GetIncidentCustomerNotes(report_id, 0)
        h = HTMLParser.HTMLParser()
        notes_text = h.unescape(notes_text)
        # Remove any HTML markup
        p = re.compile(r'<.*?>')
        return p.sub(' ', notes_text)

    def get_report_info_by_id(self, report_id):
        """
        Utilizes the GetIncidentInfoByIncidentId endpoint to retrieve the email subject and other information.
        :param report_id: The Iris Report ID to retrieve the incident information from.
        """
        try:
            xml_string = suds.sax.text.Raw("<ns0:IncidentId>" + str(report_id) +
                                           "</ns0:IncidentId>")
            return self._client.service.GetIncidentInfoByIncidentId(xml_string)
        except Exception as e:
            self._logger.error('Unable to retrieve Incident Info for report {} {}'.format(report_id, e.message))

    def _add_note_to_report(self, report_id, note):
        """
        Utilizes the AddIncidentNote endpoint to add a customer note to the provided report_id.
        :param report_id: The Iris Report ID to add the customer note to.
        :param note: The message to leave in the customer notes.
        """
        try:
            self._client.service.AddIncidentNote(report_id, note, 'phishstory')
        except Exception as e:
            self._logger.error('Unable to notate report {} {}'.format(report_id, e.message))

    def _close_report(self, report_id):
        """
        Utilizes the QuickCloseIncident endpoint to close the provided report_id
        :param report_id: The Iris Report ID to close.
        """
        try:
            self._client.service.QuickCloseIncident(int(report_id), 15550, )
        except Exception as e:
            self._logger.error('Unable to close report {} {}'.format(report_id, e.message))

    def notate_report_and_close(self, report_id, note):
        """
        Notates the provided report_id with note and then closes the incident as the Phishstory User.
        """
        if not report_id:
            self._logger.info('Unable to close report: Invalid ReportID provided')
            return

        if note not in self.approved_notes:
            self._logger.info('Unable to close report {} with unsupported note {}'.format(report_id, note))
            return

        self._add_note_to_report(report_id, note)
        self._close_report(report_id)
