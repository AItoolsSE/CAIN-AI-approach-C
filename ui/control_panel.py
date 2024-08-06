# ui/control_panel.py

import pygame
from pygame.locals import *

class ControlPanel(pygame.sprite.Sprite):
    def __init__(self, game, cell_size, grid_width):
        super().__init__()
        self.game = game
        self.cell_size = cell_size
        self.grid_width = grid_width
        self.font = pygame.font.Font(None, 36)
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
                self.game.open_settings()
            elif self.high_scores_button.rect.collidepoint(mouse_pos):
                self.game.view_high_scores()

    def update(self):
        self.score_label.image = self.font.render(f'Score: {self.game.get_score()}', True, (255, 255, 255))

    def draw(self, surface):
        if self.game.game_over:
            return
        mouse_pos = pygame.mouse.get_pos()
        for button in [self.start_button, self.pause_button, self.settings_button, self.high_scores_button]:
            if button.rect.collidepoint(mouse_pos):
                button.image.fill((200, 200, 200))  # Highlight color
            else:
                button.image.fill(button.default_color)
            surface.blit(button.image, button.rect)
            surface.blit(button.text_surf, button.text_rect)
        surface.blit(self.score_label.image, self.score_label.rect)
