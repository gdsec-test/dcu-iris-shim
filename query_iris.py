import pyodbc
import logging
from datetime import datetime, timedelta


class QueryIris:

    def __init__(self, dbstring):
        self._dbstring = dbstring
        self._logger = logging.getLogger(__name__)

    @staticmethod
    def rows(cursor, arraysize=500):
        """
        Generator function to avoid large datasets
        :param cursor:
        :param arraysize:
        :return:
        """
        while True:
            data = cursor.fetchmany(arraysize)
            if not data:
                break
            else:
                for row in data:
                    yield row

    def get_phishing_and_malware(self, x_hours, less_than=False):
        cnxn = pyodbc.connect(self._dbstring)
        cnxn.autocommit = True
        cnxn.timeout = 0
        cursor = cnxn.cursor()
        incidents = []
        logical = '<' if less_than else '>'
        try:
            query = "select iris_incidentID, iris_serviceID, OriginalEmailAddress, ModifyDate " \
                    "from IRISIncidentMain where iris_groupID = '443' And (iris_serviceID = '226' " \
                    "Or iris_serviceID = '225') and (SPAM = 'False') and iris_statusID = 1 "
            if x_hours > 0:
                query += "and ModifyDate " + logical + " \'%s\'" % (datetime.now() - timedelta(hours=x_hours)).strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(query)  # DB query goes here
            incidents = QueryIris.rows(cursor)
        except Exception as e:
            self._logger.error("Unable to run query {}".format(e))
        finally:
            return incidents

    def netabuse_query(self, x_hours, less_than=False):
        # connection to DB server
        cnxn = pyodbc.connect(self._dbstring)
        cnxn.autocommit = True
        cnxn.timeout = 0
        cursor = cnxn.cursor()
        incident_ids = []
        logical = '<' if less_than else '>'
        try:
            query = "SELECT iris_incidentID, iris_serviceID, OriginalEmailAddress, ModifyDate " \
                    " FROM IRISIncidentMain WHERE iris_groupID = '443' and " \
                    "(iris_serviceID = '232') And (SPAM = 'False') And iris_statusID = 1 "
            if x_hours > 0:
                query += "and ModifyDate " + logical + " \'%s\'" % (datetime.now() - timedelta(hours=x_hours)).strftime("%Y-%m-%d %H:%M:%S")
            # open and execute query
            cursor.execute(query) # DB query goes here
            incident_ids = QueryIris.rows(cursor)
        except Exception as e:
            self._logger.error("Unable to query IRIS for netabuse...%s", e.message)
        finally:
            return incident_ids
