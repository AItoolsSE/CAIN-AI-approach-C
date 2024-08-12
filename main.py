import pygame
import sys
from game_engine.grid_manager import Grid
from game_engine.tetromino_manager import Tetromino
from input_handler.keyboard_input import KeyboardInput
from ui.main_game_screen import MainGameScreen
from ui.control_panel import ControlPanel
from ui.game_over_screen import GameOverScreen
from ui.settings_menu import SettingsMenu
from sound_manager.background_music import BackgroundMusicManager
from game_engine.score_manager import ScoreManager
from game_engine.game import Game
from game_engine.high_scores_manager import HighScoresManager  # Import HighScoresManager

# Game settings
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
FPS = 60
CONTROL_PANEL_WIDTH = 250

def main():
    try:
        pygame.init()

        # Calculate the total width of the game window
        total_window_width = (GRID_WIDTH * CELL_SIZE) + CONTROL_PANEL_WIDTH
        total_window_height = GRID_HEIGHT * CELL_SIZE

        # Set the game window size
        screen = pygame.display.set_mode((total_window_width, total_window_height))

        pygame.display.set_caption('Tetris')

        # Initialize background music
        background_music_manager = BackgroundMusicManager("sound_manager/assets/background_music.mp3")
        background_music_manager.play_music()

        # Create game objects
        game_screen = MainGameScreen(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, screen)
        control_panel = ControlPanel(None, CELL_SIZE, GRID_WIDTH)
        game = Game(GRID_WIDTH, GRID_HEIGHT, control_panel)
        high_scores_manager = HighScoresManager()
        game.high_scores_manager = high_scores_manager
        control_panel.game = game
        game_over_screen = GameOverScreen(total_window_width, total_window_height)
        keyboard_input = KeyboardInput()

        settings_menu = SettingsMenu(game, background_music_manager)

        clock = pygame.time.Clock()
        last_drop_time = pygame.time.get_ticks()

        # Initialize DROP_INTERVAL with the current level speed
        DROP_INTERVAL = game.level_manager.get_current_speed()

        settings_open = False

        while True:
            try:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    control_panel.handle_events(event)

                    if settings_open:
                        settings_menu.handle_events(event)
                        settings_menu.draw(screen)
                        pygame.display.flip()
                        continue

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        game.toggle_pause()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                        settings_open = not settings_open

                    if game.game_over:
                        if not game.score_added:
                            game.high_scores_manager.add_score(game.get_score())
                            game.score_added = True
                        action = game_over_screen.handle_events(event)
                        if action == 'restart':
                            game.start_new_game()
                            game.game_over = False
                            DROP_INTERVAL = game.level_manager.get_current_speed()
                        elif action == 'exit':
                            pygame.quit()
                            sys.exit()

                if game.game_over:
                    game_over_screen.display(screen, game.score_manager.get_score())
                    pygame.display.flip()
                    continue

                keyboard_input.handle_events(events)

                if game.is_paused:
                    control_panel.update()
                    control_panel.draw(screen)
                    pygame.display.flip()
                    continue

                current_time = pygame.time.get_ticks()

                # Check for level changes and update DROP_INTERVAL accordingly
                if game.level_manager.update(game.score_manager.get_score()):
                    DROP_INTERVAL = game.level_manager.get_current_speed()  # Update drop interval based on the new level
                    print(f"Level increased to {game.level_manager.get_level()}, new speed: {DROP_INTERVAL}")  # Debug print
                    control_panel.update()
                    
                # Move the Tetromino down at regular intervals
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

                screen.fill((0, 0, 0))
                game_screen.update(game.grid, game.tetromino)
                control_panel.update()
                control_panel.draw(screen)

                if game.game_over:
                    game_over_screen.display(screen, game.score_manager.get_score())

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