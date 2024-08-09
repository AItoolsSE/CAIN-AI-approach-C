import sys
import os

# Ensure the base directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest
from game_engine.grid_manager import Grid

class Tetromino:
    def __init__(self, blocks, color=(255, 255, 255)):
        self.blocks = blocks
        self.color = color

    def get_blocks(self):
        return self.blocks
    
    def get_color(self):
        return self.color

class TestGridManager(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(10, 20)

    def test_grid_initialization(self):
        self.assertEqual(len(self.grid.grid), 20)
        self.assertTrue(all(len(row) == 10 for row in self.grid.grid))
        self.assertTrue(all(cell == (0, None) for row in self.grid.grid for cell in row))

    def test_place_tetromino_empty_grid(self):
        tetromino = Tetromino([(0, 0), (1, 0), (2, 0), (3, 0)])  # I-shape
        self.grid.place_tetromino(tetromino)
        self.assertTrue(all(self.grid.grid[0][x] == (1, tetromino.get_color()) for x in range(4)))

    def test_place_tetromino_partially_filled_grid(self):
        self.grid.grid[19][0] = (1, (255, 255, 255))
        tetromino = Tetromino([(0, 18), (1, 18), (2, 18), (3, 18)])  # I-shape
        self.grid.place_tetromino(tetromino)
        self.assertTrue(all(self.grid.grid[18][x] == (1, tetromino.get_color()) for x in range(4)))
        self.assertEqual(self.grid.grid[19][0], (1, (255, 255, 255)))

    def test_place_tetromino_out_of_bounds(self):
        tetromino_shapes = {
            "I-shape": Tetromino([(0, -1), (1, -1), (2, -1), (3, -1)]),
            "O-shape": Tetromino([(-1, 0), (-1, 1), (0, 0), (0, 1)]),
            "T-shape": Tetromino([(-1, 1), (0, 0), (0, 1), (0, 2)]),
            "L-shape": Tetromino([(-1, 0), (0, 0), (0, 1), (0, 2)]),
            "J-shape": Tetromino([(-1, 2), (0, 0), (0, 1), (0, 2)])
        }

        for shape_name, tetromino in tetromino_shapes.items():
            with self.subTest(tetromino=shape_name):
                with self.assertRaises(ValueError):
                    self.grid.place_tetromino(tetromino)

    def test_place_tetromino_with_overlap(self):
        """
        Test placing a new tetromino on top of an existing one.
        """
        self.grid.grid[19] = [(1, (255, 255, 255))] * 10
        tetromino = Tetromino([(0, 18), (1, 18), (2, 18), (3, 18)])  # I-shape
        self.grid.place_tetromino(tetromino)
        self.assertTrue(all(self.grid.grid[18][x] == (1, tetromino.get_color()) for x in range(4)))
        self.assertEqual(self.grid.grid[19][0], (1, (255, 255, 255)))

    def test_clear_rows(self):
        self.grid.grid[19] = [(1, (255, 255, 255))] * 10
        cleared_rows = self.grid.clear_rows()
        self.assertEqual(cleared_rows, 1)
        self.assertTrue(all(cell == (0, None) for cell in self.grid.grid[19]))
        self.assertEqual(len(self.grid.grid), 20)
        self.assertTrue(all(len(row) == 10 for row in self.grid.grid))

    def test_clear_multiple_rows(self):
        self.grid.grid[19] = [(1, (255, 255, 255))] * 10
        self.grid.grid[18] = [(1, (255, 255, 255))] * 10
        cleared_rows = self.grid.clear_rows()
        self.assertEqual(cleared_rows, 2)
        self.assertTrue(all(cell == (0, None) for cell in self.grid.grid[19]))
        self.assertTrue(all(cell == (0, None) for cell in self.grid.grid[18]))
        self.assertEqual(len(self.grid.grid), 20)
        self.assertTrue(all(len(row) == 10 for row in self.grid.grid))

    def test_clear_rows_with_boundaries(self):
        """
        Test clearing rows with boundary conditions to ensure correct row clearing.
        """
        self.grid.grid[19] = [(1, (255, 255, 255))] * 10
        self.grid.grid[18] = [(1, (255, 255, 255))] * 10
        self.grid.grid[17] = [(1, (255, 255, 255))] * 10
        cleared_rows = self.grid.clear_rows()
        self.assertEqual(cleared_rows, 3)
        self.assertTrue(all(cell == (0, None) for cell in self.grid.grid[19]))
        self.assertTrue(all(cell == (0, None) for cell in self.grid.grid[18]))
        self.assertTrue(all(cell == (0, None) for cell in self.grid.grid[17]))
        self.assertEqual(len(self.grid.grid), 20)

    def test_is_game_over(self):
        self.assertFalse(self.grid.is_game_over())
        self.grid.grid[0][0] = (1, (255, 255, 255))
        self.assertTrue(self.grid.is_game_over())

    def test_game_over_condition(self):
        for y in range(20):
            self.grid.grid[y][0] = (1, (255, 255, 255))
        self.assertTrue(self.grid.is_game_over())

    def test_game_over_non_filled_row(self):
        """
        Test that the game-over condition is not triggered by a partially filled row below the top row.
        """
        # Partially fill a row that is not the top row
        self.grid.grid[1] = [(1, (255, 255, 255))] * 9 + [(0, None)]
        # Ensure the top row is not filled
        self.grid.grid[0] = [(0, None)] * 10
        self.assertFalse(self.grid.is_game_over())  # Game should not be over


    def test_full_grid(self):
        """
        Test if the grid correctly handles being completely filled.
        """
        self.grid.grid = [[(1, (255, 255, 255))] * 10 for _ in range(20)]
        self.assertTrue(self.grid.is_game_over())

if __name__ == '__main__':
    unittest.main()
