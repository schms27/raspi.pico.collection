import unittest
from unittest.mock import patch
from macro_enums import Order
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
        self.layout_manager.swapLayout("BACKWARD")
        self.assertEqual(self.layout_manager.currentLayoutIndex, 0)

    def test_get_action(self):
        action = self.layout_manager.getAction(1, Order.SHORT_PRESSED)
        self.assertIsNotNone(action)
        self.assertEqual(action['type'], 'SOUND_MIXER')
       
if __name__ == '__main__':
    unittest.main()