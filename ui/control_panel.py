# ui/control_panel.py

import pygame
from pygame.locals import *

class ControlPanel(pygame.sprite.Sprite):
    def __init__(self, game):
        """
        Initialize the ControlPanel with game context and set up UI components.
        
        :param game: The main game instance, used to interact with the game state.
        """
        super().__init__()
        self.game = game
        self.font = pygame.font.Font(None, 24)  # Reduced font size
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
        button_width = 150
        button_height = 40
        padding = 10

        self.start_button = self.create_button((button_width, button_height), (0, 255, 0), (10, padding), "Start")
        self.pause_button = self.create_button((button_width, button_height), (255, 255, 0), (10, padding * 2 + button_height), "Pause")
        self.settings_button = self.create_button((button_width, button_height), (0, 0, 255), (10, padding * 3 + button_height * 2), "Settings")
        self.high_scores_button = self.create_button((button_width, button_height), (255, 0, 0), (10, padding * 4 + button_height * 3), "High Scores")

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
        button.image.fill(color)
        button.rect = button.image.get_rect(topleft=position)
        
        # Add text to button
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(size[0] // 2, size[1] // 2))
        button.image.blit(text_surf, text_rect)
        
        button.default_color = color  # Store the default color
        button.text = text  # Store the text for later use
        return button

    def create_labels(self):
        """
        Create and position labels on the control panel.
        """
        self.score_label = self.create_label('Score: 0', (10, 200))
        self.status_label = self.create_label('Game Status: Running', (10, 230))

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
                self.game.start_new_game()
            elif self.pause_button.rect.collidepoint(mouse_pos):
                self.game.toggle_pause()
            elif self.settings_button.rect.collidepoint(mouse_pos):
                self.game.open_settings()
            elif self.high_scores_button.rect.collidepoint(mouse_pos):
                self.game.view_high_scores()

    def update(self, is_paused):
        """
        Update the control panel display based on game state.
        """
        self.score_label.image = self.font.render(f'Score: {self.game.get_score()}', True, (255, 255, 255))
        game_status = 'Paused' if is_paused else 'Running'
        self.status_label.image = self.font.render(f'Game Status: {game_status}', True, (255, 255, 255))

    def draw(self, surface):
        """
        Draw the control panel to the given surface.
        
        :param surface: The surface to draw the control panel onto.
        """
        mouse_pos = pygame.mouse.get_pos()
        for button in [self.start_button, self.pause_button, self.settings_button, self.high_scores_button]:
            if button.rect.collidepoint(mouse_pos):
                button.image.fill((200, 200, 200))  # Highlight color
                text_surf = self.font.render(button.text, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(button.rect.width // 2, button.rect.height // 2))
                button.image.blit(text_surf, text_rect)
            else:
                button.image.fill(button.default_color)  # Default color
                text_surf = self.font.render(button.text, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(button.rect.width // 2, button.rect.height // 2))
                button.image.blit(text_surf, text_rect)
            surface.blit(button.image, button.rect)
        surface.blit(self.score_label.image, self.score_label.rect)
        surface.blit(self.status_label.image, self.status_label.rect)
