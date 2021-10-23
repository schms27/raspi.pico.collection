import unittest
import win32api
from pynput import keyboard
import time

from input_manager import InputManager

class TestInputManager(unittest.TestCase):
    def setUp(self):
        self.input_manager = InputManager()
        self.last_pressed_keys = []

    def test_set_mouse_position(self):
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1) 

        self.assertEqual(screen_width, self.input_manager.screen_width, 'screen size was not set correctly')
        self.assertEqual(screen_height, self.input_manager.screen_height, 'screen size was not set correctly')

        screenCorners = [(50,50), (screen_width-50, 50), (screen_width-50, screen_height-50), (50, screen_height -50)]
        for corner in screenCorners:
            self.input_manager.moveMouseTo(corner[0], corner[1])
            self.assertEqual(self.input_manager.mouse.position, (corner[0], corner[1]), 'mouse was not moved as expected')

    def test_generate_random_coordinates(self):
        mouse_movements = self.input_manager.getNextMouseMovements()
        self.assertGreater(len(mouse_movements), 0)

    def test_paste(self):
        # Collect events until released
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()  # start to listen on a separate thread

        self.input_manager.clear_clipboard()
        self.input_manager.sendPaste()

        time.sleep(1)
        self.assertTrue(self.last_pressed_keys[0].name == "ctrl_l")
        self.assertTrue(chr(self.last_pressed_keys[1].vk) == 'V')

    def on_press(self, key):
        self.last_pressed_keys.append(key)

    def on_release(self, key):
        print('Key released: {0}'.format(
            key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

if __name__ == '__main__':
    unittest.main()