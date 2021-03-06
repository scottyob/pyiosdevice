from ipaddress import IPv4Network
from corelibs import _get_net_size_for_tuple, _get_cidr

class SecondaryAddress:
    """
    Represents a secondary address that can exist on an interface
    """
    def __init__(self, parent_address, addr=None, netmask=None):
        """
        Creates a Secondary Address that can exist on an interface
        
        :type addr: str
        :type netmask: str
        """
        self.parent_address = parent_address
        self.address = addr
        self.netmask = netmask

    @property
    def network(self):
        """
        Returns an IPv4Network object for this network interface
        """
        address = unicode("%s/%s" % (self.address, _get_cidr(self.netmask)))
        return IPv4Network(address, strict=False)

    def getRecommendedDnsEntry(self):
        return self.parent_address.getRecommendedDnsEntry()
        
    @property
    def description(self):
        return self.parent_address.description