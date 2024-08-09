import pygame
import sys
from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino
from input_handler.keyboard_input import KeyboardInput
from ui.main_game_screen import MainGameScreen
from ui.control_panel import ControlPanel
from ui.game_over_screen import GameOverScreen
from game_engine.score_manager import ScoreManager
from game_engine.game import Game

# Game settings
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
FPS = 60

def main():
    try:
        pygame.init()

        # Create game objects
        game_screen = MainGameScreen(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
        control_panel = ControlPanel(None, CELL_SIZE, GRID_WIDTH)
        game = Game(GRID_WIDTH, GRID_HEIGHT, control_panel)
        control_panel.game = game  # Set the game instance in the control panel
        game_over_screen = GameOverScreen(game_screen.screen.get_width(), game_screen.screen.get_height())
        keyboard_input = KeyboardInput()

        clock = pygame.time.Clock()
        last_drop_time = pygame.time.get_ticks()

        DROP_INTERVAL = game.level_manager.get_current_speed()  # Use the level manager from the Game instance

        while True:
            try:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    control_panel.handle_events(event)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        game.toggle_pause()

                    if game.game_over:
                        if not game.score_added:
                            game.high_scores_manager.add_score(game.get_score())
                            game.score_added = True
                        action = game_over_screen.handle_events(event)
                        if action == 'restart':
                            game.start_new_game()
                            game.game_over = False
                            DROP_INTERVAL = game.level_manager.get_current_speed()  # Reset drop interval
                        elif action == 'exit':
                            pygame.quit()
                            sys.exit()

                if game.game_over:
                    game_over_screen.display(game_screen.screen, game.score_manager.get_score())
                    pygame.display.flip()
                    continue

                keyboard_input.handle_events(events)

                if game.is_paused:
                    control_panel.update()
                    control_panel.draw(game_screen.screen)
                    pygame.display.flip()
                    continue

                current_time = pygame.time.get_ticks()

                if game.level_manager.update(game.score_manager.get_score()):
                    DROP_INTERVAL = game.level_manager.get_current_speed()
                    control_panel.update()
                    control_panel.draw(game_screen.screen)

                if current_time - last_drop_time > DROP_INTERVAL:
                    if not game.tetromino.move('down', game.grid):
                        game.grid.place_tetromino(game.tetromino)
                        rows_cleared = game.grid.clear_rows()
                        game.score_manager.add_points(rows_cleared)
                        control_panel.update()
                        game.tetromino = Tetromino()
                        if game.grid.is_game_over():
                            game.game_over = True
                    last_drop_time = current_time

                game.update(keyboard_input)

                if game.grid.is_game_over():
                    game.game_over = True

                game_screen.update(game.grid, game.tetromino)
                control_panel.update()

                game_screen.screen.fill((0, 0, 0))
                game_screen.draw_grid(game.grid)
                game_screen.draw_tetromino(game.tetromino)
                control_panel.draw(game_screen.screen)

                if game.game_over:
                    game_over_screen.display(game_screen.screen, game.score_manager.get_score())

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
