# main.py

import pygame
import sys
from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino
from input_handler.keyboard_input import KeyboardInput
from ui.main_game_screen import MainGameScreen
from ui.control_panel import ControlPanel
from game_engine.score_manager import ScoreManager
from game_engine.game import Game

# Game settings
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
FPS = 60
DROP_INTERVAL = 750  # Time in milliseconds between automatic drops

def main():
    try:
        pygame.init()
        game = Game(GRID_WIDTH, GRID_HEIGHT)
        keyboard_input = KeyboardInput()
        game_screen = MainGameScreen(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
        control_panel = ControlPanel(game, CELL_SIZE, GRID_WIDTH)

        clock = pygame.time.Clock()
        last_drop_time = pygame.time.get_ticks()

        while True:
            try:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    control_panel.handle_events(event)

                keyboard_input.handle_events(events)

                if game.is_paused:
                    continue

                current_time = pygame.time.get_ticks()

                if current_time - last_drop_time > DROP_INTERVAL:
                    if not game.tetromino.move('down', game.grid):
                        game.grid.place_tetromino(game.tetromino)
                        game.grid.clear_rows()
                        game.tetromino = Tetromino()
                    last_drop_time = current_time

                if keyboard_input.is_key_pressed('left'):
                    game.tetromino.move('left', game.grid)
                if keyboard_input.is_key_pressed('right'):
                    game.tetromino.move('right', game.grid)
                if keyboard_input.is_key_pressed('down'):
                    if not game.tetromino.move('down', game.grid):
                        game.grid.place_tetromino(game.tetromino)
                        game.grid.clear_rows()
                        game.tetromino = Tetromino()
                if keyboard_input.is_key_pressed('rotate'):
                    game.tetromino.rotate(game.grid)
                if keyboard_input.is_key_pressed('drop'):
                    while game.tetromino.move('down', game.grid):
                        pass
                    game.grid.place_tetromino(game.tetromino)
                    game.grid.clear_rows()
                    game.tetromino = Tetromino()

                game.update(keyboard_input)

                if game.grid.is_game_over():
                    print("Game Over")
                    pygame.quit()
                    sys.exit()

                game_screen.update(game.grid, game.tetromino)
                control_panel.update(game.is_paused)
                game_screen.screen.fill((0, 0, 0))
                game_screen.draw_grid(game.grid)
                game_screen.draw_tetromino(game.tetromino)
                control_panel.draw(game_screen.screen)

                pygame.display.flip()
                clock.tick(FPS)

            except Exception as e:
                print(f"An error occurred: {e}")
                pygame.quit()
                sys.exit()

    except Exception as e:
        print(f"Failed to initialize game: {e}")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
