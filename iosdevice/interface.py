from corelibs import _get_net_size_for_tuple, _get_cidr
from ipaddress import IPv4Network

class NetworkInterface:
    """
    Represents a network interface
    """

    def __init__(self, parent_device, name=None, address=None, netmask=None, vrf=None, secondary=None, description=None):
        """
        Create a new NetworkInterface

        :type name: str
        :type address: str
        :type netmask: str
        :type cidr: int
        :type vrf: str
        :type secondary: list
        :type parent_device: IOSDevice
        """
        
        self.name = name
        self.address = address
        self.netmask = netmask
        self.vrf = vrf
        if secondary:
            self.secondary = secondary
        else:
            self.secondary = []
        self.parent_device = parent_device
        self.description = description

    @property
    def cidr(self):
        return unicode("%s/%s") % (self.address, _get_cidr(self.netmask) )

    @property
    def network(self):
        """
        Returns an IPv4Network object for this network interface
        """
        return IPv4Network(self.cidr, strict=False)

    def getRecommendedDnsEntry(self, append_domain_name=""):
        """
        Used to get a list of recommended DNS entries for all interfaces.  This will use the hostname in the config file
        but overwrite the domain-name with what's passed in

        :property domain-name: str
        """
        to_return = None
        if self.address == self.parent_device.router_id:
            to_return = self.parent_device.hostname
        else:
            to_return = "%s-%s" % (self.parent_device.hostname, self.name.replace("/", "_").replace(".", "_") )
            if self.vrf:
                to_return += "-%s" % self.vrf

        return unicode(to_return.lower()) + append_domain_name

    def __unicode__(self):
        return u'%s %s' % (self.address, self.netmask)

    def __str__(self):
        return str(self.__unicode__())

    def __repr__(self):
        return u'<NetworkInterface: %s(%s)>' % (self.name, self.__unicode__())
