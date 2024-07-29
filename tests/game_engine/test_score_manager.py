# tests/game_engine/test_score_manager.py

import unittest
from game_engine.score_manager import ScoreManager

class TestScoreManager(unittest.TestCase):
    def setUp(self):
        self.score_manager = ScoreManager()

    def test_score_initialization(self):
        self.assertEqual(self.score_manager.get_score(), 0)

    def test_add_points_one_row(self):
        self.score_manager.add_points(1)
        self.assertEqual(self.score_manager.get_score(), 40)

    def test_add_points_two_rows(self):
        self.score_manager.add_points(2)
        self.assertEqual(self.score_manager.get_score(), 100)

    def test_add_points_three_rows(self):
        self.score_manager.add_points(3)
        self.assertEqual(self.score_manager.get_score(), 300)

    def test_add_points_four_rows(self):
        self.score_manager.add_points(4)
        self.assertEqual(self.score_manager.get_score(), 1200)

    def test_add_points_multiple_times(self):
        self.score_manager.add_points(1)
        self.score_manager.add_points(2)
        self.score_manager.add_points(3)
        self.score_manager.add_points(4)
        self.assertEqual(self.score_manager.get_score(), 1640)

if __name__ == '__main__':
    unittest.main()
