import json
import os

class HighScoresPersistenceManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        """Load high scores from a JSON file."""
        try:
            with open(self.file_path, 'r') as file:
                high_scores = json.load(file)
                # Sort the high scores based on the score (in descending order)
                high_scores.sort(key=lambda x: x['score'], reverse=True)
                return high_scores
        except FileNotFoundError:
            return []

    def save_high_scores(self):
        """Save the high scores to a JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(self.high_scores, file)

    def add_high_score(self, score, date_time):
        """Add a new score to the high scores list, ensuring the list remains sorted and does not exceed 10 entries."""
        self.high_scores.append({"score": score, "date": date_time})
        self.high_scores = sorted(self.high_scores, key=lambda x: x["score"], reverse=True)[:10]
        self.save_high_scores()
        
    def get_top_high_score(self):
        """Get the top high score."""
        return self.high_scores[0] if self.high_scores else None

    def get_top_ten_high_scores(self):
        """Get the top 10 high scores."""
        return self.high_scores
