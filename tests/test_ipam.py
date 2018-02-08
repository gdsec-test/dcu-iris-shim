from nose.tools import assert_true
from mock import patch

from ipam import Ipam
import os
import logging

class TestIpam:

    @classmethod
    def setup(cls):
        cls.ipam = Ipam()