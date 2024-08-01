import pygame
import sys
from game_engine.game import Game
from input_handler.keyboard_input import KeyboardInput
from ui.main_game_screen import MainGameScreen
from ui.control_panel import ControlPanel

# Game settings
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
FPS = 30

def main():
    try:
        # Initialize pygame
        pygame.init()

        # Create game objects
        game = Game(GRID_WIDTH, GRID_HEIGHT)
        keyboard_input = KeyboardInput()
        game_screen = MainGameScreen(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
        control_panel = ControlPanel(game)

        # Set up the clock for managing frame rate
        clock = pygame.time.Clock()

        # Game state variables
        game_state = 'playing'  # Other states could be 'paused' or 'game_over'
        fall_time = 0
        fall_speed = 0.5  # Tetromino falls every 0.5 seconds

        while True:
            try:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_state = 'paused' if game_state == 'playing' else 'playing'
                            game.toggle_pause()

                    # Handle control panel events
                    if game_state == 'paused':
                        control_panel.handle_events(event)

                if game_state == 'playing':
                    # Handle keyboard input
                    keyboard_input.handle_events()

                    # Update game state
                    game.update(keyboard_input)

                    # Automatic tetromino fall
                    fall_time += clock.get_rawtime()
                    if fall_time / 1000 >= fall_speed:
                        game.tetromino.move('down', game.grid.width, game.grid.height)
                        fall_time = 0

                    # Check for game over
                    if game.grid.is_game_over():
                        game_state = 'game_over'

                # Update display
                game_screen.update(game.grid, game.tetromino)

                # Draw everything
                game_screen.screen.fill((0, 0, 0))  # Clear screen
                game_screen.draw_grid(game.grid)
                game_screen.draw_tetromino(game.tetromino)

                if game_state == 'paused':
                    control_panel.update(is_paused=True)
                    control_panel.draw(game_screen.screen)
                else:
                    control_panel.update(is_paused=False)

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
