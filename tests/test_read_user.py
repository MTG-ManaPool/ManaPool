import unittest
from user.user import readUser

class TestLogin(unittest.TestCase):
    
    def testSuccessUserRead(self):
        print('\n\n\n***** Testing Successful Login *****\n\n')
        readUser('../data/users/test_user/user.json')

if __name__ == '__main__':
    unittest.main()