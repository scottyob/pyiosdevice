"""
Core libraries used across this library

"""

def _get_net_size_for_tuple(netmask):
    """
    Returns a cidr subnet length size for a given mask given a tuple.
    """
    
    binary_str = ''
    for octet in netmask:
        binary_str += bin(int(octet))[2:].zfill(8)
    return str(len(binary_str.rstrip('0')))

def _get_cidr(subnet):
    """
    Returns the CIDR subnet length size given a tuple OR string.
    """
    
    if type(subnet) in [unicode, str]:
        return _get_net_size_for_tuple( tuple([ int(i) for i in subnet.split('.') ])  )
    return _get_net_size_for_tuple(subnet)
