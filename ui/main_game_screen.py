# ui/main_game_screen.py

import pygame
from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino

class MainGameScreen:
    def __init__(self, grid_width, grid_height, cell_size):
        pygame.init()
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((grid_width * cell_size, grid_height * cell_size))
        pygame.display.set_caption("Tetris")

    def draw_grid(self, grid):
        for y in range(grid.height):
            for x in range(grid.width):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if grid.grid[y][x] == 0:
                    pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)  # Darker grid lines for visibility
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)

    def draw_tetromino(self, tetromino):
        for x, y in tetromino.get_blocks():
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (255, 0, 0), rect)  # Red color for tetromino blocks

    def update(self, grid, tetromino):
        self.screen.fill((0, 0, 0))
        self.draw_grid(grid)
        self.draw_tetromino(tetromino)
        pygame.display.flip()

    def quit(self):
        pygame.quit()
