# ui/main_game_screen.py

import pygame
from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino

class MainGameScreen:
    def __init__(self, grid_width, grid_height, cell_size):
        """
        Initialize the main game screen.

        Parameters:
            grid_width (int): The width of the game grid.
            grid_height (int): The height of the game grid.
            cell_size (int): The size of each cell in the grid.
        """
        pygame.init()
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((grid_width * cell_size + 200, grid_height * cell_size))  # Add space for the control panel
        pygame.display.set_caption("Tetris")

    def draw_grid(self, grid):
        """
        Draw the game grid on the screen.

        Parameters:
            grid (Grid): The game grid.
        """
        for y in range(grid.height):
            for x in range(grid.width):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if grid.grid[y][x] == 0:
                    pygame.draw.rect(self.screen, (0, 0, 0), rect)  # Draw empty cell
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)  # Draw filled cell
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)  # Draw grid lines on top of the cells

    def draw_tetromino(self, tetromino):
        """
        Draw the current tetromino on the screen.

        Parameters:
            tetromino (Tetromino): The current tetromino.
        """
        for x, y in tetromino.get_blocks():
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, tetromino.color, rect)
            pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)  # Draw grid lines on top of the tetromino blocks

    def update(self, grid, tetromino):
        """
        Update the display with the current game state.

        Parameters:
            grid (Grid): The game grid.
            tetromino (Tetromino): The current tetromino.
        """
        self.screen.fill((0, 0, 0))
        self.draw_grid(grid)
        self.draw_tetromino(tetromino)
        pygame.display.flip()

    def quit(self):
        """
        Quit the game and close the display.
        """
        pygame.quit()
