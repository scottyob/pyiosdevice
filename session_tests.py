"""
IOSDevice Tests

"""
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
path = os.path.abspath(os.path.join(os.path.dirname(__file__)))


try:
    import unittest2 as unittest
except ImportError:
    import unittest

from iosdevice import IOSDevice

class SessionTests(unittest.TestCase):
    
    DATA_DIR = '/tmp/configs/'
    
    def setUp(self):
        pass
        
class TestClasses(SessionTests):
    def test_loading(self):
        for file in os.listdir(self.DATA_DIR):
            print file
            dev = IOSDevice(self.DATA_DIR + file)
            for interface in dev.interfaces:
                for secondary_address in interface.secondary:
                   print secondary_address.network
                print interface.network
            
if __name__ == '__main__':
    unittest.main()
