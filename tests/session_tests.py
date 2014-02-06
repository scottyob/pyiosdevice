"""
IOSDevice Tests

"""
import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pyiosdevice import IOSDevice

class SessionTests(unittest.TestCase):
    
    DATA_DIR = '/tmp/configs/'
    
    def setUp(self):
        pass
        
class TestClasses(SessionTests):
    def test_loading(self):
        for file in os.listdir(self.DATA_DIR):
            print file
            
if __name__ == '__main__':
    unittest.main()