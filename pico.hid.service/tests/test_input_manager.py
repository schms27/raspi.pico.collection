import unittest
import win32api
import time

from input_manager import InputManager

class TestInputManager(unittest.TestCase):
    def setUp(self):
        self.input_manager = InputManager()

    def test_set_mouse_position(self):
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1) 

        self.assertEqual(screen_width, self.input_manager.screen_width, 'screen size was not set correctly')
        self.assertEqual(screen_height, self.input_manager.screen_height, 'screen size was not set correctly')

        screenCorners = [(50,50), (screen_width-50, 50), (screen_width-50, screen_height-50), (50, screen_height -50)]
        for corner in screenCorners:
            self.input_manager.moveMouseTo(corner[0], corner[1])
            self.assertEqual(self.input_manager.mouse.position, (corner[0], corner[1]), 'mouse was not moved as expected')


if __name__ == '__main__':
    unittest.main()