#ui/settings_menu.py

import pygame

class SettingsMenu:
    def __init__(self, game, background_music_manager, cell_size, control_panel_width):
        self.game = game
        self.background_music_manager = background_music_manager
        self.cell_size = cell_size
        self.control_panel_width = control_panel_width
        self.font = pygame.font.Font(None, 36)
        
        # Calculate center positions based on the game window size
        screen_width = (game.grid.width * self.cell_size) + self.control_panel_width
        screen_height = game.grid.height * self.cell_size
        center_x = screen_width // 2

        # Center the elements by calculating their position based on the window size
        self.music_toggle_button = self.create_button((250, 50), (0, 255, 0), (center_x - 125, 150), "Toggle Music")
        self.volume_slider = self.create_slider((center_x - 75, 240), self.background_music_manager.volume)  # Adjusted Y position
        self.sound_toggle_button = self.create_button((250, 50), (0, 255, 0), (center_x - 125, 310), "Sound: On")  # Adjusted Y position

    def create_button(self, size, color, position, text):
        button = pygame.sprite.Sprite()
        button.image = pygame.Surface(size)
        button.image.fill(color)
        button.rect = button.image.get_rect(topleft=position)
        button.text_surf = self.font.render(text, True, (255, 255, 255))
        button.text_rect = button.text_surf.get_rect(center=button.rect.center)
        return button

    def create_slider(self, position, initial_value):
        slider = pygame.sprite.Sprite()
        slider.image = pygame.Surface((150, 20))
        slider.rect = slider.image.get_rect(topleft=position)
        slider.value = initial_value
        return slider

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Check if the click is outside all interactive elements
            if not (self.music_toggle_button.rect.collidepoint(mouse_pos) or
                    self.volume_slider.rect.collidepoint(mouse_pos) or
                    self.sound_toggle_button.rect.collidepoint(mouse_pos)):
                # If the click is outside, close the settings menu
                self.game.toggle_settings()
                return

            if self.music_toggle_button.rect.collidepoint(mouse_pos):
                self.background_music_manager.toggle_music()
            elif self.volume_slider.rect.collidepoint(mouse_pos):
                slider_x = self.volume_slider.rect.x
                self.volume_slider.value = (mouse_pos[0] - slider_x) / 150  # Assuming slider width is 150 pixels
                self.background_music_manager.set_volume(self.volume_slider.value)
            elif self.sound_toggle_button.rect.collidepoint(mouse_pos):
                self.game.sound_effects_manager.toggle_sound()
                new_text = "Sound: On" if self.game.sound_effects_manager.sound_enabled else "Sound: Off"
                self.sound_toggle_button.text_surf = self.font.render(new_text, True, (255, 255, 255))
                self.sound_toggle_button.text_rect = self.sound_toggle_button.text_surf.get_rect(center=self.sound_toggle_button.rect.center)

    def draw(self, surface):
        # Create a semi-transparent overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with 180/255 transparency
        surface.blit(overlay, (0, 0))  # Blit the overlay onto the screen

        # Draw the buttons and slider on top of the semi-transparent background
        surface.blit(self.music_toggle_button.image, self.music_toggle_button.rect)
        surface.blit(self.music_toggle_button.text_surf, self.music_toggle_button.text_rect)

        pygame.draw.rect(surface, (255, 255, 255), self.volume_slider.rect)
        pygame.draw.rect(surface, (0, 255, 0), (self.volume_slider.rect.x, self.volume_slider.rect.y, self.volume_slider.value * 150, self.volume_slider.rect.height))
        volume_text = self.font.render(f"Volume: {int(self.volume_slider.value * 100)}%", True, (255, 255, 255))
        surface.blit(volume_text, (self.volume_slider.rect.x, self.volume_slider.rect.y - 30))

        surface.blit(self.sound_toggle_button.image, self.sound_toggle_button.rect)
        surface.blit(self.sound_toggle_button.text_surf, self.sound_toggle_button.text_rect)
