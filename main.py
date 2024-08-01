# main.py

import pygame
import sys
from game_engine.game import Game
from input_handler.keyboard_input import KeyboardInput
from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino
from ui.main_game_screen import MainGameScreen
from ui.control_panel import ControlPanel

# Game settings
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
FPS = 60
FALL_SPEED = 1.0  # Tetromino falls every 1 second

def main():
    pygame.init()

    # Create game objects
    game = Game(GRID_WIDTH, GRID_HEIGHT)
    keyboard_input = KeyboardInput()
    game_screen = MainGameScreen(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
    control_panel = ControlPanel(game)

    clock = pygame.time.Clock()
    game_state = 'playing'
    fall_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Exit cleanly if the window is closed

            # Handle keyboard input events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = 'paused' if game_state == 'playing' else 'playing'
                    game.toggle_pause()

            keyboard_input.handle_event(event)  # Update keyboard input state

        if game_state == 'playing':
            # Update game state based on keyboard input with cooldowns
            if keyboard_input.is_key_pressed('left', current_time):
                game.tetromino.move('left', game.grid.width, game.grid.height)
            if keyboard_input.is_key_pressed('right', current_time):
                game.tetromino.move('right', game.grid.width, game.grid.height)
            if keyboard_input.is_key_pressed('down', current_time):
                game.tetromino.move('down', game.grid.width, game.grid.height)
            if keyboard_input.is_key_pressed('rotate', current_time):
                game.tetromino.rotate(game.grid.width, game.grid.height)
            if keyboard_input.is_key_pressed('drop', current_time):
                while game.grid.is_valid_position(game.tetromino):
                    game.tetromino.move('down', game.grid.width, game.grid.height)
                game.grid.place_tetromino(game.tetromino)
                rows_cleared = game.grid.clear_rows()
                game.score_manager.add_points(rows_cleared)
                game.tetromino = Tetromino()  # Generate a new Tetromino
                if not game.grid.is_valid_position(game.tetromino):
                    game_state = 'game_over'

            # Automatic tetromino fall
            if (current_time - fall_time) / 1000 >= FALL_SPEED:
                game.tetromino.move('down', game.grid.width, game.grid.height)
                if not game.grid.is_valid_position(game.tetromino):
                    game.tetromino.move('up', game.grid.width, game.grid.height)  # Move back up
                    game.grid.place_tetromino(game.tetromino)
                    rows_cleared = game.grid.clear_rows()
                    game.score_manager.add_points(rows_cleared)
                    game.tetromino = Tetromino()  # Generate a new Tetromino
                    if not game.grid.is_valid_position(game.tetromino):
                        game_state = 'game_over'
                fall_time = current_time

        # Update game screen and control panel
        game_screen.update(game.grid, game.tetromino)
        game_screen.screen.fill((0, 0, 0))  # Clear screen
        game_screen.draw_grid(game.grid)
        game_screen.draw_tetromino(game.tetromino)

        if game_state == 'paused':
            control_panel.update(is_paused=True)
            control_panel.draw(game_screen.screen)
        else:
            control_panel.update(is_paused=False)
            control_panel.draw(game_screen.screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
