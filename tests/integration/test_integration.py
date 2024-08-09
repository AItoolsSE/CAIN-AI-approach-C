import unittest
import sys
import os
import random
from unittest.mock import patch, Mock
import pygame

# Ensure the base directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from input_handler.keyboard_input import KeyboardInput
from game_engine.tetromino_manager import Tetromino
from game_engine.grid_manager import Grid
from game_engine.score_manager import ScoreManager
from game_engine.game import Game
from ui.main_game_screen import MainGameScreen
from ui.control_panel import ControlPanel

class TestIntegration(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.grid_width = 10
        self.grid_height = 20
        self.cell_size = 30
        self.grid = Grid(self.grid_width, self.grid_height)
        self.keyboard_input = KeyboardInput()
        self.score_manager = ScoreManager()
        self.screen = MainGameScreen(self.grid_width, self.grid_height, self.cell_size)
        self.control_panel = ControlPanel(None, self.cell_size, self.grid_width)
        self.game = Game(self.grid_width, self.grid_height, self.control_panel)
        self.control_panel.game = self.game

    def test_place_tetromino_on_grid(self):
        tetromino = Tetromino()
        self.grid.place_tetromino(tetromino)
        blocks = tetromino.get_blocks()
        print("Placing tetromino on grid:")
        for x, y in blocks:
            print(f"Block at ({x}, {y})")
            self.assertEqual(self.grid.grid[y][x][0], 1)  # Check presence of tetromino block
            self.assertEqual(self.grid.grid[y][x][1], tetromino.color)  # Check tetromino color

    def test_clear_row(self):
        self.grid.grid[19] = [(1, (255, 255, 255))] * 10
        print("Grid before clearing row:")
        for row in self.grid.grid:
            print(row)
        cleared_rows = self.grid.clear_rows()
        print("Grid after clearing row:")
        for row in self.grid.grid:
            print(row)
        self.assertEqual(cleared_rows, 1)
        self.assertTrue(all(cell[0] == 0 for cell in self.grid.grid[19]))  # Check if the row is cleared

    def test_game_over(self):
        self.grid.grid[0] = [(1, (255, 255, 255))] * 10
        print("Grid before checking game over:")
        for row in self.grid.grid:
            print(row)
        self.assertTrue(self.grid.is_game_over())

    @patch('random.choice', return_value='I')
    @patch('pygame.event.get')
    def test_full_game_flow(self, mock_pygame_event_get, mock_random_choice):
        tetromino = Tetromino()
        self.grid.place_tetromino(tetromino)
        self.game.tetromino = tetromino
        print("Initial grid state:")
        for row in self.grid.grid:
            print(row)
        
        # Mock dropping the tetromino down until it can't move further
        while self.game.tetromino.move('down', self.grid):
            pass
        self.grid.place_tetromino(self.game.tetromino)
        print("Grid after dropping tetromino:")
        for row in self.grid.grid:
            print(row)
        
        # Clear rows if any are full
        rows_cleared = self.grid.clear_rows()
        print(f"Rows cleared: {rows_cleared}")
        self.score_manager.add_points(rows_cleared)
        
        # Check if the game is over
        if self.grid.is_game_over():
            self.game.game_over = True
        
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.score_manager.get_score(), 0)

    def test_pause_and_resume(self):
        # Pause the game first
        self.control_panel.handle_events(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.control_panel.pause_button.rect.topleft}))
        self.assertTrue(self.game.is_paused)  # Check if the game is paused

        # Record the initial position
        initial_position = self.game.tetromino.position

        # Attempt to move tetromino while paused (should not move)
        self.game.update(self.keyboard_input)  # This will attempt to move the tetromino
        self.assertEqual(self.game.tetromino.position, initial_position)  # Should not move

        # Resume the game
        self.control_panel.handle_events(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.control_panel.pause_button.rect.topleft}))
        self.assertFalse(self.game.is_paused)

    def test_score_update_display(self):
        # Fill a row with 9 blocks and leave one empty space on the right
        self.grid.grid[19] = [(1, (255, 255, 255))] * 6 + [(0, None)]*4

        # Print grid state before placing the tetromino
        print("Grid before placing the tetromino:")
        for row in self.grid.grid:
            print(row)

        # Create a horizontal 'I' tetromino and align it with the empty slot
        tetromino = Tetromino('I')
        self.game.tetromino = tetromino

        # Move the tetromino to align with the empty slot
        while self.game.tetromino.position[0] < 6:
            self.game.tetromino.move('right', self.grid)

        # Print tetromino position before dropping
        print(f"Tetromino position before dropping: {self.game.tetromino.position}")

        # Drop the tetromino until it lands
        while self.game.tetromino.move('down', self.grid):
            pass

        # Print grid state after dropping the tetromino
        print("Grid after dropping the tetromino:")
        for row in self.grid.grid:
            print(row)

        # Place the tetromino and clear rows
        self.grid.place_tetromino(self.game.tetromino)
        rows_cleared = self.grid.clear_rows()

        # Print grid state after clearing rows
        print("Grid after clearing rows:")
        for row in self.grid.grid:
            print(row)

        # Print number of rows cleared
        print(f"Rows cleared: {rows_cleared}")

        self.score_manager.add_points(rows_cleared)
        self.control_panel.update()

        # Verify the score is updated correctly
        print(f"Score after clearing rows: {self.score_manager.get_score()}")
        self.assertEqual(self.score_manager.get_score(), 40)



    @patch('random.choice', return_value='T')
    def test_tetromino_rotation_near_boundary(self, mock_random_choice):
        tetromino = Tetromino()
        self.grid.place_tetromino(tetromino)
        self.game.tetromino = tetromino
        self.game.tetromino.position = (0, 0)  # Position near the left edge
        
        self.game.tetromino.rotate(self.grid)
        
        # Ensure that the tetromino did not rotate out of bounds
        for x, y in self.game.tetromino.get_blocks():
            self.assertTrue(self.grid.is_valid_position(x, y))

    @patch('random.choice', return_value='O')
    def test_game_over_after_multiple_tetrominoes(self, mock_random_choice):
        for i in range(self.grid_height):
            tetromino = Tetromino()
            self.grid.place_tetromino(tetromino)
            self.game.tetromino = tetromino
            
            while self.game.tetromino.move('down', self.grid):
                pass
            
            self.grid.place_tetromino(self.game.tetromino)
            
            if self.grid.is_game_over():
                self.game.game_over = True
                break
        
        self.assertTrue(self.game.game_over)

    @patch('random.choice', return_value='I')
    def test_tetromino_collision(self, mock_random_choice):
        tetromino = Tetromino()
        self.grid.grid[18] = [(1, (255, 255, 255))] * 10  # Simulate a filled row
        
        while self.game.tetromino.move('down', self.grid):
            pass  # Should stop when it hits the filled row
        
        self.grid.place_tetromino(self.game.tetromino)
        
        # Ensure the tetromino is placed right above the filled row
        for x, y in self.game.tetromino.get_blocks():
            self.assertTrue(self.grid.grid[y][x][0] == 1)
            self.assertEqual(self.grid.grid[y][x][1], self.game.tetromino.color)

    def test_ui_update_on_tetromino_placement(self):
        tetromino = Tetromino('L')
        self.grid.place_tetromino(tetromino)
        self.control_panel.update()

        surface = pygame.Surface((800, 600))
        self.control_panel.draw(surface)
        
        # Check if the control panel and game screen have updated elements
        self.assertTrue(any(self.grid.grid[y][x][0] == 1 for x, y in tetromino.get_blocks()))

    def test_control_panel_interaction(self):
        self.control_panel.handle_events(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.control_panel.pause_button.rect.topleft}))
        self.assertTrue(self.game.is_paused)  # Assuming `is_paused` flag is in Game class
        
        # Simulate clicking "Start" to resume
        self.control_panel.handle_events(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.control_panel.start_button.rect.topleft}))
        self.assertFalse(self.game.is_paused)
        
        # Simulate opening high scores
        self.control_panel.handle_events(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.control_panel.high_scores_button.rect.topleft}))
        self.assertTrue(self.game.view_high_scores)  # Assuming `viewing_high_scores` flag in Game class

if __name__ == '__main__':
    unittest.main()
