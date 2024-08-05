# game.py
from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino
from game_engine.score_manager import ScoreManager

class Game:
    def __init__(self, grid_width, grid_height):
        self.grid = Grid(grid_width, grid_height)
        self.tetromino = Tetromino()
        self.score_manager = ScoreManager()
        self.is_paused = False
        self.game_over = False

    def start_new_game(self):
        self.grid = Grid(self.grid.width, self.grid.height)
        self.tetromino = Tetromino()
        self.score_manager = ScoreManager()
        self.is_paused = False
        self.game_over = False

    def toggle_pause(self):
        self.is_paused = not self.is_paused

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
            self.tetromino = Tetromino()

        # Check for game over
        if self.grid.is_game_over():
            self.game_over = True
