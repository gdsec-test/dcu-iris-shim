from nose.tools import assert_true, assert_false, assert_equal
from mock import patch

from ipam import Ipam
import os

class TestIpam:

    @classmethod
    def setup(cls):
        os.environ['sysenv'] = 'test'
        #we have to use test here, because dev doesn't work with IPAM
        cls.ipam = Ipam()
    
    def test_get_boolean(self):
        assert_true(self.ipam._Ipam__get_boolean('TRUE'))
        assert_false(self.ipam._Ipam__get_boolean('FALSE'))

    def test_get_ips(self):
        retval = self.ipam._Ipam__get_ips({'IPAddress': {'127.0.0.1': True}})
        assert_equal(retval, [{'127.0.0.1': True}])
        retval = self.ipam._Ipam__get_ips({'IPAddress': ['127.0.0.1']})
        assert_equal(retval, ['127.0.0.1'])

    def test_get_networks(self):
        retval = self.ipam._Ipam__get_networks({'Network': {'127.0.0.0/24': True}})
        assert_equal(retval, [{'127.0.0.0/24': True}])
        retval = self.ipam._Ipam__get_networks({'Network': ['127.0.0.0/24']})
        assert_equal(retval, ['127.0.0.0/24'])
    
    def test_get_pools(self):
        retval = self.ipam._Ipam__get_pools({
            'PoolName': [
                { 'Name': 'firstpool' },
                { 'Name': 'secondpool' }
            ]
        })
        assert_true('firstpool' in retval)
        assert_true('secondpool' in retval)
        assert_false('thirdpool' in retval)