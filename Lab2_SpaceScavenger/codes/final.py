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
SCROLL_SPEED = 2
NUM_STARS = 100

# Game Thresholds
MAX_LIVES = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_BLUE = (100, 100, 255)


def show_start_menu(screen):
    font = pygame.font.Font(None, 74)
    title_text = font.render("Space Scavenger", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))

    start_button = pygame.Rect(150, 250, 500, 100)  # Button dimensions
    rules_button = pygame.Rect(150, 400, 500, 100)

    start_text = font.render("Start Game", True, (255, 255, 255))  # White text for start button
    rules_text = font.render("Game Rules", True, (255, 255, 255))  # White text for rules button

    while True:
        screen.fill((0, 0, 0))  # Clear screen with black
        screen.blit(title_text, title_rect)  # Draw title

        # Draw buttons
        pygame.draw.rect(screen, (0, 255, 0), start_button)  # Green start button
        pygame.draw.rect(screen, (0, 0, 255), rules_button)  # Blue rules button

        # Draw button text
        screen.blit(start_text, (start_button.x + 150, start_button.y + 25))  # Center text on button
        screen.blit(rules_text, (rules_button.x + 150, rules_button.y + 25))  # Center text on button

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return "start"  # Start the game
                if rules_button.collidepoint(event.pos):
                    return "rules"  # Show game rules

        # Update display
        pygame.display.flip()


def show_game_rules(screen):
    font = pygame.font.Font(None, 36)
    rules = [
        "Game Rules:",
        "- Use arrow keys to move the spaceship",
        "- Press SPACE to shoot",
        "- Collect crystals for power-ups",
        "- Avoid colliding with asteroids",
        "- Score points by destroying asteroids",
        "- Get extra life at 500 points",
        "- Game gets harder as you progress"
    ]

    while True:
        screen.fill((0, 0, 0))  # Clear screen with black
        for i, line in enumerate(rules):
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (50, 100 + i * 30))  # Adjust position

        # Draw back button
        back_button = pygame.Rect(150, 500, 500, 100)
        pygame.draw.rect(screen, (255, 0, 0), back_button)  # Red back button
        back_text = font.render("Play Game", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return  # Return to the start menu

        pygame.display.flip()


# Example usage
if __name__ == "__main__":
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Set up the display
    result = show_start_menu(screen)  # Show the start menu
    if result == "start":
        # Start the game logic here
        pass
    elif result == "rules":
        show_game_rules(screen)  # Call function to display game rules handle starting the game or showing rules
clock = pygame.time.Clock()


# Asset Loading Functions
def load_image(name):
    """Load and return an image asset"""
    return pygame.image.load(os.path.join('assets', 'images', name)).convert_alpha()


def load_sound(name):
    """Load and return a sound asset"""
    return pygame.mixer.Sound(os.path.join('assets', 'sounds', name))


# Load game assets
player_img = load_image('ship.png')
asteroid_img1 = load_image('asteroid.png')
asteroid_img2 = load_image('asteroid.png')
crystal_img = load_image('crystal.png')
# crystal_img = load_image('powerup.png')

# Load and configure sounds
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


class Star:
    """Creates individual stars for the background"""

    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)
        self.speed = random.randint(2, 5)
        self.size = random.randint(1, 3)
        self.brightness = random.choice([WHITE, GRAY, LIGHT_BLUE])

    def move(self):
        """Updates star position with wrapping"""
        self.y += self.speed
        if self.y > WINDOW_HEIGHT:
            self.y = 0
            self.x = random.randint(0, WINDOW_WIDTH)
            self.speed = random.randint(2, 5)


class Background:
    """Manages the scrolling starfield effect"""

    def __init__(self):
        self.stars = [Star() for _ in range(NUM_STARS)]

    def update(self):
        """Updates all stars"""
        for star in self.stars:
            star.move()

    def draw(self, surface):
        """Draws the starfield"""
        surface.fill(BLACK)
        for star in self.stars:
            pygame.draw.circle(surface, star.brightness,
                               (star.x, star.y), star.size)


class Bullet(pygame.sprite.Sprite):
    """Player's projectile"""

    def __init__(self, x, y, angle=0):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        # Calculate velocity based on angle for spread shot
        self.speed_y = -BULLET_SPEED * math.cos(math.radians(angle))
        self.speed_x = BULLET_SPEED * math.sin(math.radians(angle))
        if angle != 0:
            self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        """Move bullet and handle off-screen removal"""
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if (self.rect.bottom < 0 or
                self.rect.left < 0 or
                self.rect.right > WINDOW_WIDTH):
            self.kill()


class Crystal(pygame.sprite.Sprite):
    """Collectable power-up item"""

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(crystal_img, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = CRYSTAL_SPEED

    def update(self):
        """Move crystal down and handle off-screen removal"""
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    """Obstacle that scales with game time"""

    def __init__(self, game_time):
        super().__init__()
        # Size increases over time up to 2x
        size_scale = min(1 + (game_time / 60) * 0.1, 2.0)
        base_size = random.randint(30, 60)
        scaled_size = int(base_size * size_scale)

        self.image = pygame.transform.scale(asteroid_img1, (scaled_size, scaled_size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

        # Speed is inverse to size but increases with time
        speed_scale = min(1 + (game_time / 60) * 0.05, 1.5)
        self.speed = ASTEROID_SPEED * (50 / scaled_size) * speed_scale

    def update(self):
        """Move asteroid down and handle off-screen removal"""
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class Player(pygame.sprite.Sprite):
    """Player character with respawn protection"""

    def __init__(self):
        super().__init__()
        # Store both original and current image for fade effects
        self.original_image = pygame.transform.scale(player_img, (50, 50))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10

        # Movement settings
        self.speed = PLAYER_SPEED
        self.speed_y = 0
        self.has_vertical_movement = False

        # Shooting settings
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250

        # Power-up settings
        self.power_up_active = False
        self.power_up_timer = 0
        self.power_up_duration = 5

        # Respawn protection settings
        self.is_respawning = False
        self.respawn_timer = 0
        self.respawn_duration = 3
        self.fade_min = 50
        self.fade_max = 255
        self.fade_speed = 8

    def update(self):
        """Handle movement, shooting, and visual effects"""
        # Movement
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

        # Shooting
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now

        # Power-up timer
        if self.power_up_active:
            self.power_up_timer -= 1 / FPS
            if self.power_up_timer <= 0:
                self.power_up_active = False

        # Respawn effect
        if self.is_respawning:
            self.respawn_timer -= 1 / FPS
            if self.respawn_timer <= 0:
                self.is_respawning = False
                self.image = self.original_image.copy()
            else:
                # Create pulsing fade effect
                progress = self.respawn_timer / self.respawn_duration
                fade_value = self.fade_min + abs(math.sin(progress * math.pi * self.fade_speed)) * (
                            self.fade_max - self.fade_min)
                self.apply_fade(int(fade_value))

    def apply_fade(self, alpha):
        """Apply transparency effect during respawn"""
        self.image = self.original_image.copy()
        alpha_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        alpha_surface.fill((255, 255, 255, alpha))
        self.image.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def start_respawn_effect(self):
        """Initialize respawn protection and fade effect"""
        self.is_respawning = True
        self.respawn_timer = self.respawn_duration
        self.reset_position()

    def shoot(self):
        """Handle shooting based on power-up status"""
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
        """Fire spread pattern when powered up"""
        angles = [-45, -30, -15, 0, 15, 30, 45]
        for angle in angles:
            bullet = Bullet(self.rect.centerx, self.rect.top, angle)
            all_sprites.add(bullet)
            bullets.add(bullet)
        laser_sound.play()

    def activate_power_up(self):
        """Start or refresh power-up mode"""
        self.power_up_active = True
        self.power_up_timer = self.power_up_duration

    def reset_position(self):
        """Reset to starting position"""
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10


def show_message(screen, text, duration=2):
    """Create a centered screen message"""
    font = pygame.font.Font(None, 36)
    message = font.render(text, True, WHITE)
    text_rect = message.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    return {"text": message, "rect": text_rect, "duration": duration}


def main():
    """Main game loop and initialization"""
    global all_sprites, asteroids, crystals, bullets, player

    # Initialize all sprite groups for game objects
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    crystals = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Create and set up the player and background
    player = Player()
    all_sprites.add(player)
    background = Background()

    # Initialize game state variables
    score = 0
    high_score = 0
    crystal_count = 0
    lives = 1
    game_over = False
    active_messages = []
    game_time = 0
    spawn_timer = 0

    # Start the background music in infinite loop
    background_music.play(-1)

    # Main game loop
    running = True
    while running:
        # Control game speed using FPS
        clock.tick(FPS)

        # Event handling (quit and restart)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Reset game state while keeping high score
                    game_over = False
                    score = 0
                    crystal_count = 0
                    lives = 1
                    game_time = 0
                    player.reset_position()
                    player.has_vertical_movement = False
                    player.power_up_active = False
                    player.is_respawning = False
                    # Clear all sprites except player
                    for sprite in all_sprites:
                        if sprite != player:
                            sprite.kill()
                    background_music.play(-1)

        if not game_over:
            # Update game time and spawn timer
            game_time += 1 / FPS
            spawn_timer += 1 / FPS

            # Calculate spawn timing that gets faster over time
            base_spawn_interval = 0.4
            min_spawn_interval = 0.15
            current_interval = max(
                base_spawn_interval - (game_time / 30) * 0.1,
                min_spawn_interval
            )

            # Handle enemy and crystal spawning
            if spawn_timer >= current_interval:
                spawn_timer = 0
                asteroid_chance = min(0.9 + (game_time / 30) * 0.02, 0.98)
                spawn_count = min(1 + int(game_time / 60), 3)

                for _ in range(spawn_count):
                    if random.random() < asteroid_chance:
                        asteroid = Asteroid(game_time)
                        asteroids.add(asteroid)
                        all_sprites.add(asteroid)
                    else:
                        crystal = Crystal()
                        crystals.add(crystal)
                        all_sprites.add(crystal)

            # Update all game objects and background
            all_sprites.update()
            background.update()

            # Handle collisions
            # Crystal collection
            crystal_hits = pygame.sprite.spritecollide(player, crystals, True)
            for crystal in crystal_hits:
                crystal_sound.play()
                score += 10
                crystal_count += 1
                high_score = max(high_score, score)

                # Power-up activation every 5 crystals collected
                if crystal_count % 5 == 0:
                    player.activate_power_up()
                    active_messages.append(show_message(screen, "Power-up activated!"))

                # Unlock vertical movement at score 300
                if score >= 300 and not player.has_vertical_movement:
                    player.has_vertical_movement = True
                    player.speed_y = 5
                    active_messages.append(show_message(screen, "Vertical movement unlocked!"))

            # Bullet hits on asteroids
            hits = pygame.sprite.groupcollide(bullets, asteroids, True, True)
            for hit in hits:
                score += 10
                clash_sound.play()
                high_score = max(high_score, score)

                # Grant extra life every 500 points
                if score % 500 == 0 and lives < MAX_LIVES:
                    lives += 1
                    active_messages.append(show_message(screen, "Extra life earned!"))

            # Player collision with asteroids
            if not player.is_respawning:  # Only check collisions if not in respawn protection
                if pygame.sprite.spritecollide(player, asteroids, True):
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                        game_over_sound.play()
                        background_music.stop()
                    else:
                        player.start_respawn_effect()  # Start respawn protection and fade effect

            # Update message timers
            active_messages = [msg for msg in active_messages if msg["duration"] > 0]
            for msg in active_messages:
                msg["duration"] -= 1 / FPS

        # Drawing section
        background.draw(screen)
        all_sprites.draw(screen)

        # Draw UI elements
        font = pygame.font.Font(None, 36)
        # Game stats display
        texts = [
            (f'Score: {score}', (10, 10)),
            (f'High Score: {high_score}', (10, 40)),
            (f'Crystals: {crystal_count}', (10, 70)),
            (f'Lives: {lives}', (10, 100))
        ]

        for text, pos in texts:
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, pos)

        # Draw active messages (power-ups, achievements, etc.)
        for msg in active_messages:
            screen.blit(msg["text"], msg["rect"])

        # Game over screen
        if game_over:
            game_over_text = font.render('GAME OVER! Press SPACE to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            screen.blit(game_over_text, text_rect)

        # Update the display
        pygame.display.flip()

    # Clean up the game
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()