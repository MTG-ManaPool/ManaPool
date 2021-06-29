import unittest
from unittest.mock import patch
from ui.login import login

class TestLogin(unittest.TestCase):
    
    def testLoginSuccess(self):
        print('\n\n\n***** Testing Successful Login *****\n\n')
        login()


if __name__ == '__main__':
    unittest.main()