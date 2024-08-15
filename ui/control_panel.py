import pygame
from pygame.locals import MOUSEBUTTONDOWN

class ControlPanel(pygame.sprite.Sprite):
    def __init__(self, game, cell_size, grid_width, grid_height, control_panel_width):
        super().__init__()
        self.game = game
        self.cell_size = cell_size
        self.grid_width = grid_width
        self.grid_height = grid_height  # Store the grid height
        self.control_panel_width = control_panel_width  # Store the control panel width
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
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
        button.default_color = color  # Set the default color attribute
        button.text_surf = self.font.render(text, True, (255, 255, 255))
        button.text_rect = button.text_surf.get_rect(center=button.rect.center)
        button.color = color  # Store the color for restoring later
        return button

    def create_labels(self):
        self.score_label = self.create_label('Score: 0', (self.grid_width * self.cell_size + 10, 250), self.font)
        self.level_label = self.create_label('Level: 1', (self.grid_width * self.cell_size + 10, 300), self.font)
        # Adjust the top score label to the bottom right of the screen
        screen_width = self.grid_width * self.cell_size + self.control_panel_width
        screen_height = self.cell_size * self.grid_height
        self.top_score_label = self.create_label(
            'All-Time Best: 0',
            (screen_width - 200, screen_height - 50),
            self.font
        )

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
                self.game.is_settings_open = not self.game.is_settings_open
            elif self.high_scores_button.rect.collidepoint(mouse_pos):
                self.game.toggle_high_scores()  # Toggle the high scores screen

    def update(self):
        level = self.game.level_manager.get_level()
        self.score_label.image = self.font.render(f'Score: {self.game.get_score()}', True, (255, 255, 255))
        self.level_label.image = self.font.render(f'Level: {level}', True, (255, 255, 255))

        top_score = self.game.high_scores_persistence_manager.get_top_high_score()
        top_score_value = top_score["score"] if top_score else 0
        self.top_score_label.image = self.font.render(f'All-Time Best: {top_score_value}', True, (255, 255, 255))

    def draw_high_scores(self, surface):
        title = self.font.render("Current Session", True, (255, 255, 255))
        surface.blit(title, (self.grid_width * self.cell_size + 10, 340))

        score_header = self.small_font.render("Score", True, (255, 255, 255))
        time_header = self.small_font.render("Time", True, (255, 255, 255))
        surface.blit(score_header, (self.grid_width * self.cell_size + 10, 370))
        surface.blit(time_header, (self.grid_width * self.cell_size + 90, 370))

        high_scores = self.game.high_scores_manager.get_high_scores()
        for i, (score, timestamp) in enumerate(high_scores):
            y_pos = 400 + i * 30
            score_text = self.small_font.render(str(score), True, (255, 255, 255))
            time_text = self.small_font.render(timestamp, True, (255, 255, 255))
            surface.blit(score_text, (self.grid_width * self.cell_size + 10, y_pos))
            surface.blit(time_text, (self.grid_width * self.cell_size + 90, y_pos))

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        for button in [self.start_button, self.pause_button, self.settings_button, self.high_scores_button]:
            if button.rect.collidepoint(mouse_pos):
                button.image.fill((200, 200, 200))  # Highlight color
            else:
                button.image.fill(button.default_color)  # Use the default color
            surface.blit(button.image, button.rect)
            surface.blit(button.text_surf, button.text_rect)
        surface.blit(self.score_label.image, self.score_label.rect)
        surface.blit(self.level_label.image, self.level_label.rect)
        surface.blit(self.top_score_label.image, self.top_score_label.rect)
        self.draw_high_scores(surface)
