# game_engine/game.py
from datetime import datetime
from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino
from game_engine.score_manager import ScoreManager
from game_engine.level_manager import LevelManager
from game_engine.high_scores_manager import HighScoresManager
from sound_manager.sound_effects import SoundEffectsManager

class Game:
    def __init__(self, grid_width, grid_height, control_panel, sound_effects_manager, high_scores_persistence_manager):
        self.grid = Grid(grid_width, grid_height)
        self.tetromino = Tetromino()
        self.score_manager = ScoreManager()
        self.level_manager = LevelManager()
        self.high_scores_manager = HighScoresManager()
        self.sound_effects_manager = sound_effects_manager
        self.high_scores_persistence_manager = high_scores_persistence_manager
        self.is_paused = False
        self.game_over = False
        self.is_settings_open = False
        self.is_high_scores_open = False  # Add this attribute
        self.control_panel = control_panel
        self.score_added = False

    def start_new_game(self):
        self.grid = Grid(self.grid.width, self.grid.height)
        self.tetromino = Tetromino()
        self.score_manager = ScoreManager()
        self.level_manager = LevelManager()
        self.is_paused = False
        self.game_over = False
        self.control_panel.update()
        self.score_added = False

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.control_panel.update()

    def toggle_settings(self):
        self.is_settings_open = not self.is_settings_open

    def toggle_high_scores(self):
        self.is_high_scores_open = not self.is_high_scores_open

    def get_score(self):
        return self.score_manager.get_score()

    def update(self, keyboard_input):
        if self.is_paused or self.game_over:
            return

        # Handle keyboard input
        if keyboard_input.is_key_pressed('left'):
            self.tetromino.move('left', self.grid)
        if keyboard_input.is_key_pressed('right'):
            self.tetromino.move('right', self.grid)
        if keyboard_input.is_key_pressed('down'):
            if not self.tetromino.move('down', self.grid):
                self.grid.place_tetromino(self.tetromino)
                self.sound_effects_manager.play_sound('block_placed')  # Play block placement sound
                rows_cleared = self.grid.clear_rows()
                if rows_cleared > 0:
                    self.sound_effects_manager.play_sound('row_cleared')  # Play row cleared sound
                self.score_manager.add_points(rows_cleared)
                self.level_manager.update(self.score_manager.get_score())  # Update level based on score
                self.control_panel.update()  # Update control panel
                self.tetromino.generate_new_piece()  # Generate a new Tetromino

        # Handle rotation
        if keyboard_input.is_key_pressed('rotate'):
            self.tetromino.rotate(self.grid)  # Rotate the Tetromino

        # Check for game over
        if self.grid.is_game_over():
            self.game_over = True
            self.sound_effects_manager.play_sound('game_over')  # Play game over sound
            if not self.score_added:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.high_scores_manager.add_score(self.get_score())
                self.high_scores_persistence_manager.add_high_score(self.get_score(), current_time)
                self.score_added = True  # Ensure score is only added once
            # Handle rotation
            if keyboard_input.is_key_pressed('rotate'):
                self.tetromino.rotate(self.grid)  # Rotate the Tetromino

            # Check for game over
            if self.grid.is_game_over():
                self.game_over = True
                self.sound_effects_manager.play_sound('game_over')  # Play game over sound
                if not self.score_added:
                    self.high_scores_manager.add_score(self.get_score())
                    self.high_scores_persistence_manager.add_high_score({"score": self.get_score()})
                    self.score_added = True  # Ensure score is only added once

    def handle_natural_falling(self):
        """Handle the natural falling of the Tetromino based on DROP_INTERVAL."""
        if not self.tetromino.move('down', self.grid):
            self.grid.place_tetromino(self.tetromino)
            self.sound_effects_manager.play_sound('block_placed')  # Play block placement sound
            rows_cleared = self.grid.clear_rows()
            if rows_cleared > 0:
                self.sound_effects_manager.play_sound('row_cleared')  # Play row cleared sound
            self.score_manager.add_points(rows_cleared)
            self.level_manager.update(self.score_manager.get_score())  # Update level based on score
            self.control_panel.update()  # Update control panel
            self.tetromino.generate_new_piece()  # Generate a new Tetromino

        # Check for game over
        if self.grid.is_game_over():
            self.game_over = True
            self.sound_effects_manager.play_sound('game_over')  # Play game over sound
            if not self.score_added:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.high_scores_manager.add_score(self.get_score())
                self.high_scores_persistence_manager.add_high_score(self.get_score(), current_time)
                self.score_added = True  # Ensure score is only added once
