# game_engine/level_manager.py

class LevelManager:
    def __init__(self, points_per_level=40, speed_increment=100, base_speed=750):
        self.level = 1
        self.points_per_level = points_per_level
        self.speed_increment = speed_increment
        self.base_speed = base_speed
        print("LevelManager initialized")  # Debugging print statement

    def update(self, current_points):
        """Update the level based on the player's current score."""
        # Calculate the expected level based on the score
        new_level = (current_points // self.points_per_level) + 1
        if new_level > self.level:
            self.level = new_level
            print(f"self.level {self.level}")  # Debugging print statement
            print(f"new_level {new_level}")  # Debugging print statement
            return True
        #else:
            #print(f"No level change: current level is {self.level}")  # Added debug print
        return False

    def get_current_speed(self):
        """Get the current drop speed based on the level."""
        new_speed = max(self.base_speed - (self.level - 1) * self.speed_increment, 100)
        print(f"speed: {new_speed}")
        return new_speed  # Minimum speed cap

    def get_level(self):
        """Return the current level."""
        return self.level
