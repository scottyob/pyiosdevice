from corelibs import _get_net_size_for_tuple, _get_cidr

class NetworkInterface:
    """
    Represents a network interface
    """

    def __init__(self, parent_device, name=None, address=None, netmask=None, vrf=None, secondary=[]):
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
        self.secondary = secondary
        self.parent_device = parent_device

    @property
    def cidr(self):
        return "%s/%s" % (self.address, _get_cidr(self.netmask) )

    def getRecommendedDnsEntry(self, append_domain_name=""):
        """
        Used to get a list of recommended DNS entries for all interfaces.  This will use the hostname in the config file
        but overwrite the domain-name with what's passed in

        :property domain-name: str
        """
        to_return = None
        if self.address == self.parent_device.router_id:
            to_return = self.parent_device.hostname + append_domain_name
        else:
            to_return = "%s-%s" % (self.parent_device.hostname, self.name.replace("/", "_").replace(".", "_") )
            if self.vrf != 'GLOBAL':
                to_return += "-%s" % self.vrf

        return to_return

    def __unicode__(self):
        return u'%s %s' % (self.address, self.netmask)

    def __str__(self):
        return str(self.__unicode__())

    def __repr__(self):
        return u'<NetworkInterface: %s(%s)>' % (self.name, self.__unicode__())
