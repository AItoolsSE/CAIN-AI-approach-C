# tests/integration/test_integration.py

import unittest
import sys
import os
import random

# Ensure the base directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from input_handler.keyboard_input import KeyboardInput
from game_engine.tetromino_manager import Tetromino
from game_engine.grid_manager import Grid
from game_engine.score_manager import ScoreManager
from game_engine.game import Game
from ui.main_game_screen import MainGameScreen
from ui.control_panel import ControlPanel
from unittest.mock import patch, Mock
import pygame

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


if __name__ == '__main__':
    unittest.main()
