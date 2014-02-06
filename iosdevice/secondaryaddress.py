class SecondaryAddress:
    """
    Represents a secondary address that can exist on an interface
    """
    def __init__(self, addr=None, netmask=None):
        """
        Creates a Secondary Address that can exist on an interface
        
        :type addr: str
        :type netmask: str
        """
        self.address = addr
        self.netmask = netmask
