Tetris Game
Overview
This is a Tetris game implemented in Python, featuring a comprehensive game engine, user interface, sound management, input handling, and persistence for saving progress and high scores.

High-Level Architectural Design
Major Components
Game Engine

Description: Manages the game state and interactions between components.
Subcomponents:
Tetromino Manager: Handles the creation and movement of tetromino pieces.
Grid Manager: Manages the game grid and checks for completed lines.
Level Manager: Manages game levels and progression.
Score Manager: Calculates and updates the player's score.
User Interface (UI)

Description: Displays the game elements and controls.
Subcomponents:
Main Game Screen: Displays the game grid and current tetromino.
Control Panel: Shows game controls and current score.
Game Over Screen: Displays when the game is over.
Settings Menu: Allows users to adjust game settings.
Input Handler

Description: Manages user inputs and custom controls.
Subcomponents: (Details about specific input handling can be added here)
Sound Manager

Description: Handles sound effects and background music.
Subcomponents: (Details about specific sound management can be added here)
Persistence Manager

Description: Saves and loads player progress and high scores.
Subcomponents: (Details about specific persistence management can be added here) 