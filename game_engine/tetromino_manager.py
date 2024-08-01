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

    COLORS = {
        'I': (0, 255, 255),
        'O': (255, 255, 0),
        'T': (128, 0, 128),
        'S': (0, 255, 0),
        'Z': (255, 0, 0),
        'J': (0, 0, 255),
        'L': (255, 165, 0)
    }

    def __init__(self, shape=None):
        self.shape = shape or random.choice(list(self.SHAPES.keys()))
        self.blocks = self.SHAPES[self.shape]
        self.color = self.COLORS[self.shape]
        self.position = (3, 0)

    def move(self, direction, grid):
        x, y = self.position
        if direction == 'left' and all(grid.is_valid_position(bx + x - 1, by + y) for bx, by in self.blocks):
            self.position = (x - 1, y)
        elif direction == 'right' and all(grid.is_valid_position(bx + x + 1, by + y) for bx, by in self.blocks):
            self.position = (x + 1, y)
        elif direction == 'down' and all(grid.is_valid_position(bx + x, by + y + 1) for bx, by in self.blocks):
            self.position = (x, y + 1)

    def rotate(self, grid):
        if self.shape != 'O':
            new_blocks = [(-y, x) for x, y in self.blocks]
            if all(grid.is_valid_position(bx + self.position[0], by + self.position[1]) for bx, by in new_blocks):
                self.blocks = new_blocks

    def get_blocks(self):
        x, y = self.position
        return [(x + bx, y + by) for bx, by in self.blocks]
