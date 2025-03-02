# Color Fill Puzzle Game

**Color Fill Puzzle** is a challenging puzzle game where players must fill a 5x5 grid with four distinct colors. The goal is to fill all empty cells on the board while following the rule that no two adjacent cells (horizontally or vertically) can share the same color. The game becomes more difficult as the player progresses through multiple levels, with decreasing time limits and increasingly complex grid configurations.

## Game Features

- **Grid and Colors**: The game board consists of a 5x5 grid, with cells that can hold one of four colors: Green, Pink, Violet, and Yellow.
- **Color Palette**: Players can select one of the four colors from the palette at the bottom of the screen.
- **Adjacency Rules**: No two adjacent cells can share the same color, requiring players to think strategically.
- **Time Limits**: Each level has a time limit, which gradually decreases as the player progresses through the game.
- **Valid Moves**: Players click on empty squares and select a color from the palette, ensuring no adjacent cells share the same color.

## Gameplay

1. **Start the Game**: Press **P** to begin the game.
2. **Select a Color**: Choose a color from the color palette at the bottom of the screen.
3. **Fill the Grid**: Click on empty squares to fill them with the selected color, ensuring no two adjacent cells have the same color.
4. **Level Progression**: The game progresses to the next level after successfully completing a grid. The difficulty increases with each level.
5. **Game Over/Win**: The game ends if the player runs out of time, has no valid moves left, or if the player doesn't use all four colors. The game is won by filling the grid with valid colors within the time limit.

## Levels

- **Level 1**: 80% of the grid is pre-filled, and players have 40 seconds to complete the grid.
- **Level 2**: 50% of the grid is pre-filled, and players have 30 seconds to complete the grid.
- **Level 3**: The grid is completely empty, and players have 20 seconds to fill the entire grid.

## Constraints

The game is lost if:
- The player runs out of time.
- The player has no valid moves left.
- The player doesn't use all four colors to fill the board. If the grid is filled but fewer than four colors are used, the game continues until the time runs out.

## Additional Features

- **Time Tracking**: After finishing the game, players can view their completion times for each level by pressing the **2** key.
- **Invalid Move**: If the player tries to place a color in an adjacent square where the color already exists, the move is invalid, and the square remains empty.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    ```
2. Install the required dependencies (assuming you have Python and Pygame installed):
    ```bash
    pip install pygame
    ```
3. Run the game:
    ```bash
    python color_fill_puzzle.py
    ```

## Code Overview

The game is built using **Pygame** and includes the following core components:
- **Board Setup and Initialization**: The game starts by setting up a 5x5 grid with some pre-filled squares.
- **Color Palette**: A palette with four selectable colors is rendered at the bottom of the screen.
- **Game Logic**: Includes the logic for filling the grid, checking for valid moves, and managing the time limit.
- **Levels and Difficulty**: The game has multiple levels with progressively decreasing time limits and increasingly complex grid configurations.
- **Game Over and Win Screens**: At the end of each level, the game displays a message indicating whether the player won or lost.

## Acknowledgments

- Pygame for providing the game development framework.
- The idea for the Color Fill Puzzle is based on classic logic puzzle games.

---

Enjoy!
