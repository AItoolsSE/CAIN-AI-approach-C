# tests/game_engine/test_tetromino_manager.py

import sys
import os

# Ensure the base directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from game_engine.tetromino_manager import Tetromino
from game_engine.grid_manager import Grid

class TestTetrominoManager(unittest.TestCase):
    def test_tetromino_initialization(self):
        tetromino = Tetromino()
        self.assertIn(tetromino.shape, Tetromino.SHAPES.keys())
        self.assertEqual(tetromino.position, (3, 0))

    def test_tetromino_movement(self):
        tetromino = Tetromino()
        grid = Grid(10, 20)

        # Move left
        tetromino.move('left', grid)
        self.assertEqual(tetromino.position, (2, 0))
        
        # Move right
        tetromino.move('right', grid)
        self.assertEqual(tetromino.position, (3, 0))

        # Move down
        tetromino.move('down', grid)
        self.assertEqual(tetromino.position, (3, 1))

    def test_tetromino_rotation(self):
        tetromino = Tetromino()
        grid = Grid(10, 20)

        initial_blocks = tetromino.blocks[:]
        tetromino.rotate(grid)
        if tetromino.shape != 'O':
            self.assertNotEqual(tetromino.blocks, initial_blocks)

    def test_get_blocks(self):
        tetromino = Tetromino()
        blocks = tetromino.get_blocks()
        expected_blocks = [(x + 3, y) for x, y in tetromino.SHAPES[tetromino.shape]]
        self.assertEqual(blocks, expected_blocks)

if __name__ == '__main__':
    unittest.main()
