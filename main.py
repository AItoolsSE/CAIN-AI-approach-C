import pygame
import sys
from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino
from input_handler.keyboard_input import KeyboardInput
from ui.main_game_screen import MainGameScreen
from ui.control_panel import ControlPanel
from game_engine.score_manager import ScoreManager

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
        grid = Grid(GRID_WIDTH, GRID_HEIGHT)
        tetromino = Tetromino()
        score_manager = ScoreManager()
        keyboard_input = KeyboardInput()
        game_screen = MainGameScreen(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
        control_panel = ControlPanel(score_manager)

        # Set up the clock for managing frame rate
        clock = pygame.time.Clock()

        # Game state variables
        game_state = 'playing'  # Other states could be 'paused' or 'game_over'

        while True:
            try:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    # Handle control panel events
                    control_panel.handle_events(event)

                    # Toggle game state with Esc key
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        if game_state == 'playing':
                            game_state = 'paused'
                        elif game_state == 'paused':
                            game_state = 'playing'

                if game_state == 'playing':
                    # Handle keyboard input
                    keyboard_input.handle_events()

                    # Game logic
                    if keyboard_input.is_key_pressed('left'):
                        tetromino.move('left', GRID_WIDTH, GRID_HEIGHT)
                    if keyboard_input.is_key_pressed('right'):
                        tetromino.move('right', GRID_WIDTH, GRID_HEIGHT)
                    if keyboard_input.is_key_pressed('down'):
                        tetromino.move('down', GRID_WIDTH, GRID_HEIGHT)
                    if keyboard_input.is_key_pressed('rotate'):
                        tetromino.rotate(GRID_WIDTH, GRID_HEIGHT)
                    if keyboard_input.is_key_pressed('drop'):
                        # Move Tetromino down until it cannot move further
                        while not grid.place_tetromino(tetromino):
                            tetromino.move('down', GRID_WIDTH, GRID_HEIGHT)
                        rows_cleared = grid.clear_rows()
                        score_manager.add_points(rows_cleared)
                        tetromino = Tetromino()  # Generate a new Tetromino

                    # Check for game over
                    if grid.is_game_over():
                        game_state = 'game_over'

                # Update display
                game_screen.update(grid, tetromino)
                control_panel.update(game_state == 'paused')

                # Draw everything
                game_screen.screen.fill((0, 0, 0))  # Clear screen
                game_screen.draw_grid(grid)
                game_screen.draw_tetromino(tetromino)

                # Only draw the control panel if the game is paused
                if game_state == 'paused':
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
