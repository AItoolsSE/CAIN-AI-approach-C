# tests/integration/test_integration.py

import unittest
import sys
import os

# Ensure the base directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from input_handler.keyboard_input import KeyboardInput
from game_engine.tetromino_manager import Tetromino
from game_engine.grid_manager import Grid
from unittest.mock import patch, Mock
import pygame

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(10, 20)
        self.keyboard_input = KeyboardInput()

    def test_place_tetromino_on_grid(self):
        tetromino = Tetromino()
        self.grid.place_tetromino(tetromino)
        blocks = tetromino.get_blocks()
        for x, y in blocks:
            self.assertEqual(self.grid.grid[y][x], 1)

    @patch('pygame.event.get')
    def test_move_tetromino_left(self, mock_pygame_event_get):
        tetromino = Tetromino()
        self.grid.place_tetromino(tetromino)
        initial_blocks = tetromino.get_blocks()
        
        mock_pygame_event_get.return_value = [Mock(type=pygame.KEYDOWN, key=pygame.K_LEFT)]
        self.keyboard_input.handle_events()
        if self.keyboard_input.is_key_pressed('left'):
            tetromino.move('left', self.grid.width, self.grid.height)
        
        self.grid = Grid(10, 20)  # Reset grid for testing
        self.grid.place_tetromino(tetromino)
        moved_blocks = tetromino.get_blocks()
        for x, y in moved_blocks:
            self.assertEqual(self.grid.grid[y][x], 1)
        self.assertNotEqual(initial_blocks, moved_blocks)

    @patch('pygame.event.get')
    def test_rotate_tetromino(self, mock_pygame_event_get):
        tetromino = Tetromino()
        self.grid.place_tetromino(tetromino)
        initial_blocks = tetromino.get_blocks()
        
        mock_pygame_event_get.return_value = [Mock(type=pygame.KEYDOWN, key=pygame.K_UP)]
        self.keyboard_input.handle_events()
        if self.keyboard_input.is_key_pressed('rotate'):
            tetromino.rotate(self.grid.width, self.grid.height)
        
        self.grid = Grid(10, 20)  # Reset grid for testing
        self.grid.place_tetromino(tetromino)
        rotated_blocks = tetromino.get_blocks()
        for x, y in rotated_blocks:
            self.assertEqual(self.grid.grid[y][x], 1)
        if tetromino.shape == 'O':
            self.assertEqual(initial_blocks, rotated_blocks)
        else:
            self.assertNotEqual(initial_blocks, rotated_blocks)

    def test_clear_row(self):
        self.grid.grid[19] = [1] * 10
        cleared_rows = self.grid.clear_rows()
        self.assertEqual(cleared_rows, 1)
        self.assertTrue(all(cell == 0 for cell in self.grid.grid[19]))

if __name__ == '__main__':
    unittest.main()
