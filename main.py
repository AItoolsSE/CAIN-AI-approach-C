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

        DROP_INTERVAL = game.level_manager.get_current_speed()

        while True:
            try:
                screen.fill((0, 0, 0))  # Clear screen at the start of each loop
                
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    # Handle events based on whether the settings menu is open or not
                    if game.is_settings_open:
                        settings_menu.handle_events(event)
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                            game.toggle_settings()  # Allow closing the settings menu with 'S'
                            continue  # Skip the rest of the loop to close the menu properly

                    control_panel.handle_events(event)

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        game.toggle_pause()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                        game.toggle_settings()  # Toggle settings menu

                # If settings menu is open, draw the semi-transparent overlay and the settings menu
                if game.is_settings_open:
                    # Draw the game behind the settings menu
                    game_screen.update(game.grid, game.tetromino)
                    control_panel.update()
                    game_screen.draw_grid(game.grid)
                    game_screen.draw_tetromino(game.tetromino)
                    control_panel.draw(screen)

                    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 180))  # Black with 180/255 transparency
                    screen.blit(overlay, (0, 0))  # Blit the overlay onto the screen
                    settings_menu.draw(screen)  # Draw the settings menu on top

                else:
                    # Game logic when the settings menu is not open
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
                    else:
                        keyboard_input.handle_events(events)

                        if game.is_paused:
                            control_panel.update()
                            control_panel.draw(screen)
                        else:
                            current_time = pygame.time.get_ticks()

                            if game.level_manager.update(game.score_manager.get_score()):
                                DROP_INTERVAL = game.level_manager.get_current_speed()
                                control_panel.update()

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

                            game_screen.update(game.grid, game.tetromino)
                            control_panel.update()
                            game_screen.draw_grid(game.grid)
                            game_screen.draw_tetromino(game.tetromino)
                            control_panel.draw(screen)

                pygame.display.flip()  # Only one call to flip at the end of the loop
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

