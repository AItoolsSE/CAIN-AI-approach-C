#game_engine/high_scores_manager.py

import datetime

class HighScoresManager:
    def __init__(self, max_entries=5):
        self.max_entries = max_entries
        self.high_scores = []

    def add_score(self, score):
        """Add a new score to the high scores list with the current date-time."""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.high_scores.append((score, current_time))
        self.high_scores.sort(reverse=True, key=lambda x: x[0])  # Sort by score
        if len(self.high_scores) > self.max_entries:
            self.high_scores.pop()  # Remove the lowest score if exceeding max_entries

    def get_high_scores(self):
        """Return the list of top scores."""
        return self.high_scores

    def reset(self):
        """Clear the current session high scores."""
        self.high_scores = []
