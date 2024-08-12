# ui/main_game_screen.py

import pygame

class MainGameScreen:
    def __init__(self, grid_width, grid_height, cell_size, screen):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.screen = screen  # Use the screen passed as an argument

    def draw_grid(self, grid):
        for y in range(grid.height):
            for x in range(grid.width):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if grid.grid[y][x][0] == 0:
                    pygame.draw.rect(self.screen, (0, 0, 0), rect)
                else:
                    pygame.draw.rect(self.screen, grid.grid[y][x][1], rect)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)

    def draw_tetromino(self, tetromino):
        for x, y in tetromino.get_blocks():
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, tetromino.color, rect)
            pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)

    def update(self, grid, tetromino):
        self.screen.fill((0, 0, 0))
        self.draw_grid(grid)
        self.draw_tetromino(tetromino)

    def quit(self):
        pygame.quit()
