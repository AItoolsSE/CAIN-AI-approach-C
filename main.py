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
FPS = 30
DROP_INTERVAL = 500  # Time in milliseconds between automatic drops

def main():
    try:
        # Initialize pygame
        pygame.init()

        # Create game objects
        game = Game(GRID_WIDTH, GRID_HEIGHT)
        keyboard_input = KeyboardInput()
        game_screen = MainGameScreen(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
        control_panel = ControlPanel(game, CELL_SIZE, GRID_WIDTH)

        # Set up the clock for managing frame rate
        clock = pygame.time.Clock()
        last_drop_time = pygame.time.get_ticks()

        while True:
            try:
                # Handle events
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    # Handle control panel events
                    control_panel.handle_events(event)

                # Handle keyboard input
                keyboard_input.handle_events(events)

                if game.is_paused:
                    continue

                # Automatic drop
                current_time = pygame.time.get_ticks()
                if current_time - last_drop_time > DROP_INTERVAL:
                    game.tetromino.move('down', game.grid)
                    last_drop_time = current_time

                # Update game state
                game.update(keyboard_input)

                # Check for game over
                if game.grid.is_game_over():
                    print("Game Over")
                    pygame.quit()
                    sys.exit()

                # Update display
                game_screen.update(game.grid, game.tetromino)
                control_panel.update(game.is_paused)

                # Draw everything
                game_screen.screen.fill((0, 0, 0))  # Clear screen
                game_screen.draw_grid(game.grid)
                game_screen.draw_tetromino(game.tetromino)
                control_panel.draw(game_screen.screen)

                # Update the display
                pygame.display.flip()

                # Cap the frame rate
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
