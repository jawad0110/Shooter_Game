import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shooter Game")

# Set up the clock
clock = pygame.time.Clock()

# Set up the player
player_width = 50
player_height = 50
player_x = screen_width / 2 - player_width / 2
player_y = screen_height - player_height - 10
player_speed = 5
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Set up the bullets
bullet_width = 10
bullet_height = 20
bullet_speed = 10
bullets = []

# Set up the enemies
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []

# Set up the score
score = 0
font = pygame.font.Font(None, 36)

# Set up the game over text
game_over_text = font.render("Game Over", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(screen_width / 5, screen_height / 5))

win_game_text = font.render("You win!!!", True, (0, 255, 0))
win_game_rect = win_game_text.get_rect(center=(screen_width / 5, screen_height / 5))

# Set up the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE :
                # Fire a bullet
                bullet_x = player.x + player.width / 2 - bullet_width / 2
                bullet_y = player.y - bullet_height
                bullet = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
                bullets.append(bullet)

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    elif keys[pygame.K_RIGHT] and player.x < screen_width - player_width:
        player.x += player_speed

    # Move the bullets
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Spawn enemies
    if len(enemies) < 10:
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = random.randint(-screen_height, -enemy_height)
        enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        enemies.append(enemy) 

    # Move the enemies
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > screen_height:
            enemies.remove(enemy)
            score -= 1

    # Check for collisions
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1

    for enemy in enemies:
        if enemy.colliderect(player):
            running = False

    # Draw the screen
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), player)
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), bullet)
    for enemy in enemies:
        pygame.draw.rect(screen, (0, 255, 0), enemy)
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    if not running:
        screen.blit(game_over_text, game_over_rect)

    if running:
        if score == 10:
            screen.blit(win_game_text, win_game_rect)
            pygame.quit() 
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()    