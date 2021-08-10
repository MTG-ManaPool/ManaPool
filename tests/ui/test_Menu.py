import sys
sys.path.append('src')
import unittest
from ui.menu import Menu

class TestUI(unittest.TestCase):
    def test_main_menu(self):
        print('Testing main_menu')
        # call asserts to test before/after state.
        # use mocks for parts that you need, but, dont want the test to depend upon

    def test_inventory_menu(self):
        print('Testing inventory_menu')
        # call asserts to test before/after state.
        # use mocks for parts that you need, but, dont want the test to depend upon