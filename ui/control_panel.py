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
            (screen_width - 240, screen_height - 50),
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
            else:
                # Check if the high scores menu is open and click is outside the menu
                if self.game.is_high_scores_open:
                    # Calculate the position of the high scores menu
                    screen_width = self.grid_width * self.cell_size + self.control_panel_width
                    screen_height = self.grid_height * self.cell_size
                    table_width = 300  # Use the same width as defined in draw_high_scores
                    table_height = 400  # Use the same height as defined in draw_high_scores
                    table_x = (screen_width - table_width) // 2
                    table_y = (screen_height - table_height) // 2

                    # Check if the click is outside the high scores menu area
                    if not (table_x <= mouse_pos[0] <= table_x + table_width and 
                            table_y <= mouse_pos[1] <= table_y + table_height):
                        self.game.toggle_high_scores()  # Close the high scores screen

    def update(self):
        level = self.game.level_manager.get_level()
        self.score_label.image = self.font.render(f'Score: {self.game.get_score()}', True, (255, 255, 255))
        self.level_label.image = self.font.render(f'Level: {level}', True, (255, 255, 255))

        top_score = self.game.high_scores_persistence_manager.get_top_high_score()
        top_score_value = top_score["score"] if top_score else 0
        self.top_score_label.image = self.font.render(f'All-Time Best: {top_score_value}', True, (255, 255, 255))

    def draw_high_scores(self, surface):
        # Get the screen dimensions
        screen_width = self.grid_width * self.cell_size + self.control_panel_width
        screen_height = self.grid_height * self.cell_size
        
        # Define the width and height of the high scores table
        table_width = 300  # Adjust this width according to your needs
        table_height = 400  # Adjust this height according to your needs
        
        # Calculate the position to center the table on the screen
        table_x = (screen_width - table_width) // 2
        table_y = (screen_height - table_height) // 2
        
        # Draw the semi-transparent background for the table
        background_rect = pygame.Rect(table_x, table_y, table_width, table_height)
        pygame.draw.rect(surface, (0, 0, 0, 180), background_rect)
        
        # Draw the title
        title = self.font.render("All-Time High Scores", True, (255, 255, 255))
        surface.blit(title, (table_x + (table_width - title.get_width()) // 2, table_y + 20))
        
        # Draw column headers
        score_header = self.small_font.render("Score", True, (255, 255, 255))
        date_header = self.small_font.render("Date", True, (255, 255, 255))
        surface.blit(score_header, (table_x + 20, table_y + 60))
        surface.blit(date_header, (table_x + 120, table_y + 60))
        
        # Draw the high scores
        high_scores = self.game.high_scores_persistence_manager.get_top_ten_high_scores()
        for i, entry in enumerate(high_scores):
            y_pos = table_y + 90 + i * 30
            score_text = self.small_font.render(str(entry['score']), True, (255, 255, 255))
            date_text = self.small_font.render(entry['date'], True, (255, 255, 255))
            surface.blit(score_text, (table_x + 20, y_pos))
            surface.blit(date_text, (table_x + 120, y_pos))

    def draw_current_session_scores(self, surface):
        """Draw the current session high scores table."""
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
        
        # Draw the current session scores by default
        if not self.game.is_high_scores_open:
            self.draw_current_session_scores(surface)