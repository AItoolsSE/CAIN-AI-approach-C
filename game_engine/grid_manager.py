# game_engine/grid_manager.py

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)]

    def place_tetromino(self, tetromino):
        blocks = tetromino.get_blocks()
        for x, y, _ in blocks:
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                print(f"Attempting to place tetromino out of bounds: ({x}, {y})")
                raise ValueError("Tetromino placement out of bounds.")
            self.grid[y][x] = 1

    def clear_rows(self):
        rows_to_clear = [i for i, row in enumerate(self.grid) if all(cell == 1 for cell in row)]
        for row in rows_to_clear:
            del self.grid[row]
            self.grid.insert(0, [0] * self.width)
        return len(rows_to_clear)

    def is_game_over(self):
        return any(self.grid[0][x] == 1 for x in range(self.width))

    def is_valid_position(self, tetromino):
        """
        Check if the tetromino is in a valid position on the grid.

        Parameters:
            tetromino (Tetromino): The tetromino to check.

        Returns:
            bool: True if the tetromino is in a valid position, False otherwise.
        """
        for x, y, _ in tetromino.get_blocks():
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return False
            if self.grid[y][x] == 1:
                return False
        return True
