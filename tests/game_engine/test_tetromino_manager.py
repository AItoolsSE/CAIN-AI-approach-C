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

    def test_tetromino_move_left_edge(self):
        tetromino = Tetromino('I')
        grid = Grid(10, 20)
        tetromino.position = (0, 0)  # Move it to the far left
        tetromino.move('left', grid)
        self.assertEqual(tetromino.position, (0, 0))  # Should not move lefts

    def test_tetromino_move_into_filled_cells(self):
        shapes_to_test = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        grid = Grid(10, 20)

        for shape in shapes_to_test:
            with self.subTest(shape=shape):
                tetromino = Tetromino(shape)
                tetromino.position = (3, 0)  # Starting near the center

                # Get the blocks of the Tetromino based on its shape
                blocks = tetromino.get_blocks()

                # Surround each block with filled cells to prevent any movement
                for bx, by in blocks:
                    if bx - 1 >= 0:
                        grid.grid[by][bx - 1] = (1, (255, 255, 255))  # Left
                    if bx + 1 < grid.width:
                        grid.grid[by][bx + 1] = (1, (255, 255, 255))  # Right
                    if by - 1 >= 0:
                        grid.grid[by - 1][bx] = (1, (255, 255, 255))  # Above
                    if by + 1 < grid.height:
                        grid.grid[by + 1][bx] = (1, (255, 255, 255))  # Below

                # Attempt to move right, left, and down into the filled cells
                can_move_right = tetromino.move('right', grid)
                can_move_left = tetromino.move('left', grid)
                can_move_down = tetromino.move('down', grid)

                # Check that the Tetromino didn't move in any direction
                self.assertFalse(can_move_right)
                self.assertFalse(can_move_left)
                self.assertFalse(can_move_down)
                self.assertEqual(tetromino.position, (3, 0))  # Position should remain unchanged




    def test_tetromino_rotation_at_edge(self):
        tetromino = Tetromino('T')
        grid = Grid(10, 20)
        tetromino.position = (0, 0)  # Position near the left edge
        tetromino.rotate(grid)
        # Assert that rotation does not cause Tetromino to go out of bounds
        self.assertTrue(all(grid.is_valid_position(x, y) for x, y in tetromino.get_blocks()))

    def test_tetromino_rotation_collision(self):
        tetromino = Tetromino('T')
        grid = Grid(10, 20)
        grid.grid[0][2] = (1, (255, 255, 255))  # Block where rotation would overlap
        tetromino.position = (0, 0)
        tetromino.rotate(grid)
        # Assert Tetromino rotation does not cause it to overlap filled cells
        self.assertTrue(all(grid.is_valid_position(x, y) for x, y in tetromino.get_blocks()))

    def test_tetromino_random_shape(self):
        tetromino = Tetromino()
        self.assertIn(tetromino.shape, Tetromino.SHAPES.keys())
        self.assertIn(tetromino.color, Tetromino.COLORS.values())

    def test_all_shapes_rotation(self):
        for shape in Tetromino.SHAPES.keys():
            with self.subTest(shape=shape):
                tetromino = Tetromino(shape)
                grid = Grid(10, 20)
                initial_blocks = tetromino.blocks[:]
                tetromino.rotate(grid)
                if shape != 'O':
                    self.assertNotEqual(tetromino.blocks, initial_blocks)

    def test_no_three_consecutive_pieces(self):
        tetromino = Tetromino()
        consecutive_count = 1
        last_piece = tetromino.shape

        for _ in range(100000):
            new_piece = tetromino.generate_new_piece()
            if new_piece == last_piece:
                consecutive_count += 1
            else:
                consecutive_count = 1

            last_piece = new_piece
            self.assertLessEqual(consecutive_count, 2, "Same piece appeared more than twice in a row")

if __name__ == '__main__':
    unittest.main()

