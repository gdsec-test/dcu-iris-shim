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
            query = "select iris_incidentID, iris_serviceID, OriginalEmailAddress " \
                    "from IRISIncidentMain where iris_groupID = '443' And (iris_serviceID = '226' " \
                    "Or iris_serviceID = '236') and (SPAM = 'False') and iris_statusID = 1 "
            if x_hours > 0:
                    query += "and CreateDate " + logical + " \'%s\'" % (datetime.utcnow() - timedelta(hours=x_hours)).strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(query)  # DB query goes here
            incidents = QueryIris.rows(cursor)
        except Exception as e:
            self._logger.error("Unable to run query {}".format(e))
        finally:
            return incidents


