import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmo Dodge")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

player_size = 30
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 10
player_speed = 6
lives = 3
shield = 0
boost = False

enemy_size = 25
enemy_speed = 5
enemies = []

bonus_size = 20
bonus_speed = 4
bonuses = []

powerup_size = 25
powerup_speed = 3
powerups = []

score = 0
font = pygame.font.Font(None, 36)
difficulty = 1
high_score = 0

game_state = "menu"

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "menu" and event.key == pygame.K_SPACE:
                game_state = "playing"
                score = 0
                lives = 3
                enemies = []
                bonuses = []
                powerups = []
                difficulty = 1
                player_x = WIDTH // 2
            elif game_state == "game_over" and event.key == pygame.K_r:
                game_state = "playing"
                score = 0
                lives = 3
                enemies = []
                bonuses = []
                powerups = []
                difficulty = 1
                player_x = WIDTH // 2
        if event.type == pygame.USEREVENT + 1:
            boost = False

    if game_state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > player_size:
            player_x -= player_speed * (2 if boost else 1)
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed * (2 if boost else 1)
        if keys[pygame.K_SPACE] and not boost:
            boost = True
            pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

        if random.randint(1, 15 - difficulty) == 1:
            enemy_x = random.randint(enemy_size, WIDTH - enemy_size)
            enemies.append([enemy_x, -enemy_size, enemy_size])

        if random.randint(1, 50) == 1:
            bonus_x = random.randint(bonus_size, WIDTH - bonus_size)
            bonuses.append([bonus_x, -bonus_size])

        if random.randint(1, 80) == 1:
            powerup_x = random.randint(powerup_size, WIDTH - powerup_size)
            powerups.append([powerup_x, -powerup_size])

        for enemy in enemies[:]:
            enemy[1] += enemy_speed + difficulty * 0.5
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)
                score += 1

        for bonus in bonuses[:]:
            bonus[1] += bonus_speed
            if bonus[1] > HEIGHT:
                bonuses.remove(bonus)

        for powerup in powerups[:]:
            powerup[1] += powerup_speed
            if powerup[1] > HEIGHT:
                powerups.remove(powerup)

        player_rect = pygame.Rect(player_x - player_size // 2, player_y - player_size // 2, player_size, player_size)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy[0] - enemy[2] // 2, enemy[1] - enemy[2] // 2, enemy[2], enemy[2])
            if player_rect.colliderect(enemy_rect):
                if shield > 0:
                    enemies.remove(enemy)
                else:
                    enemies.remove(enemy)
                    lives -= 1
                    if lives <= 0:
                        high_score = max(high_score, score)
                        game_state = "game_over"

        for bonus in bonuses[:]:
            bonus_rect = pygame.Rect(bonus[0] - bonus_size // 2, bonus[1] - bonus_size // 2, bonus_size, bonus_size)
            if player_rect.colliderect(bonus_rect):
                bonuses.remove(bonus)
                score += 20

        for powerup in powerups[:]:
            powerup_rect = pygame.Rect(powerup[0] - powerup_size // 2, powerup[1] - powerup_size // 2, powerup_size,
                                       powerup_size)
            if player_rect.colliderect(powerup_rect):
                powerups.remove(powerup)
                if random.random() < 0.5:
                    shield = 180
                else:
                    lives = min(5, lives + 1)

        if score > 0 and score % 20 == 0:
            difficulty = min(5, difficulty + 1)

        if shield > 0:
            shield -= 1

    screen.fill(BLACK)

    if game_state == "menu":
        title = font.render("Cosmo Dodge - Press SPACE to Start", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 20))

    elif game_state == "playing":
        pygame.draw.polygon(screen, BLUE, [(player_x, player_y - player_size // 2),
                                           (player_x - player_size // 2, player_y + player_size // 2),
                                           (player_x + player_size // 2, player_y + player_size // 2)])
        if shield > 0:
            pygame.draw.circle(screen, YELLOW, (int(player_x), int(player_y)), player_size, 2)

        for enemy in enemies:
            pygame.draw.circle(screen, RED, (int(enemy[0]), int(enemy[1])), enemy[2] // 2)

        for bonus in bonuses:
            pygame.draw.rect(screen, GREEN,
                             (bonus[0] - bonus_size // 2, bonus[1] - bonus_size // 2, bonus_size, bonus_size))

        for powerup in powerups:
            points = [(powerup[0] + powerup_size * math.cos(math.radians(a)),
                       powerup[1] + powerup_size * math.sin(math.radians(a))) for a in range(0, 360, 72)]
            pygame.draw.polygon(screen, PURPLE, points)

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        diff_text = font.render(f"Difficulty: {difficulty}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(diff_text, (10, 70))

    elif game_state == "game_over":
        game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()