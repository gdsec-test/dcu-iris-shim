import os
import sys
import yaml
import logging

from datetime import datetime
from logging.config import dictConfig
from query_incident import QueryIncident
from query_iris import QueryIris
from match_ip import MatchIP
from itertools import islice
from api_ticket import APITicket
from time import sleep

if __name__ == '__main__':

    # Set up logging
    path = 'logging.yml'
    value = os.getenv('LOG_CFG', None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            lconfig = yaml.safe_load(f.read())
        dictConfig(lconfig)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # sys.exit("This line must be commented out to run program")

    logger.info('Starting BATCH_NETABUSE iris shim: {}'.format(str(datetime.now())))

    ips = MatchIP()
    api = APITicket('prod')
    jwt = 'sso-key {}:{}'.format(os.getenv('key'), os.getenv('secret'))
    iris = QueryIris(
        'DRIVER={FreeTDS};SERVER=10.32.146.30;PORT=1433;DATABASE=iris;UID=N1_mF09EAA138D464E;PWD=bCFF03B5F01D042;TDS_VERSION=8.0'
    )
    ip_dict = dict()
    incident = QueryIncident(
        'https://iris-ws.int.godaddy.com/iriswebservice.asmx?wsdl')
    counter = 1
    seen_tickets = set()
    for iid, rtype, email, create_date in iris.netabuse_query(24, True):
        if counter % 100 == 0:
            sleep(30)
        info, notes = incident.get_incident_info(iid)
        for ip in ips.get_ip(notes):
            item = dict(jwt=jwt, type='NETWORK_ABUSE', url='http://'+ip, iid=iid, email=email, create_date=create_date)
            response = api.post_ticket(item)
            if response is not None:
		logger.info("{} {}".format(response.text, response.status_code))
                if response.status_code == 201 or (
                        response.status_code == 422 and
                        "We have already been informed" in response.text):

                    if iid not in seen_tickets:
                        logger.info('BATCH_NETABUSE Closing incident: {}'.format(iid))
                        incident.close_incident(iid)
                        seen_tickets.add(iid)
        counter += 1

    logger.info('Finishing BATCH_NETABUSE iris shim: {}'.format(str(datetime.now())))
