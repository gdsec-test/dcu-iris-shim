import HTMLParser
import logging
import os
import re
from datetime import datetime, timedelta

import pyodbc
import suds
import suds.client

from iris_shim.models import Report
from settings import config_by_name

app_settings = config_by_name[os.getenv('sysenv', 'dev')]()


class IrisDB:
    _service_id_mappings = {app_settings.IRIS_SERVICE_ID_PHISHING: 'PHISHING',
                            app_settings.IRIS_SERVICE_ID_MALWARE: 'MALWARE',
                            app_settings.IRIS_SERVICE_ID_NETWORK_ABUSE: 'NETWORK_ABUSE'}
    _connection_string = 'DRIVER=FreeTDS;SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password};TDS_VERSION=8.0'

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
        modify_time = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
        query = "SELECT iris_incidentID, iris_serviceID, OriginalEmailAddress, ModifyDate " \
                "FROM IRISIncidentMain WHERE iris_groupID = '{group_id}' AND (iris_serviceID = '{service_id}') " \
                "AND (SPAM = 'False') AND iris_statusID = 1 AND ModifyDate < '{time}'".format(group_id=group_id,
                                                                                              service_id=service_id,
                                                                                              time=modify_time)
        return self._rows(query)

    def get_phishing_reports(self, hours=1):
        """
        Retrieves all Phishing specific incidents from Iris for a given time frame
        :param hours: The number of hours to look back in time since now
        """
        return [] if hours < 0 else self._get_reports(app_settings.IRIS_GROUP_ID_CSA,
                                                      app_settings.IRIS_SERVICE_ID_PHISHING, hours)

    def get_network_abuse_reports(self, hours=1):
        """
        Retrieves all Network Abuse specific incidents from Iris for a given time frame
        :param hours: The number of hours to look back in time since now
        """
        return [] if hours < 0 else self._get_reports(app_settings.IRIS_GROUP_ID_CSA,
                                                      app_settings.IRIS_SERVICE_ID_NETWORK_ABUSE, hours)

    def get_malware_reports(self, hours=1):
        """
        Retrieves all Malware specific incidents from Iris for a given time frame
        :param hours: The number of hours to look back in time since now
        """
        return [] if hours < 0 else self._get_reports(app_settings.IRIS_GROUP_ID_CSA,
                                                      app_settings.IRIS_SERVICE_ID_MALWARE, hours)


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

        Please note: this method does not return the expected iris message body when used in the Dev environment
        """
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

        Example return:
            ((IncidentInfo){
               SubscriberId = 106
               Source = 4
               IncidentType = 1
               PriorityId = 3
               ServiceId = 212
               GroupId = 510
               Category = 0
               PrivateLabelId = 1
               NoteType = 0
               Action = 1
               Visibility = 2
               Protection = 0
               ShopperValidate = 1
               Active = False
               ShopperId = "-1"
               ToEmailAddress = "paddy@justsomeemail.com"
               Subject = "testing create"
               IncidentId = 1355054
               CompanyId = 1
               EmployeeId = 15550
               StatusId = 0
            }
        """
        try:
            xml_string = suds.sax.text.Raw("<ns0:IncidentId>" + str(report_id) + "</ns0:IncidentId>")
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
            self._client.service.AddIncidentNote(report_id, note, 'phishtory')
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
            self._logger.info('Unable to close report an invalid ReportID was provided')
            return

        if note not in self.approved_notes:
            self._logger.info('Unable to close report {} with unsupported note {}'.format(report_id, note))
            return

        self._add_note_to_report(report_id, note)
        self._close_report(report_id)
