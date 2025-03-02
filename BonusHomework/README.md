# Escape the Fall - 3D Adventure Game

**Escape the Fall** is a 3D adventure game created using the **Godot Engine**. In the game, you control a fox navigating a park to collect hidden coins before time runs out. The challenge is to collect all coins within the time limit. If the time runs out before all coins are collected, the player will experience a "fall-through-floor" game over effect.

## Game Features

- **Player Movement**: The player can move in four directions (forward, backward, left, right), jump, and sprint.
- **Camera Control**: The camera follows the player and allows for free movement.
- **Coin Collection**: The player must collect coins scattered throughout the park.
- **Timer System**: The player is given a limited amount of time to collect all the coins, with a visual warning when time is running out.
- **Game Over**: If the timer reaches zero before all coins are collected, the player experiences a "fall-through-floor" effect, signaling the end of the game.

## Gameplay

- **Movement**: Use the **AWSD** keys for basic movement, and **X** to sprint.
- **Jumping**: Press **SPACE** to jump, and press **SPACE** again to perform a double jump.
- **Camera Control**: Use the **middle mouse button** to move the camera around.
- **Coin Collection**: Collect all the hidden coins scattered throughout the park before the timer runs out.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/mblerona/Video-Games-Programming/tree/main/BonusHomework
    ```
2. Open the project in **Godot Engine**.

## Project Structure

- **Main Player**: Controls the fox's movement and animations (walking, running, and jumping).
- **Park**: The park environment is built using Godot’s Grid Map, with physics and collisions enabled for interaction.
- **Coin**: Coins are placed around the park, and the player can collect them. Each coin has a collision shape for interaction with the player.
- **Menus**: The game features a start menu and end game menu with buttons for starting the game, restarting, or quitting.
- **Timer and Treasure Count**: A countdown timer is displayed, and the treasure count increases as the player collects coins.

## Game Logic

- **Timer**: The timer starts when the player begins the game, with a visual warning when there are 5 seconds left. If time runs out, the game ends.
- **Coin Collection**: When the player collects all required coins, the game ends and displays a win message.
- **Game Over**: If the player runs out of time before collecting all the coins, they fall through the floor and the game ends.

## References

- [Mixamo](https://www.mixamo.com/)
- [Sketchfab](https://sketchfab.com/)
- [Kenney](https://kenney.nl/)
- [Blender](https://www.blender.org/)

## Screenshots

- **Start Menu**  
- **Game UI with Timer and Treasure Count**
- **End Game Menu**


## GitHub Repository

Visit the project on GitHub:  
[Escape the Fall - GitHub](https://github.com/mblerona/Video-Games-Programming/tree/main/BonusHomework)

---

Enjoy the game, and feel free to contribute!
