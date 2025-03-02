# Space Scavenger

**Space Scavenger** is a 2D space-themed arcade game where players control a spaceship to collect crystals, shoot asteroids, and avoid obstacles. The game challenges players to survive as long as possible, scoring points while avoiding increasing difficulty over time. The goal is to collect as many crystals as possible, survive waves of asteroids, and achieve a high score.

## Game Features

- **Dynamic Background**: A scrolling starfield that gives the effect of movement.
- **Power-ups**: Collect crystals to activate power-ups, including multi-shot lasers for a short duration.
- **Scaling Difficulty**: As the game progresses, asteroids increase in size, frequency, and speed. The spaceship also accelerates, upping the challenge.
- **Sound Effects and Music**: Engaging audio effects for background music, laser shooting, collisions, and power-ups.
- **Game Over Mechanism**: The game ends when the player's lives reach zero, but high scores are tracked.
- **Visual Effects**: Fading respawn effects when the spaceship has more than one life.

## Gameplay

1. **Collect Crystals**: Crystals boost your score and can trigger power-ups like multi-shot lasers.
2. **Avoid Asteroids**: Dodge or destroy asteroids to survive.
3. **Survive Waves**: As you progress, asteroids increase in size and frequency. The spaceship also accelerates to give you a better chance at survival.
4. **Achieve High Scores**: Compete for the highest score possible.

### Game Bonuses
- **Every 5 crystals**: Unlock a power-up (multi-shot lasers for 5 seconds).
- **300 points**: Unlock vertical movement (Up/Down) for the spaceship.
- **500 points**: Earn an extra life.

### Controls

- **Arrow Keys (Left/Right)**: Move the spaceship horizontally.
- **Arrow Keys (Up/Down)**: Move vertically (unlocked after reaching 300 points).
- **Spacebar**: Shoot lasers to destroy asteroids.
- **Escape**: Quit the game.

## Game Flow

- The game begins with the spaceship moving horizontally. As the player collects crystals and destroys asteroids, they unlock additional abilities.
- As the game progresses, asteroids increase in size, speed, and frequency. The player also speeds up, making the game more challenging.
- The game ends when the player loses all lives. High scores are tracked during gameplay.

## Implementation Details

- **Game Environment**: The game runs at an 800x600 resolution at 60 FPS, with dynamic background scrolling.
- **Player Movement and Shooting**: The player controls movement using arrow keys and shoots using the spacebar. Vertical movement unlocks after reaching 300 points.
- **Obstacles and Power-ups**: Asteroids scale over time, and crystals grant score bonuses and activate power-ups.
- **Collision Detection**: Implemented using Pygame's built-in sprite collision detection to handle interactions between the player, bullets, asteroids, and crystals.
- **Scaling Difficulty**: Asteroids increase in size, frequency, and speed as the game progresses. The spaceship also accelerates over time to increase the challenge.
- **Game Over and Restart**: Players can restart the game after losing without exiting. High scores persist across sessions.

## How to Install and Play

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
    python space_scavenger.py
    ```

## Code Overview

The game is developed using **Pygame** and includes the following main components:
- **Power-Ups**: Activate multi-shot lasers and provide bonus score through crystals.
- **Lives**: Start with one life and gain extra lives at certain score milestones.
- **Asteroids Scaling**: Asteroids grow in size and speed as the game progresses, with increased spawn frequency.
- **Main Game Loop**: Handles movement, object spawning, collision detection, and game over handling.



## Acknowledgments

- Pygame for providing the game development framework.
- The concept of Space Scavenger combines fast-paced arcade action with scaling difficulty.

---

Enjoy **Space Scavenger** and try to beat your high score!
