# game_engine/tetromino_manager.py

import random

class Tetromino:
    SHAPES = {
        'I': [(0, 1), (1, 1), (2, 1), (3, 1)],
        'O': [(1, 0), (2, 0), (1, 1), (2, 1)],
        'T': [(1, 0), (0, 1), (1, 1), (2, 1)],
        'S': [(1, 0), (2, 0), (0, 1), (1, 1)],
        'Z': [(0, 0), (1, 0), (1, 1), (2, 1)],
        'J': [(0, 0), (0, 1), (1, 1), (2, 1)],
        'L': [(2, 0), (0, 1), (1, 1), (2, 1)]
    }

    def __init__(self, shape=None):
        self.shape = shape or random.choice(list(self.SHAPES.keys()))
        self.blocks = self.SHAPES[self.shape]
        self.position = (3, 0)  # Starting position (x, y)

    def move(self, direction, grid_width, grid_height):
        x, y = self.position
        if direction == 'left' and all(bx + x - 1 >= 0 for bx, by in self.blocks):
            self.position = (x - 1, y)
        elif direction == 'right' and all(bx + x + 1 < grid_width for bx, by in self.blocks):
            self.position = (x + 1, y)
        elif direction == 'down' and all(by + y + 1 < grid_height for bx, by in self.blocks):
            self.position = (x, y + 1)

    def rotate(self, grid_width, grid_height):
        if self.shape != 'O':
            new_blocks = [(-y, x) for x, y in self.blocks]
            if all(0 <= bx + self.position[0] < grid_width and 0 <= by + self.position[1] < grid_height for bx, by in new_blocks):
                self.blocks = new_blocks

    def get_blocks(self):
        x, y = self.position
        return [(x + bx, y + by) for bx, by in self.blocks]
