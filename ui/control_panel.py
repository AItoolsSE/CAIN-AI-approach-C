#ui/control_panel.py

import pygame
from pygame.locals import MOUSEBUTTONDOWN

class ControlPanel(pygame.sprite.Sprite):
    def __init__(self, game, cell_size, grid_width):
        super().__init__()
        self.game = game
        self.cell_size = cell_size
        self.grid_width = grid_width
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)  # Smaller font for the date and time
        self.create_buttons()
        self.create_labels()
        self.buttons = pygame.sprite.Group(
            self.start_button, 
            self.pause_button, 
            self.settings_button, 
            self.high_scores_button
        )

    def create_buttons(self):
        self.start_button = self.create_button((150, 50), (0, 255, 0), (self.grid_width * self.cell_size + 10, 10), "Start")
        self.pause_button = self.create_button((150, 50), (255, 255, 0), (self.grid_width * self.cell_size + 10, 70), "Pause")
        self.settings_button = self.create_button((150, 50), (0, 0, 255), (self.grid_width * self.cell_size + 10, 130), "Settings")
        self.high_scores_button = self.create_button((150, 50), (255, 0, 0), (self.grid_width * self.cell_size + 10, 190), "High Scores")

    def create_button(self, size, color, position, text):
        button = pygame.sprite.Sprite()
        button.image = pygame.Surface(size)
        button.image.fill(color)
        button.rect = button.image.get_rect(topleft=position)
        
        # Add text to button
        button.text_surf = self.font.render(text, True, (255, 255, 255))
        button.text_rect = button.text_surf.get_rect(center=button.rect.center)
        
        button.default_color = color
        button.text = text
        return button

    def create_labels(self):
        self.score_label = self.create_label('Score: 0', (self.grid_width * self.cell_size + 10, 250), self.font)
        self.level_label = self.create_label('Level: 1', (self.grid_width * self.cell_size + 10, 300), self.font)

    def create_label(self, text, position, font):
        label = pygame.sprite.Sprite()
        label.image = font.render(text, True, (255, 255, 255))
        label.rect = label.image.get_rect(topleft=position)
        return label

    def handle_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.start_button.rect.collidepoint(mouse_pos):
                self.game.start_new_game()
            elif self.pause_button.rect.collidepoint(mouse_pos):
                self.game.toggle_pause()
            elif self.settings_button.rect.collidepoint(mouse_pos):
                # Directly handle the settings menu here
                self.game.is_settings_open = not self.game.is_settings_open
            elif self.high_scores_button.rect.collidepoint(mouse_pos):
                self.game.view_high_scores()

    def update(self):
        """Update the control panel with the current score and level."""
        level = self.game.level_manager.get_level()
        self.score_label.image = self.font.render(f'Score: {self.game.get_score()}', True, (255, 255, 255))
        self.level_label.image = self.font.render(f'Level: {level}', True, (255, 255, 255))

    def draw_high_scores(self, surface):
        """Draw the current session high scores table on the screen."""
        # Header
        title = self.font.render("Current Session", True, (255, 255, 255))
        surface.blit(title, (self.grid_width * self.cell_size + 10, 340))  # Adjusted position

        # Column titles
        score_header = self.small_font.render("Score", True, (255, 255, 255))
        time_header = self.small_font.render("Time", True, (255, 255, 255))
        surface.blit(score_header, (self.grid_width * self.cell_size + 10, 370))
        surface.blit(time_header, (self.grid_width * self.cell_size + 90, 370))  # Adjusted position to the left

        # Rows of scores
        high_scores = self.game.high_scores_manager.get_high_scores()
        for i, (score, timestamp) in enumerate(high_scores):
            y_pos = 400 + i * 30
            score_text = self.small_font.render(str(score), True, (255, 255, 255))
            time_text = self.small_font.render(timestamp, True, (255, 255, 255))  # Show the full timestamp (date and time)
            surface.blit(score_text, (self.grid_width * self.cell_size + 10, y_pos))
            surface.blit(time_text, (self.grid_width * self.cell_size + 90, y_pos))  # Adjusted position to the left

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        for button in [self.start_button, self.pause_button, self.settings_button, self.high_scores_button]:
            if button.rect.collidepoint(mouse_pos):
                button.image.fill((200, 200, 200))  # Highlight color
            else:
                button.image.fill(button.default_color)
            surface.blit(button.image, button.rect)
            surface.blit(button.text_surf, button.text_rect)
        surface.blit(self.score_label.image, self.score_label.rect)
        surface.blit(self.level_label.image, self.level_label.rect)  # Draw level label
        self.draw_high_scores(surface)  # Draw the high scores table
