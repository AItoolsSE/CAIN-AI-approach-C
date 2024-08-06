import pygame

class GameOverScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 36)
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent background
        self.text_color = (255, 255, 255)
        self.restart_button_rect = None
        self.exit_button_rect = None

    def display(self, surface, final_score):
        # Draw the semi-transparent background
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill(self.bg_color)
        surface.blit(overlay, (0, 0))
        
        # Display "Game Over" text
        game_over_text = self.font_large.render("Game Over", True, self.text_color)
        text_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        surface.blit(game_over_text, text_rect)

        # Display final score
        score_text = self.font_small.render(f"Final Score: {final_score}", True, self.text_color)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        surface.blit(score_text, score_rect)

        # Display buttons
        restart_button_surf, self.restart_button_rect = self.create_button("Restart", (self.screen_width // 2, self.screen_height // 2 + 100))
        exit_button_surf, self.exit_button_rect = self.create_button("Exit", (self.screen_width // 2, self.screen_height // 2 + 160))
        surface.blit(restart_button_surf, self.restart_button_rect)
        surface.blit(exit_button_surf, self.exit_button_rect)
    
    def create_button(self, text, position):
        button_surf = pygame.Surface((200, 50), pygame.SRCALPHA)
        button_rect = button_surf.get_rect(center=position)
        button_surf.fill((100, 100, 100, 255))  # Grey color with full opacity
        
        text_surf = self.font_small.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(100, 25))  # Center text in button
        button_surf.blit(text_surf, text_rect)

        return button_surf, button_rect

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.restart_button_rect.collidepoint(mouse_pos):
                return 'restart'
            elif self.exit_button_rect.collidepoint(mouse_pos):
                return 'exit'
        return None
