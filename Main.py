# Author: Clinton Chieng
# Collect'em!
# Date: 2024/06/02

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Collect'em!")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 7
        self.lives = 5
        self.invincible = False
        self.invincibility_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Boundary checks
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Manage invincibility frames
        if self.invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False

    def become_invincible(self, duration):
        self.invincible = True
        self.invincibility_timer = duration

# Enemy and Coin classes (same as before)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = 3

    def update(self):
        # Movement towards the player
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        if self.rect.y > player.rect.y:
            self.rect.y -= self.speed

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = random.randint(0, SCREEN_HEIGHT)

# Start Screen
def show_start_screen():
    screen.fill((0, 0, 0))
    title_text = font.render("Coin Collector Shooter", True, (255, 255, 255))
    instructions_text = font.render("Press any key to start", True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    wait_for_key()

# End Screen
def show_end_screen(score):
    screen.fill((0, 0, 0))
    end_text = font.render("Game Over", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    instructions_text = font.render("Press any key to restart", True, (255, 255, 255))
    screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

# Reset enemy positions
def reset_enemy_positions():
    for enemy in enemies:
        enemy.rect.x = random.randint(0, SCREEN_WIDTH)
        enemy.rect.y = random.randint(0, SCREEN_HEIGHT)

# Main game loop
player = Player()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

all_sprites.add(player)

font = pygame.font.Font(None, 36)

running = True
while running:
    show_start_screen()
    player.lives = 5
    score = 0

    # Reset enemy positions and coins
    enemies.empty()
    coins.empty()
    all_sprites.empty()

    all_sprites.add(player)

    for i in range(5):
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)

    for i in range(10):
        coin = Coin()
        coins.add(coin)
        all_sprites.add(coin)

    while player.lives > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                player.lives = 0

        all_sprites.update()

        # Check for collisions with enemies if not invincible
        if not player.invincible and pygame.sprite.spritecollideany(player, enemies):
            player.lives -= 1
            if player.lives > 0:
                player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                player.become_invincible(60)  # Invincibility for 1 second
                reset_enemy_positions()

        # Check for collisions with coins
        coins_collected = pygame.sprite.spritecollide(player, coins, True)
        score += len(coins_collected)

        # Respawn coins
        while len(coins) < 10:
            coin = Coin()
            coins.add(coin)
            all_sprites.add(coin)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw all sprites
        all_sprites.draw(screen)

        # Draw the score and lives
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 50))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    show_end_screen(score)
pygame.quit()
