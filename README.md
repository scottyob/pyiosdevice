pyiosdevice
===========
A (really) simple wrapper around the ios parser that can turn an ios file into a class.


Requirements
------------
- Python 2.7.  Untested on anything else
- Cisco Conf Parse (http://www.pennington.net/py/ciscoconfparse/tutorial.html)
- ipaddress library

Library usage
-------------
e.g.

.. code:: python
    
    from iosdevice import IOSDevice
    
    dev = IOSDevice('/some/config/file')
    for interface in dev.interfaces:
      print "VRF on %s" % str(interface)
      print interface.vrf
    
