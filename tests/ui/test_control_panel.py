# tests/ui/test_control_panel.py

import pygame
import unittest
from unittest.mock import Mock
from ui.control_panel import ControlPanel  # Adjusted import path

class TestControlPanel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize pygame once for all tests
        pygame.init()

    def setUp(self):
        # Mock the game object and its methods
        self.game = Mock()
        self.game.get_score = Mock(return_value=123)
        self.game.is_paused = Mock(return_value=False)

        # Create a ControlPanel instance
        self.control_panel = ControlPanel(self.game)

    def test_update_labels(self):
        """
        Test that labels are updated correctly based on game state.
        """
        # Call the update method to refresh labels
        self.control_panel.update()
        
        # Create a surface to render the expected text
        font = pygame.font.Font(None, 36)  # Use the same font and size
        expected_score_surface = font.render("Score: 123", True, (255, 255, 255))
        expected_status_surface = font.render("Game Status: Running", True, (255, 255, 255))
        
        # Check if the score label surface matches the expected surface
        score_label_surface = self.control_panel.score_label.image
        status_label_surface = self.control_panel.status_label.image

        # Compare the pixels of the expected and actual surfaces
        self.assertTrue(self.compare_surfaces(score_label_surface, expected_score_surface),
                        "Score label text does not match expected value.")
        self.assertTrue(self.compare_surfaces(status_label_surface, expected_status_surface),
                        "Status label text does not match expected value.")

    def compare_surfaces(self, surface1, surface2):
        """
        Compare two pygame surfaces pixel by pixel.
        """
        if surface1.get_size() != surface2.get_size():
            return False
        
        # Compare pixel data
        pixels1 = pygame.surfarray.array3d(surface1)
        pixels2 = pygame.surfarray.array3d(surface2)
        
        return (pixels1 == pixels2).all()

    def tearDown(self):
        # Clean up pygame after tests
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
