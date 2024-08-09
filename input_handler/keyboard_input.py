import pygame

class KeyboardInput:
    def __init__(self):
        """
        Initialize the KeyboardInput class and set up key mappings.
        """
        self.keys = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'down': pygame.K_DOWN,
            'rotate': pygame.K_UP,
            'drop': pygame.K_SPACE
        }
        self.pressed_keys = set()  # Set to keep track of pressed keys
        self.last_press_time = {action: 0 for action in self.keys}  # Track the last press time for each action
        self.key_tap_time = {action: 0 for action in self.keys}  # Track the last tap time for each action
        self.cooldown = 100  # Cooldown time in milliseconds

    def handle_events(self, events):
        """
        Handle keyboard events and update the state of pressed keys.

        Parameters:
            events (list): List of Pygame events.
        """
        current_time = pygame.time.get_ticks()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in self.keys.values():
                self.pressed_keys.add(event.key)
                for action, key in self.keys.items():
                    if key == event.key:
                        self.last_press_time[action] = current_time  # Update the last press time on key down
                        self.key_tap_time[action] = current_time  # Also track key tap time
            elif event.type == pygame.KEYUP and event.key in self.keys.values():
                if event.key in self.pressed_keys:
                    self.pressed_keys.remove(event.key)

    def is_key_pressed(self, action):
        """
        Check if a specific action is currently being pressed or tapped.

        Parameters:
            action (str): The action to check ('left', 'right', 'down', 'rotate', 'drop').

        Returns:
            bool: True if the key for the action is pressed or tapped, False otherwise.
        """
        current_time = pygame.time.get_ticks()
        key = self.keys.get(action)
        if key is None:
            return False
        
        # Handle key tap (tap takes precedence over hold)
        if key in self.pressed_keys and current_time - self.key_tap_time[action] < self.cooldown:
            self.key_tap_time[action] = 0  # Reset tap time after handling
            return True
        
        # Handle key hold with cooldown
        if key in self.pressed_keys and current_time - self.last_press_time[action] > self.cooldown:
            self.last_press_time[action] = current_time
            return True
        
        return False
