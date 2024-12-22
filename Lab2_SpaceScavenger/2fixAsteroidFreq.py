import pygame
import sys
import random
import os
import math

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init()

# Game Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Movement and Speed Settings
PLAYER_SPEED = 3
ASTEROID_SPEED = 3
CRYSTAL_SPEED = 2
BULLET_SPEED = 10
SPAWN_RATE = 60  # frames between spawns
SCROLL_SPEED = 2
NUM_STARS = 100

# Game Thresholds
VERTICAL_MOVEMENT_THRESHOLD = 10  # crystals needed for vertical movement
POWER_UP_THRESHOLD = 5  # crystals needed for power-up
EXTRA_LIFE_THRESHOLD = 100  # score needed for extra life
MAX_LIVES = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_BLUE = (100, 100, 255)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Scavenger")
clock = pygame.time.Clock()


# Asset Loading Functions
def load_image(name):
    """Load and return an image asset"""
    return pygame.image.load(os.path.join('assets', 'images', name)).convert_alpha()


def load_sound(name):
    """Load and return a sound asset"""
    return pygame.mixer.Sound(os.path.join('assets', 'sounds', name))


# Load all game assets
player_img = load_image('ship.png')
asteroid_img1 = load_image('asteroid.png')
asteroid_img2 = load_image('asteroid.png')
crystal_img = load_image('crystal.png')

# Load and configure all sounds
background_music = load_sound('background_music.wav')
crystal_sound = load_sound('317771__jalastram__sfx_powerup_01.wav')
laser_sound = load_sound('421704__bolkmar__sfx-laser-shoot-02.wav')
game_over_sound = load_sound('442127__euphrosyyn__8-bit-game-over.wav')
clash_sound = load_sound('clash_sound.wav')

# Adjust sound volumes
background_music.set_volume(0.4)
crystal_sound.set_volume(0.1)
laser_sound.set_volume(0.4)
game_over_sound.set_volume(0.8)
clash_sound.set_volume(0.4)


# Define all sprite classes first
class Star:
    """Represents a single star in the background"""

    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)
        self.speed = random.randint(2, 5)
        self.size = random.randint(1, 3)
        self.brightness = random.choice([WHITE, GRAY, LIGHT_BLUE])

    def move(self):
        """Update star position and reset if off screen"""
        self.y += self.speed
        if self.y > WINDOW_HEIGHT:
            self.y = 0
            self.x = random.randint(0, WINDOW_WIDTH)
            self.speed = random.randint(2, 5)


class Background:
    """Manages the starfield background"""

    def __init__(self):
        self.stars = [Star() for _ in range(NUM_STARS)]

    def update(self):
        """Update all stars in the background"""
        for star in self.stars:
            star.move()

    def draw(self, surface):
        """Draw the background with all stars"""
        surface.fill(BLACK)
        for star in self.stars:
            pygame.draw.circle(surface, star.brightness,
                               (star.x, star.y), star.size)


class Bullet(pygame.sprite.Sprite):
    """Represents a bullet fired by the player"""

    def __init__(self, x, y, angle=0):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -BULLET_SPEED * math.cos(math.radians(angle))
        self.speed_x = BULLET_SPEED * math.sin(math.radians(angle))
        if angle != 0:
            self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        """Update bullet position and remove if off screen"""
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if (self.rect.bottom < 0 or
                self.rect.left < 0 or
                self.rect.right > WINDOW_WIDTH):
            self.kill()


class Crystal(pygame.sprite.Sprite):
    """Represents a collectable crystal power-up"""

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(crystal_img, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = CRYSTAL_SPEED

    def update(self):
        """Update crystal position and remove if off screen"""
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    """Represents an asteroid obstacle that scales with game time"""

    def __init__(self, game_time):
        super().__init__()

        # Calculate size scaling factor based on game time (minutes)
        # Size increases by 10% every minute, up to double the original size
        size_scale = min(1 + (game_time / 60) * 0.1, 2.0)

        # Base size is scaled by the time factor
        base_size = random.randint(30, 80)
        scaled_size = int(base_size * size_scale)

        # Create the scaled asteroid image
        self.image = pygame.transform.scale(asteroid_img1, (scaled_size, scaled_size))
        self.rect = self.image.get_rect()

        # Position the asteroid
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

        # Speed is inversely proportional to size but increases slightly with time
        # This prevents larger asteroids from being too slow
        speed_scale = min(1 + (game_time / 60) * 0.05, 1.5)  # 5% faster per minute
        self.speed = ASTEROID_SPEED * (50 / scaled_size) * speed_scale

    def update(self):
        """Update asteroid position and remove if off screen"""
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class Player(pygame.sprite.Sprite):
    """Represents the player's spaceship"""

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10
        self.speed = PLAYER_SPEED
        self.speed_y = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.has_vertical_movement = False
        self.power_up_active = False
        self.power_up_timer = 0
        self.power_up_duration = 5

    def update(self):
        """Update player position and handle shooting"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
        if self.has_vertical_movement:
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed_y
            if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
                self.rect.y += self.speed_y

        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now

        if self.power_up_active:
            self.power_up_timer -= 1 / FPS
            if self.power_up_timer <= 0:
                self.power_up_active = False

    def shoot(self):
        """Handle shooting logic"""
        if self.power_up_active:
            self._shoot_shower()
        else:
            self._shoot_normal()

    def _shoot_normal(self):
        """Fire a single bullet"""
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()

    def _shoot_shower(self):
        """Fire multiple bullets in a spread pattern"""
        angles = [-45, -30, -15, 0, 15, 30, 45]
        for angle in angles:
            bullet = Bullet(self.rect.centerx, self.rect.top, angle)
            all_sprites.add(bullet)
            bullets.add(bullet)
        laser_sound.play()

    def activate_power_up(self):
        """Activate the power-up mode"""
        self.power_up_active = True
        self.power_up_timer = self.power_up_duration

    def reset_position(self):
        """Reset player to starting position"""
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10


def show_message(screen, text, duration=2):
    """Display a centered message on screen"""
    font = pygame.font.Font(None, 36)
    message = font.render(text, True, WHITE)
    text_rect = message.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    return {"text": message, "rect": text_rect, "duration": duration}


def main():
    """Main game loop"""
    global all_sprites, asteroids, crystals, bullets, player

    # Initialize sprite groups
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    crystals = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Create player and background
    player = Player()
    all_sprites.add(player)
    background = Background()

    # Game state variables
    score = 0
    high_score = 0
    crystal_count = 0
    lives = 1
    game_over = False
    active_messages = []
    game_time = 0  # Track game time in seconds
    spawn_timer = 0  # Timer for controlling spawn rates

    # Start background music
    background_music.play(-1)

    # Main game loop
    running = True
    while running:
        # Control game speed
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Reset game state while preserving high score
                    game_over = False
                    score = 0
                    crystal_count = 0
                    lives = 1
                    player.reset_position()
                    player.has_vertical_movement = False
                    player.power_up_active = False
                    # Clear all sprites except player
                    for sprite in all_sprites:
                        if sprite != player:
                            sprite.kill()
                    background_music.play(-1)

        if not game_over:
            # Update game time (in seconds)
            game_time += 1 / FPS

            # Calculate spawn interval based on game time
            # Start with a much shorter base interval of 0.4 seconds
            # Decrease quickly to create intense action
            base_spawn_interval = 0.4  # Starting spawn interval in seconds
            min_spawn_interval = 0.15  # Very short minimum interval for intense action

            # Decrease spawn interval more aggressively
            current_interval = max(
                base_spawn_interval - (game_time / 30) * 0.1,  # Decrease by 0.1s every 30 seconds
                min_spawn_interval
            )

            # Update spawn timer
            spawn_timer += 1 / FPS
            if spawn_timer >= current_interval:
                spawn_timer = 0  # Reset timer

                # Much higher asteroid probability
                asteroid_chance = min(0.9 + (game_time / 30) * 0.02, 0.98)  # Max 98% chance

                # Multiple spawns per interval for increased density
                spawn_count = min(1 + int(game_time / 60), 3)  # Up to 3 spawns at once

                for _ in range(spawn_count):
                    if random.random() < asteroid_chance:
                        # Vary the spawn positions for multiple asteroids
                        asteroid = Asteroid(game_time)
                        asteroids.add(asteroid)
                        all_sprites.add(asteroid)
                    else:
                        crystal = Crystal()
                        crystals.add(crystal)
                        all_sprites.add(crystal)

            # Update game objects
            all_sprites.update()
            background.update()

            # Handle collisions
            # Crystal collection
            crystal_hits = pygame.sprite.spritecollide(player, crystals, True)
            for crystal in crystal_hits:
                crystal_sound.play()
                score += 10
                crystal_count += 1

                # Update high score if current score is higher
                high_score = max(high_score, score)

                # Check for vertical movement unlock
                if crystal_count >= VERTICAL_MOVEMENT_THRESHOLD and not player.has_vertical_movement:
                    player.has_vertical_movement = True
                    player.speed_y = 5
                    active_messages.append(show_message(screen, "Vertical movement unlocked!"))

                # Check for power-up activation
                if crystal_count >= POWER_UP_THRESHOLD and not player.power_up_active:
                    player.activate_power_up()
                    active_messages.append(show_message(screen, "Power-up activated!"))

            # Bullet hits on asteroids
            hits = pygame.sprite.groupcollide(bullets, asteroids, True, True)
            for hit in hits:
                score += 10
                clash_sound.play()

                # Update high score if current score is higher
                high_score = max(high_score, score)

            # Player collision with asteroids
            if pygame.sprite.spritecollide(player, asteroids, True):
                lives -= 1
                if lives <= 0:
                    game_over = True
                    game_over_sound.play()
                    background_music.stop()
                else:
                    player.reset_position()

            # Update message timers
            active_messages = [msg for msg in active_messages
                               if msg["duration"] > 0]
            for msg in active_messages:
                msg["duration"] -= 1 / FPS

        # Drawing
        # Draw background first
        background.draw(screen)

        # Draw all game sprites
        all_sprites.draw(screen)

        # Draw UI elements
        font = pygame.font.Font(None, 36)
        # Score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        # High Score
        high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
        screen.blit(high_score_text, (10, 40))
        # Crystal count
        crystal_text = font.render(f'Crystals: {crystal_count}', True, WHITE)
        screen.blit(crystal_text, (10, 70))
        # Lives
        lives_text = font.render(f'Lives: {lives}', True, WHITE)
        screen.blit(lives_text, (10, 100))

        # Draw active messages
        for msg in active_messages:
            screen.blit(msg["text"], msg["rect"])

        # Game over screen
        if game_over:
            game_over_text = font.render('GAME OVER! Press SPACE to restart',
                                         True, WHITE)
            text_rect = game_over_text.get_rect(
                center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            screen.blit(game_over_text, text_rect)

        # Update the display
        pygame.display.flip()

    # Clean up when the game exits
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()