#sound_manager/sound_effects.py

import pygame

class SoundEffectsManager:
    def __init__(self, sound_files):
        self.sound_files = sound_files
        self.sound_enabled = True  # Sound effects are enabled by default
        self.sounds = self.load_sounds()

    def load_sounds(self):
        """Load the sound files and return a dictionary of sounds."""
        sounds = {}
        for event, file_path in self.sound_files.items():
            sounds[event] = pygame.mixer.Sound(file_path)
        return sounds

    def play_sound(self, event):
        """Play the sound associated with the given event if sound is enabled."""
        if self.sound_enabled and event in self.sounds:
            if event == "next_level":
                return  # Skip playing the next_level sound
            self.sounds[event].play()

    def toggle_sound(self):
        """Toggle the sound effects on or off."""
        self.sound_enabled = not self.sound_enabled
