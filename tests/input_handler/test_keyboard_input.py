# test_keyboard_input.py

import unittest
import pygame
import sys
import os

# Ensure the base directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from input_handler.keyboard_input import KeyboardInput

class TestKeyboardInput(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        pygame.init()
        self.keyboard_input = KeyboardInput()
        self.start_time = pygame.time.get_ticks()
    
    def create_key_event(self, event_type, key):
        """
        Helper method to create a Pygame key event.
        
        Parameters:
            event_type (int): The type of the event (pygame.KEYDOWN or pygame.KEYUP).
            key (int): The key associated with the event.
        
        Returns:
            pygame.event.Event: The created event.
        """
        return pygame.event.Event(event_type, key=key)
    
    def test_handle_keydown_event(self):
        """
        Test handling of KEYDOWN event.
        """
        key_event = self.create_key_event(pygame.KEYDOWN, pygame.K_LEFT)
        self.keyboard_input.handle_events([key_event])
        self.assertIn(pygame.K_LEFT, self.keyboard_input.pressed_keys)
        self.assertEqual(self.keyboard_input.last_press_time['left'], self.start_time)
    
    def test_handle_keyup_event(self):
        """
        Test handling of KEYUP event.
        """
        keydown_event = self.create_key_event(pygame.KEYDOWN, pygame.K_LEFT)
        keyup_event = self.create_key_event(pygame.KEYUP, pygame.K_LEFT)
        self.keyboard_input.handle_events([keydown_event, keyup_event])
        self.assertNotIn(pygame.K_LEFT, self.keyboard_input.pressed_keys)
    
    def test_is_key_pressed_with_cooldown(self):
        """
        Test if a key press is recognized considering the cooldown.
        """
        key_event = self.create_key_event(pygame.KEYDOWN, pygame.K_LEFT)
        self.keyboard_input.handle_events([key_event])
        
        # Simulate waiting for cooldown
        pygame.time.wait(150)
        self.assertTrue(self.keyboard_input.is_key_pressed('left'))
    
    def test_is_key_pressed_without_cooldown(self):
        """
        Test if a key press is not recognized due to cooldown not being over.
        """
        key_event = self.create_key_event(pygame.KEYDOWN, pygame.K_LEFT)
        self.keyboard_input.handle_events([key_event])
        
        # Check immediately without waiting for cooldown
        self.assertFalse(self.keyboard_input.is_key_pressed('left'))
    
    def test_non_existent_action(self):
        """
        Test the response to a non-existent action.
        """
        self.assertFalse(self.keyboard_input.is_key_pressed('non_existent_action'))
    
    def test_multiple_key_presses(self):
        """
        Test handling of multiple simultaneous key presses.
        """
        key_events = [
            self.create_key_event(pygame.KEYDOWN, pygame.K_LEFT),
            self.create_key_event(pygame.KEYDOWN, pygame.K_RIGHT)
        ]
        self.keyboard_input.handle_events(key_events)
        self.assertIn(pygame.K_LEFT, self.keyboard_input.pressed_keys)
        self.assertIn(pygame.K_RIGHT, self.keyboard_input.pressed_keys)
    
    def test_cooldown_accuracy(self):
        """
        Test that a key cannot be pressed again until the cooldown period has passed.
        """
        key_event = self.create_key_event(pygame.KEYDOWN, pygame.K_LEFT)
        self.keyboard_input.handle_events([key_event])
        
        # Simulate waiting for a time shorter than cooldown
        pygame.time.wait(50)
        self.assertFalse(self.keyboard_input.is_key_pressed('left'))

        # Simulate waiting for enough time to pass
        pygame.time.wait(100)
        self.assertTrue(self.keyboard_input.is_key_pressed('left'))
    
    def test_continuous_key_presses(self):
        """
        Test handling of continuous key presses.
        """
        key_event = self.create_key_event(pygame.KEYDOWN, pygame.K_DOWN)
        for _ in range(5):
            self.keyboard_input.handle_events([key_event])
        self.assertIn(pygame.K_DOWN, self.keyboard_input.pressed_keys)
    
    def test_state_persistence(self):
        """
        Test that state is correctly maintained across multiple cycles of event handling.
        """
        key_event = self.create_key_event(pygame.KEYDOWN, pygame.K_UP)
        self.keyboard_input.handle_events([key_event])
        self.assertIn(pygame.K_UP, self.keyboard_input.pressed_keys)

        # Simulate another event cycle
        self.keyboard_input.handle_events([self.create_key_event(pygame.KEYUP, pygame.K_UP)])
        self.assertNotIn(pygame.K_UP, self.keyboard_input.pressed_keys)
    
    def test_rapid_key_presses(self):
        """
        Test handling of very rapid key presses.
        """
        key_events = [self.create_key_event(pygame.KEYDOWN, pygame.K_SPACE)] * 10
        self.keyboard_input.handle_events(key_events)
        self.assertIn(pygame.K_SPACE, self.keyboard_input.pressed_keys)

    def tearDown(self):
        """
        Clean up after the tests.
        """
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
