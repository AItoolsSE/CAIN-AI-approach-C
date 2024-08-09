import pygame

class SettingsMenu:
    def __init__(self, game, background_music_manager):
        self.game = game
        self.background_music_manager = background_music_manager
        self.font = pygame.font.Font(None, 36)
        self.music_toggle_button = self.create_button((200, 50), (0, 255, 0), (100, 100), "Toggle Music")
        self.volume_slider = self.create_slider((100, 200), self.background_music_manager.volume)

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
            if self.music_toggle_button.rect.collidepoint(event.pos):
                self.background_music_manager.toggle_music()
            elif self.volume_slider.rect.collidepoint(event.pos):
                mouse_x, _ = pygame.mouse.get_pos()
                slider_x = self.volume_slider.rect.x
                self.volume_slider.value = (mouse_x - slider_x) / 150  # Assuming slider width is 150 pixels
                self.background_music_manager.set_volume(self.volume_slider.value)

    def draw(self, surface):
        surface.blit(self.music_toggle_button.image, self.music_toggle_button.rect)
        surface.blit(self.music_toggle_button.text_surf, self.music_toggle_button.text_rect)

        pygame.draw.rect(surface, (255, 255, 255), self.volume_slider.rect)
        pygame.draw.rect(surface, (0, 255, 0), (self.volume_slider.rect.x, self.volume_slider.rect.y, self.volume_slider.value * 150, self.volume_slider.rect.height))
        volume_text = self.font.render(f"Volume: {int(self.volume_slider.value * 100)}%", True, (255, 255, 255))
        surface.blit(volume_text, (self.volume_slider.rect.x, self.volume_slider.rect.y - 30))
