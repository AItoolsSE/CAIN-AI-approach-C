import pygame
import sys
from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino
from input_handler.keyboard_input import KeyboardInput
from ui.main_game_screen import MainGameScreen
from ui.control_panel import ControlPanel
from ui.game_over_screen import GameOverScreen  # Import GameOverScreen
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
        # Initialize pygame
        pygame.init()

        # Create game objects
        game_screen = MainGameScreen(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
        control_panel = ControlPanel(None, CELL_SIZE, GRID_WIDTH)
        game = Game(GRID_WIDTH, GRID_HEIGHT, control_panel)
        control_panel.game = game  # Set the game instance in the control panel
        game_over_screen = GameOverScreen(game_screen.screen.get_width(), game_screen.screen.get_height())  # Initialize GameOverScreen
        keyboard_input = KeyboardInput()

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

                    # Handle pause event
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        game.toggle_pause()

                    if game.game_over:
                        action = game_over_screen.handle_events(event)
                        if action == 'restart':
                            game.start_new_game()
                            game.game_over = False
                        elif action == 'exit':
                            pygame.quit()
                            sys.exit()

                # If game is over, skip updating game state
                if game.game_over:
                    game_over_screen.display(game_screen.screen, game.score_manager.get_score())
                    pygame.display.flip()  # Update the display
                    continue

                # Handle keyboard input
                keyboard_input.handle_events(events)

                if game.is_paused:
                    control_panel.update()  # Update the control panel
                    control_panel.draw(game_screen.screen)  # Draw the control panel
                    pygame.display.flip()  # Update the display
                    continue

                current_time = pygame.time.get_ticks()

                # Automatic drop
                if current_time - last_drop_time > DROP_INTERVAL:
                    if not game.tetromino.move('down', game.grid):
                        game.grid.place_tetromino(game.tetromino)
                        rows_cleared = game.grid.clear_rows()
                        game.score_manager.add_points(rows_cleared)
                        control_panel.update()  # Update the control panel
                        game.tetromino = Tetromino()
                        if game.grid.is_game_over():
                            game.game_over = True
                    last_drop_time = current_time

                # Controlled key press handling
                if keyboard_input.is_key_pressed('left'):
                    game.tetromino.move('left', game.grid)
                if keyboard_input.is_key_pressed('right'):
                    game.tetromino.move('right', game.grid)
                if keyboard_input.is_key_pressed('down'):
                    if not game.tetromino.move('down', game.grid):
                        game.grid.place_tetromino(game.tetromino)
                        rows_cleared = game.grid.clear_rows()
                        game.score_manager.add_points(rows_cleared)
                        control_panel.update()  # Update the control panel
                        game.tetromino = Tetromino()
                        if game.grid.is_game_over():
                            game.game_over = True
                if keyboard_input.is_key_pressed('rotate'):
                    game.tetromino.rotate(game.grid)
                if keyboard_input.is_key_pressed('drop'):
                    while game.tetromino.move('down', game.grid):
                        pass
                    game.grid.place_tetromino(game.tetromino)
                    rows_cleared = game.grid.clear_rows()
                    game.score_manager.add_points(rows_cleared)
                    control_panel.update()  # Update the control panel
                    game.tetromino = Tetromino()
                    if game.grid.is_game_over():
                        game.game_over = True

                # Update game state
                game.update(keyboard_input)

                # Check for game over
                if game.grid.is_game_over():
                    game.game_over = True

                # Update display
                game_screen.update(game.grid, game.tetromino)
                control_panel.update()  # Update the control panel

                # Draw everything
                game_screen.screen.fill((0, 0, 0))  # Clear screen
                game_screen.draw_grid(game.grid)
                game_screen.draw_tetromino(game.tetromino)
                control_panel.draw(game_screen.screen)  # Draw the control panel

                if game.game_over:
                    game_over_screen.display(game_screen.screen, game.score_manager.get_score())

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
