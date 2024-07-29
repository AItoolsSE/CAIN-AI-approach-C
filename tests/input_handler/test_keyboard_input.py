# tests/input_handler/test_keyboard_input.py

import unittest
import pygame
from input_handler.keyboard_input import KeyboardInput
from unittest.mock import patch

class TestKeyboardInput(unittest.TestCase):
    def setUp(self):
        self.keyboard_input = KeyboardInput()

    @patch('pygame.event.get')
    def test_process_input_move_left(self, mock_pygame_event_get):
        mock_pygame_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)]
        self.keyboard_input.handle_events()
        self.assertTrue(self.keyboard_input.is_key_pressed('left'))

    @patch('pygame.event.get')
    def test_process_input_move_right(self, mock_pygame_event_get):
        mock_pygame_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)]
        self.keyboard_input.handle_events()
        self.assertTrue(self.keyboard_input.is_key_pressed('right'))

    @patch('pygame.event.get')
    def test_process_input_move_down(self, mock_pygame_event_get):
        mock_pygame_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)]
        self.keyboard_input.handle_events()
        self.assertTrue(self.keyboard_input.is_key_pressed('down'))

    @patch('pygame.event.get')
    def test_process_input_rotate(self, mock_pygame_event_get):
        mock_pygame_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)]
        self.keyboard_input.handle_events()
        self.assertTrue(self.keyboard_input.is_key_pressed('rotate'))

    @patch('pygame.event.get')
    def test_process_input_drop(self, mock_pygame_event_get):
        mock_pygame_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]
        self.keyboard_input.handle_events()
        self.assertTrue(self.keyboard_input.is_key_pressed('drop'))

    @patch('pygame.event.get')
    def test_process_input_quit(self, mock_pygame_event_get):
        mock_pygame_event_get.return_value = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)]
        self.keyboard_input.handle_events()
        self.assertFalse(self.keyboard_input.is_key_pressed('quit'))

if __name__ == '__main__':
    unittest.main()
