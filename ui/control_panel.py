# ui/control_panel.py

import pygame
from pygame.locals import *

class ControlPanel(pygame.sprite.Sprite):
    def __init__(self, score_manager):
        """
        Initialize the ControlPanel with score manager and set up UI components.
        
        :param score_manager: The ScoreManager instance to track and display the score.
        """
        super().__init__()
        self.score_manager = score_manager
        self.font = pygame.font.Font(None, 24)  # Smaller font size for better fit
        self.create_buttons()
        self.create_labels()
        self.buttons = pygame.sprite.Group(
            self.start_button, 
            self.pause_button, 
            self.settings_button, 
            self.high_scores_button
        )

    def create_buttons(self):
        """
        Create and position buttons on the control panel.
        """
        button_width = 100
        button_height = 40
        spacing = 10  # Spacing between buttons
        x_position = 10  # X position for all buttons

        self.start_button = self.create_button((button_width, button_height), (0, 255, 0), (x_position, 10), "Start")
        self.pause_button = self.create_button((button_width, button_height), (255, 255, 0), (x_position, 60), "Pause")
        self.settings_button = self.create_button((button_width, button_height), (0, 0, 255), (x_position, 110), "Settings")
        self.high_scores_button = self.create_button((button_width, button_height), (255, 0, 0), (x_position, 160), "High Scores")

    def create_button(self, size, color, position, text):
        """
        Create a button sprite with specified size, color, position, and text.
        
        :param size: Tuple (width, height) for button dimensions.
        :param color: RGB tuple for button color.
        :param position: Tuple (x, y) for button position.
        :param text: Text to be displayed on the button.
        :return: Configured pygame.sprite.Sprite instance.
        """
        button = pygame.sprite.Sprite()
        button.image = pygame.Surface(size)
        button.default_color = color  # Store the default color
        button.image.fill(button.default_color)
        button.rect = button.image.get_rect(topleft=position)
        
        # Add text to button
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(size[0] // 2, size[1] // 2))
        button.image.blit(text_surf, text_rect)
        
        button.text_surf = text_surf
        button.text_rect = text_rect
        button.text = text
        return button

    def create_labels(self):
        """
        Create and position labels on the control panel.
        """
        self.score_label = self.create_label('Score: 0', (10, 210))
        self.status_label = self.create_label('Game Status: Running', (10, 240))

    def create_label(self, text, position):
        """
        Create a label sprite with specified text and position.
        
        :param text: Text to be displayed on the label.
        :param position: Tuple (x, y) for label position.
        :return: Configured pygame.sprite.Sprite instance.
        """
        label = pygame.sprite.Sprite()
        label.image = self.font.render(text, True, (255, 255, 255))
        label.rect = label.image.get_rect(topleft=position)
        return label

    def handle_events(self, event):
        """
        Handle user input events such as button clicks.
        
        :param event: The pygame event to handle.
        """
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.start_button.rect.collidepoint(mouse_pos):
                self.start_new_game()
            elif self.pause_button.rect.collidepoint(mouse_pos):
                self.toggle_pause()
            elif self.settings_button.rect.collidepoint(mouse_pos):
                self.open_settings()
            elif self.high_scores_button.rect.collidepoint(mouse_pos):
                self.view_high_scores()

    def update(self, is_paused):
        """
        Update the control panel display based on game state.
        """
        self.score_label.image = self.font.render(f'Score: {self.score_manager.get_score()}', True, (255, 255, 255))
        game_status = 'Paused' if is_paused else 'Running'
        self.status_label.image = self.font.render(f'Game Status: {game_status}', True, (255, 255, 255))

    def draw(self, surface):
        """
        Draw the control panel to the given surface.
        
        :param surface: The surface to draw the control panel onto.
        """
        mouse_pos = pygame.mouse.get_pos()
        for button in [self.start_button, self.pause_button, self.settings_button, self.high_scores_button]:
            button.image.fill(button.default_color)
            if button.rect.collidepoint(mouse_pos):
                button.image.fill((200, 200, 200))  # Highlight color
            button.image.blit(button.text_surf, button.text_rect)
            surface.blit(button.image, button.rect)
        surface.blit(self.score_label.image, self.score_label.rect)
        surface.blit(self.status_label.image, self.status_label.rect)

    def start_new_game(self):
        """
        Placeholder method to start a new game.
        """
        print("Starting a new game...")

    def toggle_pause(self):
        """
        Placeholder method to toggle pause.
        """
        print("Toggling pause...")

    def open_settings(self):
        """
        Placeholder method to open settings.
        """
        print("Opening settings...")

    def view_high_scores(self):
        """
        Placeholder method to view high scores.
        """
        print("Viewing high scores...")
