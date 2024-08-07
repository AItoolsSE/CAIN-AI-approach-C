#tests/ui/test_control_panel.py
import sys
import os

# Ensure the base directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest
import pygame
from ui.control_panel import ControlPanel
from unittest.mock import Mock

class TestControlPanel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.mock_game = Mock()
        self.screen = pygame.display.set_mode((800, 600))
        self.control_panel = ControlPanel(self.mock_game, 30, 10)
    
    def test_create_button(self):
        button = self.control_panel.create_button((150, 50), (255, 0, 0), (10, 10), "Test")
        self.assertEqual(button.image.get_size(), (150, 50))
        self.assertEqual(button.default_color, (255, 0, 0))
        self.assertEqual(button.text, "Test")
    
    def test_create_label(self):
        label = self.control_panel.create_label('Score: 0', (10, 10), self.control_panel.font)
        self.assertIsInstance(label.image, pygame.Surface)
        self.assertEqual(label.rect.topleft, (10, 10))
    
    def test_handle_events_start_button(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.control_panel.start_button.rect.topleft})
        self.control_panel.handle_events(event)
        self.mock_game.start_new_game.assert_called_once()
    
    def test_handle_events_pause_button(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.control_panel.pause_button.rect.topleft})
        self.control_panel.handle_events(event)
        self.mock_game.toggle_pause.assert_called_once()
    
    def test_handle_events_settings_button(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.control_panel.settings_button.rect.topleft})
        self.control_panel.handle_events(event)
        self.mock_game.open_settings.assert_called_once()
    
    def test_handle_events_high_scores_button(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': self.control_panel.high_scores_button.rect.topleft})
        self.control_panel.handle_events(event)
        self.mock_game.view_high_scores.assert_called_once()
    
    def test_update(self):
        self.mock_game.get_score.return_value = 100
        self.control_panel.update()
        score_text = self.control_panel.font.render(f'Score: 100', True, (255, 255, 255))
        self.assertEqual(self.control_panel.score_label.image.get_rect(), score_text.get_rect())

    def test_draw(self):
        surface = pygame.Surface((800, 600))
        self.control_panel.draw(surface)
        self.assertEqual(surface.get_at(self.control_panel.start_button.rect.topleft), pygame.Color(0, 255, 0, 255))

if __name__ == '__main__':
    unittest.main()