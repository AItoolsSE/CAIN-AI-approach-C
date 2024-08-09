from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino
from game_engine.score_manager import ScoreManager
from game_engine.level_manager import LevelManager  # Import LevelManager
from game_engine.high_scores_manager import HighScoresManager  # Import HighScoresManager

class Game:
    def __init__(self, grid_width, grid_height, control_panel):
        self.grid = Grid(grid_width, grid_height)
        self.tetromino = Tetromino()
        self.score_manager = ScoreManager()
        self.level_manager = LevelManager()  # Initialize LevelManager
        self.high_scores_manager = HighScoresManager()  # Initialize HighScoresManager
        self.is_paused = False
        self.game_over = False
        self.control_panel = control_panel
        self.score_added = False  # To track if the score has been added to high scores

    def start_new_game(self):
        self.grid = Grid(self.grid.width, self.grid.height)
        self.tetromino = Tetromino()
        self.score_manager = ScoreManager()
        self.level_manager = LevelManager()  # Reset LevelManager
        self.is_paused = False
        self.game_over = False
        self.control_panel.update()  # Update control panel
        self.score_added = False  # Reset score added flag for the new game

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.control_panel.update()  # Update control panel

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
                rows_cleared = self.grid.clear_rows()
                self.score_manager.add_points(rows_cleared)
                self.level_manager.update(self.score_manager.get_score())  # Update level based on score
                self.control_panel.update()  # Update control panel
                self.tetromino = Tetromino()
        if keyboard_input.is_key_pressed('rotate'):
            self.tetromino.rotate(self.grid)
        if keyboard_input.is_key_pressed('drop'):
            # Move Tetromino down until it cannot move further
            while self.tetromino.move('down', self.grid):
                pass
            self.grid.place_tetromino(self.tetromino)
            rows_cleared = self.grid.clear_rows()
            self.score_manager.add_points(rows_cleared)
            self.level_manager.update(self.score_manager.get_score())  # Update level based on score
            print(f"Level: {self.level_manager.get_level()}")
            self.control_panel.update()  # Update control panel
            self.tetromino = Tetromino()

        # Check for game over
        if self.grid.is_game_over():
            self.game_over = True
            if not self.score_added:
                self.high_scores_manager.add_score(self.get_score())
                self.score_added = True  # Ensure score is only added once
