# tests/game_engine/test_grid_manager.py

import unittest
from game_engine.grid_manager import Grid

class Tetromino:
    def __init__(self, blocks):
        self.blocks = blocks

    def get_blocks(self):
        return self.blocks

class TestGridManager(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(10, 20)

    def test_grid_initialization(self):
        self.assertEqual(len(self.grid.grid), 20)
        self.assertTrue(all(len(row) == 10 for row in self.grid.grid))
        self.assertTrue(all(cell == 0 for row in self.grid.grid for cell in row))

    def test_place_tetromino_empty_grid(self):
        tetromino = Tetromino([(0, 0), (1, 0), (2, 0), (3, 0)])  # I-shape
        self.grid.place_tetromino(tetromino)
        self.assertTrue(all(self.grid.grid[0][x] == 1 for x in range(4)))

    def test_place_tetromino_partially_filled_grid(self):
        self.grid.grid[19][0] = 1
        tetromino = Tetromino([(0, 18), (1, 18), (2, 18), (3, 18)])  # I-shape
        self.grid.place_tetromino(tetromino)
        self.assertTrue(all(self.grid.grid[18][x] == 1 for x in range(4)))
        self.assertEqual(self.grid.grid[19][0], 1)

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
                try:
                    self.grid.place_tetromino(tetromino)
                except ValueError:
                    pass  # Expected outcome
                else:
                    self.fail(f"{shape_name} should raise ValueError")

    def test_clear_rows(self):
        self.grid.grid[19] = [1] * 10
        cleared_rows = self.grid.clear_rows()
        self.assertEqual(cleared_rows, 1)
        self.assertTrue(all(cell == 0 for cell in self.grid.grid[19]))
        self.assertEqual(len(self.grid.grid), 20)
        self.assertTrue(all(len(row) == 10 for row in self.grid.grid))

    def test_clear_multiple_rows(self):
        self.grid.grid[19] = [1] * 10
        self.grid.grid[18] = [1] * 10
        cleared_rows = self.grid.clear_rows()
        self.assertEqual(cleared_rows, 2)
        self.assertTrue(all(cell == 0 for cell in self.grid.grid[19]))
        self.assertTrue(all(cell == 0 for cell in self.grid.grid[18]))
        self.assertEqual(len(self.grid.grid), 20)
        self.assertTrue(all(len(row) == 10 for row in self.grid.grid))

    def test_is_game_over(self):
        self.assertFalse(self.grid.is_game_over())
        self.grid.grid[0][0] = 1
        self.assertTrue(self.grid.is_game_over())

    def test_game_over_condition(self):
        for y in range(20):
            self.grid.grid[y][0] = 1
        self.assertTrue(self.grid.is_game_over())

if __name__ == '__main__':
    unittest.main()
