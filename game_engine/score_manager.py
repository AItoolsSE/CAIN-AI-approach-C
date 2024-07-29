# game_engine/score_manager.py

class ScoreManager:
    def __init__(self):
        """
        Initialize the score manager.
        """
        self.score = 0

    def add_points(self, rows_cleared):
        """
        Add points based on the number of rows cleared.

        Parameters:
            rows_cleared (int): The number of rows cleared.
        """
        points_for_rows = {
            1: 40,
            2: 100,
            3: 300,
            4: 1200
        }
        if rows_cleared in points_for_rows:
            self.score += points_for_rows[rows_cleared]

    def get_score(self):
        """
        Get the current score.

        Returns:
            int: The current score.
        """
        return self.score
