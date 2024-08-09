import sys
import os

# Ensure the base directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
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

    def test_add_points_invalid_row_counts(self):
        """
        Test the handling of invalid row counts.
        """
        self.score_manager.add_points(-1)
        self.assertEqual(self.score_manager.get_score(), 0)  # Score should not change

        self.score_manager.add_points(5)
        self.assertEqual(self.score_manager.get_score(), 0)  # Score should not change

    def test_score_consistency(self):
        """
        Test that the score remains consistent after multiple add_points operations.
        """
        self.score_manager.add_points(1)
        self.score_manager.add_points(2)
        self.score_manager.add_points(3)
        self.score_manager.add_points(4)
        self.assertEqual(self.score_manager.get_score(), 1640)

        # Reset and test again
        self.score_manager = ScoreManager()
        self.score_manager.add_points(4)
        self.assertEqual(self.score_manager.get_score(), 1200)

    def test_score_overflow(self):
        """
        Test handling of very large scores to ensure no overflow issues.
        """
        self.score_manager = ScoreManager()
        for _ in range(1_000_000):  # Simulate many points additions
            self.score_manager.add_points(4)
        self.assertTrue(self.score_manager.get_score() > 0)  # Ensure the score is positive

if __name__ == '__main__':
    unittest.main()
