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
SPEED_INCREASE = 0.2
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
    return pygame.image.load(os.path.join('assets', 'images', name)).convert_alpha()


def load_sound(name):
    return pygame.mixer.Sound(os.path.join('assets', 'sounds', name))


# Load game assets
player_img = load_image('ship.png')
asteroid_img1 = load_image('asteroid.png')
asteroid_img2 = load_image('asteroid.png')
crystal_img = load_image('crystal.png')

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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10
        self.speed = PLAYER_SPEED
        self.speed_y = 0  # Vertical movement (unlocked later)
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.has_vertical_movement = False
        self.power_up_active = False
        self.power_up_timer = 0
        self.power_up_duration = 5  # seconds

    def update(self):
        # Handle movement
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

        # Handle shooting
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now

        # Update power-up timer
        if self.power_up_active:
            self.power_up_timer -= 1 / FPS
            if self.power_up_timer <= 0:
                self.power_up_active = False

    def shoot(self):
        if self.power_up_active:
            self._shoot_shower()
        else:
            self._shoot_normal()

    def _shoot_normal(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()

    def _shoot_shower(self):
        # Create spread pattern of bullets
        angles = [-45, -30, -15, 0, 15, 30, 45]
        for angle in angles:
            bullet = Bullet(self.rect.centerx, self.rect.top, angle)
            all_sprites.add(bullet)
            bullets.add(bullet)
        laser_sound.play()

    def activate_power_up(self):
        self.power_up_active = True
        self.power_up_timer = self.power_up_duration

    def reset_position(self):
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        # Calculate velocity components based on angle
        self.speed_y = -BULLET_SPEED * math.cos(math.radians(angle))
        self.speed_x = BULLET_SPEED * math.sin(math.radians(angle))
        if angle != 0:
            self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        # Remove if off screen
        if (self.rect.bottom < 0 or
                self.rect.left < 0 or
                self.rect.right > WINDOW_WIDTH):
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, level=1):
        super().__init__()
        # Size scales with level
        base_size = random.randint(30, 80)
        size = min(base_size + (level * 5), 120)  # Cap at 120 pixels
        self.image = pygame.transform.scale(asteroid_img1, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        # Speed inversely proportional to size
        self.speed = ASTEROID_SPEED * (1 + (level * 0.2)) * (50 / size)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class Crystal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(crystal_img, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = CRYSTAL_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class Star:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)
        self.speed = random.randint(2, 5)
        self.size = random.randint(1, 3)
        self.brightness = random.choice([WHITE, GRAY, LIGHT_BLUE])

    def move(self):
        self.y += self.speed
        if self.y > WINDOW_HEIGHT:
            self.y = 0
            self.x = random.randint(0, WINDOW_WIDTH)
            self.speed = random.randint(2, 5)


class Background:
    def __init__(self):
        self.stars = [Star() for _ in range(NUM_STARS)]

    def update(self):
        for star in self.stars:
            star.move()

    def draw(self, surface):
        surface.fill(BLACK)
        for star in self.stars:
            pygame.draw.circle(surface, star.brightness,
                               (star.x, star.y), star.size)


def show_message(screen, text, duration=2):
    """Display a centered message on screen"""
    font = pygame.font.Font(None, 36)
    message = font.render(text, True, WHITE)
    text_rect = message.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    return {"text": message, "rect": text_rect, "duration": duration}


def main():
    global all_sprites, asteroids, crystals, bullets, player, SPAWN_RATE

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
    crystal_count = 0
    lives = 1  # Start with 1 life
    level = 1
    elapsed_time = 0
    game_over = False
    active_messages = []

    # Start background music
    background_music.play(-1)

    # Game loop
    running = True
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Reset game state
                    game_over = False
                    score = 0
                    crystal_count = 0
                    lives = 1
                    level = 1
                    player.reset_position()
                    player.has_vertical_movement = False
                    player.power_up_active = False
                    # Clear all sprites except player
                    for sprite in all_sprites:
                        if sprite != player:
                            sprite.kill()
                    background_music.play(-1)

        if not game_over:
            # Update game time and difficulty
            elapsed_time += 1 / FPS
            if elapsed_time >= 10:
                level += 1
                elapsed_time = 0
                SPAWN_RATE = max(10, SPAWN_RATE - 5)

            # Spawn objects
            if random.randrange(SPAWN_RATE) == 0:
                if random.random() < 0.8:
                    asteroid = Asteroid(level)
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

                # Check for extra life
                if score >= EXTRA_LIFE_THRESHOLD and lives < MAX_LIVES:
                    lives += 1
                    active_messages.append(show_message(screen, "Extra life earned!"))

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
        background.draw(screen)
        all_sprites.draw(screen)

        # Draw UI elements
        font = pygame.font.Font(None, 36)
        # Score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        # Crystal count
        crystal_text = font.render(f'Crystals: {crystal_count}', True, WHITE)
        screen.blit(crystal_text, (10, 40))
        # Lives
        lives_text = font.render(f'Lives: {lives}', True, WHITE)
        screen.blit(lives_text, (10, 70))
        # Level
        level_text = font.render(f'Level: {level}', True, WHITE)
        screen.blit(level_text, (10, 100))

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

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()