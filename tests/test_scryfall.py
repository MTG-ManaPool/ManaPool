import unittest
from unittest.mock import patch
from ..src.scryfall.scryfall import Scryfall

class TestLogin(unittest.TestCase):
    
    def testScryfall(self):
        scryfall = Scryfall()

        print('\n\n\n***** Testing Scryfall Constructor *****\n\n')
        assert(scryfall != None)
    
    def testSetCodeConversion(self, scryfall):
        scryfall.search(['MTG 2012 Core'])
        


if __name__ == '__main__':
    unittest.main()