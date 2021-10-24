import unittest
from unittest.mock import patch
from settings import Settings

from layout_manager import LayoutManager

class TestLayoutManager(unittest.TestCase):

    # @patch('layout_manager.LayoutManager')
    def setUp(self): 
        settings = Settings('./pico.hid.service/tests/')
        self.layout_manager = LayoutManager(settings)

    def test_swap_layout(self):
        self.assertEqual(self.layout_manager.currentLayoutIndex, 0)
        self.layout_manager.swapLayout("FORWARD")
        self.assertEqual(self.layout_manager.currentLayoutIndex, 1)
       
if __name__ == '__main__':
    unittest.main()