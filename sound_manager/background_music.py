import pygame

class BackgroundMusicManager:
    def __init__(self, music_file, volume=0.5):
        pygame.mixer.init()  # Initialize the mixer module for sound
        self.music_file = music_file
        self.is_playing = False
        self.volume = volume
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.set_volume(self.volume)

    def play_music(self):
        if not self.is_playing:
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            self.is_playing = True

    def stop_music(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False

    def toggle_music(self):
        if self.is_playing:
            self.stop_music()
        else:
            self.play_music()

    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)
