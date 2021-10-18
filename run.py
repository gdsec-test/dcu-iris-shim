import logging
import os
from logging.config import dictConfig

import yaml

from iris_shim.handlers import CSAM
from settings import config_by_name

app_settings = config_by_name[os.getenv('sysenv', 'dev')]()

path = ''
value = os.getenv('LOG_CFG')
if value:
    path = value
if os.path.exists(path):
    with open(path, 'rt') as f:
        lconfig = yaml.safe_load(f.read())
    dictConfig(lconfig)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    supported_drivers = [CSAM(app_settings)]

    for driver in supported_drivers:
        driver.run()
