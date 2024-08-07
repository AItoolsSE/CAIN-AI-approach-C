# game_engine/grid_manager.py

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[(0, None)] * width for _ in range(height)]

    def is_valid_position(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.grid[y][x][0] == 0

    def place_tetromino(self, tetromino):
        blocks = tetromino.get_blocks()
        color = tetromino.get_color()
        for x, y in blocks:
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                raise ValueError("Position out of bounds")
            self.grid[y][x] = (1, color)

    def clear_rows(self):
        rows_to_clear = [i for i, row in enumerate(self.grid) if all(cell[0] == 1 for cell in row)]
        for row in rows_to_clear:
            del self.grid[row]
            self.grid.insert(0, [(0, None)] * self.width)
        return len(rows_to_clear)

    def is_game_over(self):
        return any(self.grid[0][x][0] == 1 for x in range(self.width))
