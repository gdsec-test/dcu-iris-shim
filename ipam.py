#!/usr/bin/python2.6
# This file contains a Python class for working with our IPAM service.
# Author: Kyle Barnes
# Version: 1.0
# Date Created: 05/14/2014
import json
import logging
import re
from suds import WebFault
from suds.client import Client
import ssl
from suds.transport.https import WindowsHttpAuthenticated
from urllib2 import URLError
import os


# This class calls into the IPAM SOAP Service to retrieve and modify IP data.
class Ipam:
    # Local Suds SOAP client.
    client = None

    # dev, test, or prod.
    environment = os.getenv('sysenv') or 'dev'

    # SMDB credentials.
    smdbUsername = None
    smdbPassword = None

    # Environment specific SMDB IPAM SOAP API URL's.
    smdbUrls = {
        'dev': 'https://smdb.int.dev-godaddy.com/IPService/ipam.asmx?WSDL',
        'test': 'http://smdb.int.test-godaddy.com/IPService/ipam.asmx?WSDL',
        'prod': 'https://smdb.int.godaddy.com/IPService/ipam.asmx?WSDL'
    }

    if environment != 'prod' and hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    # This method is called automatically when this class is instantiated.
    def __init__(self):

        # Load the SMDB credentials from Nimitz.
        self.__load_credentials()

        # Create the NTLM authentication object.
        self.ntlm = WindowsHttpAuthenticated(
            username=self.smdbUsername, password=self.smdbPassword)

        # Create the SUDS SOAP client.
        self.client = Client(
            self.smdbUrls[self.environment], transport=self.ntlm)

    # Convert the string "true" and "false" to boolean.
    def __get_boolean(self, obj):
        # Make sure the object is a string.
        if isinstance(obj, basestring):
            if obj.lower() == 'false':
                return False
            elif obj.lower() == 'true':
                return True

        raise Exception('Could not determine boolean value: %s' % obj)

    # Get a list of IP addresses from an object. This is specific to the IPAM IP SOAP response.
    def __get_ips(self, obj):
        # Default to empty list.
        ips = []

        # Make sure the object is a list, and contains a 'IPAddress' key.
        if obj is not None and hasattr(obj, '__iter__') and 'IPAddress' in obj:
            # If the object is a list already, just return it.
            if isinstance(obj['IPAddress'], list):
                ips = obj['IPAddress']
            # If the object is a dictionary, cast as a list.
            elif isinstance(obj['IPAddress'], dict):
                ips.append(obj['IPAddress'])

        return ips

    # Get a list of networks from an object. This is specific to the IPAM Network SOAP response.
    def __get_networks(self, obj):
        # Default to empty list.
        ips = []

        # Make sure the object is a list, and contains a 'Network' key.
        if obj is not None and hasattr(obj, '__iter__') and 'Network' in obj:
            # If the object is a list already, just return it.
            if isinstance(obj['Network'], list):
                ips = obj['Network']
            # If the object is a dictionary, cast as a list.
            elif isinstance(obj['Network'], dict):
                ips.append(obj['Network'])

        return ips

    # Get a list of pool names.
    def __get_pools(self, obj):
        # Default to empty list.
        pools = []

        # Make sure the object is a list, and contains a 'PoolName' key.
        if obj is not None and hasattr(obj, '__iter__') and 'PoolName' in obj:
            for pool in obj['PoolName']:
                if 'Name' in pool and pool['Name'] is not None:
                    pools.append(pool['Name'])

        return pools

    # Load the SMDB credentials from Nimitz.
    def __load_credentials(self):
        self.smdbUsername = os.getenv('SMDB_USERNAME')
        self.smdbPassword = os.getenv('SMDB_PASSWORD')

    # Perform a SOAP call, and parse the results.
    def __soap_call(self, method, params, responseKey):
        # We need the params to be a tuple for Suds. So if it's a single element, cast as a tuple.
        if not isinstance(params, tuple):
            params = (params,)

        # Try and make the SOAP call, and return the results. Or throw an exception on any SOAP faults.
        try:
            # Dynamically make SOAP call.
            soapResult = getattr(self.client.service, method)(*params)

            # Manually parse the SOAP XML response.
            return soapResult
        except (WebFault, URLError) as e:
            try:
                raise Exception("IPAM SOAP Fault: %s" % e.fault.faultstring)
            except AttributeError as e2:
                raise Exception("IPAM SOAP Attribute Fault: %s" % str(e2))

    # Make sure all method parameters were supplied. The only exception is 'vlan', which is optional.
    def __validate_params(self, params):
        for key, val in params.iteritems():
            if val is None and key != 'vlan':
                raise Exception('Missing parameter %s' % key)

    # Get the environment we're running under.
    def get_environment(self):
        return self.environment

    # SOAP METHODS

    # Allocate a specific IP address to a hostname. Returns a boolean.
    def allocate_ip(self, ip, hostname):
        self.__validate_params(locals())
        return self.__get_boolean(
            self.__soap_call('AllocateIP', (ip, hostname), 'AllocateIPResult'))

    # Allocate a random IPv4 address from a pool to a hostname. Returns a list.
    def allocate_ip_by_attribute(self, hostname, attribute_name,
                                 attribute_value, quantity):
        self.__validate_params(locals())
        return self.__get_ips(
            self.__soap_call('AllocateIPByAttribute', (
                hostname, attribute_name, attribute_value, quantity),
                             'AllocateIPByAttributeResult'))

    # Allocate a random IPv6 address from a pool to a hostname. Returns a list.
    def allocate_ipv6_by_attribute(self, hostname, attribute_name,
                                   attribute_value, quantity, vlan):
        self.__validate_params(locals())
        return self.__get_ips(
            self.__soap_call('AllocateIPv6ByAttribute', (
                hostname, attribute_name, attribute_value, quantity, vlan),
                             'AllocateIPv6ByAttributeResult'))

    # Assign an IPv6 network block to one specific hostname. This has not been tested.
    def allocate_ipv6_network_by_attribute(self, reserved_name, attribute_name,
                                           attribute_value):
        self.__validate_params(locals())
        return self.__soap_call('AllocateIPv6NetworkByAttribute', (
            reserved_name, attribute_name, attribute_value),
                                'AllocateIPv6NetworkByAttributeResult')

    # Assign an IPv4 network block to one specific hostname. This has not been tested.
    def allocate_network_by_attribute(self, reserved_name, attribute_name,
                                      attribute_value):
        self.__validate_params(locals())
        return self.__soap_call('AllocateNetworkByAttribute', (
            reserved_name, attribute_name, attribute_value),
                                'AllocateNetworkByAttributeResult')

    # Allocate sequential IP addresses from a pool to a hostname. Returns a list.
    def allocate_sequential_ips_by_attribute(self, hostname, attribute_name,
                                             attribute_value, quantity, vlan):
        self.__validate_params(locals())
        return self.__get_ips(
            self.__soap_call('AllocateSequentialIPsByAttribute', (
                hostname, attribute_name, attribute_value, quantity, vlan),
                             'AllocateSequentialIPsByAttributeResult'))

    # Create a new IP pool by name. Returns a boolean.
    def create_pool(self, pool_name):
        self.__validate_params(locals())
        return self.__get_boolean(
            self.__soap_call('CreatePool', pool_name, 'CreatePoolResult'))

    # De-Allocate a specific IP address. Returns a boolean.
    def de_allocate_ip(self, ip):
        self.__validate_params(locals())
        return self.__get_boolean(
            self.__soap_call('DeAllocateIP', ip, 'DeAllocateIPResult'))

    # Get details for a specific IP address. Returns a dictionary.
    def get_gateway_by_ip(self, ip):
        self.__validate_params(locals())
        return self.__soap_call('GetGatewayByIP', ip, 'GetGatewayByIPResult')

    # Get IP's assigned to a specific IP pool. Returns a list
    def get_ips_by_attribute(self, attribute_name, attribute_value, quantity,
                             include_allocated):
        self.__validate_params(locals())
        return self.__get_ips(
            self.__soap_call('GetIPsByAttribute', (
                attribute_name, attribute_value, quantity, include_allocated),
                             'GetIPsByAttributeResult'))

    # Get IP's assigned to a specific hostname. Returns a list.
    def get_ips_by_hostname(self, hostname):
        self.__validate_params(locals())
        return self.__get_ips(
            self.__soap_call('GetIPsByHostname', hostname,
                             'GetIPsByHostnameResult'))

    # Get a network block details assigned to one specific hostname. This has not been tested.
    def get_network_by_reserved_name(self, reserved_name):
        self.__validate_params(locals())
        return self.__get_networks(
            self.__soap_call('GetNetworkByReservedName', reserved_name,
                             'GetNetworkByReservedNameResult'))

    # Get networks assigned to a specific IP pool or attribute.
    def get_networks_by_attribute(self, attribute_name, attribute_value,
                                  quantity, include_allocated):
        self.__validate_params(locals())
        return self.__get_networks(
            self.__soap_call('GetNetworksByAttribute', (
                attribute_name, attribute_value, quantity, include_allocated),
                             'GetNetworksByAttributeResult'))

    # Get details for a specific IP address. Returns a dictionary.
    def get_properties_for_ip(self, ip):
        self.__validate_params(locals())
        return self.client.service.GetPropertiesForIP(ip, transport=self.ntlm)
        # return self.__soap_call('GetPropertiesForIP', ip, 'GetPropertiesForIPResult')

    # Get details for multiple IP addresses. Returns a list.

    def get_properties_for_ip_list(self, ips):
        self.__validate_params(locals())
        return self.__get_ips(
            self.__soap_call('GetPropertiesForIPList', ips,
                             'GetPropertiesForIPListResult'))

    # Checks whether a specific IP address is restricted. Returns a boolean.

    def is_ip_restricted(self, ip):
        self.__validate_params(locals())
        return self.__get_boolean(
            self.__soap_call('isIPRestricted', ip, 'isIPRestrictedResult'))

    # Get existing IP pool names. Returns a list.
    def list_pools(self):
        return self.__get_pools(
            self.__soap_call('ListPools', None, 'ListPoolsResult'))

    # Set an attribute, such as the IP pool, on a list of IP's. Returns a boolean.
    def set_attribute_for_ip_list(self, ips, attribute_name, attribute_value):
        self.__validate_params(locals())
        return self.__get_boolean(
            self.__soap_call('SetAttributeForIPList', (ips, attribute_name,
                                                       attribute_value),
                             'SetAttributeForIPListResult'))

    # Set an attribute, such as the IP pool, on a specific IP. Returns a boolean.
    def set_ip_attribute(self, ip, attribute_name, attribute_value):
        self.__validate_params(locals())
        return self.__get_boolean(
            self.__soap_call('SetIPAttribute', (
                ip, attribute_name, attribute_value), 'SetIPAttributeResult'))
