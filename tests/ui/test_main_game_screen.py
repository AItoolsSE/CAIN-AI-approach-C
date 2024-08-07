# tests/ui/test_main_game_screen.py

import unittest
import sys
import os

# Ensure the base directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ui.main_game_screen import MainGameScreen
from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino
import pygame

class TestMainGameScreen(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.grid_width = 10
        self.grid_height = 20
        self.cell_size = 30
        self.screen = MainGameScreen(self.grid_width, self.grid_height, self.cell_size)
        self.grid = Grid(self.grid_width, self.grid_height)
        self.tetromino = Tetromino()

    def test_draw_grid(self):
        self.screen.draw_grid(self.grid)
        # Check if the screen was updated by verifying the color of a cell
        self.assertEqual(self.screen.screen.get_at((1, 1)), (0, 0, 0, 255))  # Inside a cell
        self.assertEqual(self.screen.screen.get_at((0, 0)), (50, 50, 50, 255))  # Grid line

    def test_draw_tetromino(self):
        self.tetromino.position = (0, 0)
        self.screen.draw_tetromino(self.tetromino)
        # Check if the tetromino was drawn by verifying the color of a cell
        block = self.tetromino.get_blocks()[0]
        x, y = block[0] * self.cell_size, block[1] * self.cell_size
        self.assertEqual(self.screen.screen.get_at((x + 1, y + 1)), self.tetromino.color + (255,))  # Inside a tetromino block

    def test_update(self):
        self.screen.update(self.grid, self.tetromino)
        # Check if the screen was updated by verifying the color of a cell
        self.assertEqual(self.screen.screen.get_at((1, 1)), (0, 0, 0, 255))  # Inside a cell
        self.assertEqual(self.screen.screen.get_at((0, 0)), (50, 50, 50, 255))  # Grid line

    def tearDown(self):
        self.screen.quit()

if __name__ == '__main__':
    unittest.main()
