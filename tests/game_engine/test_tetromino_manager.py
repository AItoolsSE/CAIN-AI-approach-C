# tests/game_engine/test_tetromino_manager.py

import unittest
from game_engine.tetromino_manager import Tetromino

class TestTetrominoManager(unittest.TestCase):
    def test_tetromino_initialization(self):
        tetromino = Tetromino()
        self.assertIn(tetromino.shape, Tetromino.SHAPES.keys())
        self.assertEqual(tetromino.position, (3, 0))

    def test_tetromino_movement(self):
        tetromino = Tetromino()
        grid_width = 10
        grid_height = 20

        # Move left
        tetromino.move('left', grid_width, grid_height)
        self.assertEqual(tetromino.position, (2, 0))
        
        # Move right
        tetromino.move('right', grid_width, grid_height)
        self.assertEqual(tetromino.position, (3, 0))

        # Move down
        tetromino.move('down', grid_width, grid_height)
        self.assertEqual(tetromino.position, (3, 1))

    def test_tetromino_rotation(self):
        tetromino = Tetromino()
        grid_width = 10
        grid_height = 20

        initial_blocks = tetromino.blocks[:]
        tetromino.rotate(grid_width, grid_height)
        if tetromino.shape != 'O':
            self.assertNotEqual(tetromino.blocks, initial_blocks)

    def test_get_blocks(self):
        tetromino = Tetromino()
        blocks = tetromino.get_blocks()
        expected_blocks = [(x + 3, y) for x, y in tetromino.SHAPES[tetromino.shape]]
        self.assertEqual(blocks, expected_blocks)

if __name__ == '__main__':
    unittest.main()
