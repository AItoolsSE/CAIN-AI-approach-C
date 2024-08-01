# input_handler/keyboard_input.py

import pygame

class KeyboardInput:
    def __init__(self):
        """
        Initialize the KeyboardInput class and set up key mappings.
        """
        pygame.init()  # Initialize Pygame
        self.keys = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'down': pygame.K_DOWN,
            'rotate': pygame.K_UP,
            'drop': pygame.K_SPACE
        }
        self.pressed_keys = set()  # Set to keep track of pressed keys
        self.last_action_time = {
            'left': 0,
            'right': 0,
            'down': 0,
            'rotate': 0,
            'drop': 0
        }
        self.cooldown = {
            'left': 200,  # Cooldown in milliseconds
            'right': 200,
            'down': 100,
            'rotate': 300,
            'drop': 500
        }

    def handle_event(self, event):
        """
        Handle individual keyboard events to update pressed_keys.
        
        :param event: The pygame event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys.values():
                self.pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            if event.key in self.keys.values():
                self.pressed_keys.discard(event.key)

    def is_key_pressed(self, action, current_time):
        """
        Check if a specific action is currently being pressed and handle cooldown.

        Parameters:
            action (str): The action to check ('left', 'right', 'down', 'rotate', 'drop').
            current_time (int): The current time in milliseconds.

        Returns:
            bool: True if the key for the action is pressed and cooldown has elapsed, False otherwise.
        """
        key_code = self.keys.get(action)
        if key_code in self.pressed_keys:
            elapsed_time = current_time - self.last_action_time[action]
            if elapsed_time >= self.cooldown[action]:
                self.last_action_time[action] = current_time
                return True
        return False

    def __del__(self):
        """
        Clean up resources when the KeyboardInput object is destroyed.
        """
        pygame.quit()  # Quit Pygame
