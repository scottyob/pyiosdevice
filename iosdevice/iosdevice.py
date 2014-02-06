from corelibs import _get_net_size_for_tuple, _get_cidr
from interface import NetworkInterface
from secondaryaddress import SecondaryAddress
from ciscoconfparse import CiscoConfParse
from ipaddress import IPv4Address

class IOSDevice:
    """
    Represents an IOS Device.  Some helper functions here to assist with common stuff
    """

    def __init__(self, config_filename):
        self.parsed_switch_config = CiscoConfParse(config_filename)
        self.hostname = self._getHostname()
        self.interfaces = self._getNetworkInterfaces()
        self.router_id = self._getRouterId()

    def __repr__(self):
        return "<IOSDevice: %s>" % self.hostname
        
    def _getHostname(self):
        if not self.parsed_switch_config.find_lines('^hostname'):
            raise RuntimeError('This device has no hostname.  This library requires this device has a hostname')
        return self.parsed_switch_config.find_lines('^hostname')[0].split()[1]

    def _getRouterId(self):
        router_id = None
        router_ids = self.parsed_switch_config.find_lines('router-id')
        if len(router_ids) > 0:
            router_id = self.parsed_switch_config.find_lines('router-id')[0].split()[-1] #Assume all mgmt addresses are the same
        else:
            #There is no explicit mgmt address.
            # The router-id is set by the highest IP Address of a manually created loopback address
            highestAddress = IPv4Address(u'0.0.0.0')
            for interface in self.getNetworkInterfaces():
                if "loopback" in interface.name.lower():
                    address = IPv4Address(unicode(interface.address))
                    if address > highestAddress:
                        highestAddress = address
                        router_id = interface.address

            # If there is no configured loopback the router id will be the highest IP address of the fist active (on-boot)
            # physical interface
            if router_id is None:
                for interface in self.getNetworkInterfaces():
                    address = IPv4Address(unicode(interface.address))
                    if address > highestAddress:
                        highestAddress = address
                        router_id = interface.address
        return router_id

    def _getNetworkInterfaces(self):
        """
        Used to generate a list of NetworkInterface for a given config file
    
        :type parsed_switch_config: ciscoconfparse.CiscoConfParse
        :return list of interfaces
        """
        
        to_return = []
        
    
        switch_interfaces = self.parsed_switch_config.find_parents_wo_child("^interface", 'shutdown')
        for interface in switch_interfaces:
            #Gets the child config for this interface
            interface_config = CiscoConfParse(self.parsed_switch_config.find_children(interface, exactmatch=True))
            
            #We are only interested in the interface name, not the entire interface command definition
            interface_name = interface.split()[1]
            
            #VRF is in global by default
            vrf = 'GLOBAL'
            
            if interface_config.find_lines('^ ip vrf forwarding'):
                vrf = interface_config.find_lines('^ ip vrf forwarding')[0].strip().split()[-1]
            elif interface_config.find_lines('^ vrf forwarding'):
                vrf = interface_config.find_lines('^ vrf forwarding')[0].strip().split()[-1]
            
            #We only really care about this interface if it has an IP address on it
            #interfaces that have no addresses should be skipped
            if interface_config.find_lines('no ip address'):
                continue
    
            if interface_config.find_lines('^ ip address'):
                #Create a new network interface object
                interface = NetworkInterface(self)
    
                #In case we want to skip this interface and not show it for some reason
                should_add_address = True
                
                for address in interface_config.find_lines('^ ip address'):
                    #We can have multiple addresses here, have to allow for secondaries
                    if "secondary" in address:
                        secondary_address = SecondaryAddress()
                        secondary_address.address = address.strip().split('ip address')[1].split()[0]
                        secondary_address.netmask = address.strip().split('ip address')[1].split()[1]
                        interface.secondary.append(secondary_address)
                    else:
    
                        if "no" in address or "negotiated" in address:
                            should_add_address = False
                            break
                        if len(interface_config.find_lines('channel-group')) > 0:
                            should_add_address = False
                            break
    
                        interface.address = address.strip().split('ip address')[1].split()[0]
                        interface.name = interface_name
                        interface.netmask = address.strip().split('ip address')[1].split()[1]
                        interface.vrf = vrf
                        to_return.append(interface)
        return to_return

    def getNetworkInterfaces(self):
        """
        Used to generate a list of NetworkInterface for a given config file
    
        :type parsed_switch_config: ciscoconfparse.CiscoConfParse
        :return list of interfaces
        """
        if self.interfaces is None:
            self.interfaces = self._getNetworkInterfaces()
        return self.interfaces
