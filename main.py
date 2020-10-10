import math
import random
import pygame
from pygame import mixer

pygame.init()

# WINDOW
WIDTH = 800
HEIGHT = 600
GAME_SPEED = .4
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)
backGround = pygame.image.load('img/bg.jpg')
backGround = pygame.transform.scale(backGround, (WIDTH, HEIGHT))
mixer.music.load('sound/background.wav')
mixer.music.play(-1)

# PLAYER
playerImg = pygame.image.load('img/player1.png')
playerImg = pygame.transform.scale(playerImg, (60, 60))
playerX = WIDTH / 2 - 30
playerY = HEIGHT - 80
playerX_change_left = 0
playerX_change_right = 0
score = 0
font = pygame.font.Font('freesansbold.ttf', 25)
laser_fx = mixer.Sound('sound/laser.wav')
explosion_fx = mixer.Sound('sound/explosion.wav')


def player(x):
    screen.blit(playerImg, (x, playerY))


def show_score():
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


def game_over():
    end_font = pygame.font.Font('freesansbold.ttf', 50)
    game_over_text = end_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (WIDTH/2 - 150, HEIGHT/2 - 30))


# ENEMIES
enemyX = []
enemyY = []
enemy_amount = 6
enemyX_change = 2 * GAME_SPEED
enemyY_change = 30
enemyImg = pygame.image.load('img/icon.png')
enemyImg = pygame.transform.scale(enemyImg, (60, 60))

for i in range(enemy_amount):
    enemyX.append(random.randint(80, WIDTH - 140))
    enemyY.append(20)


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


# PROJECTILE
projectileImg = pygame.image.load('img/blue_laser.png')
projectileImg = pygame.transform.scale(projectileImg, (20, 50))
projectileX = 0
projectileY = HEIGHT - 80
projectileY_change = 10 * GAME_SPEED
projectile_state = "ready"


def fire_projectile(x, y):
    global projectile_state
    projectile_state = "fire"
    screen.blit(projectileImg, (x + 20, y + 20))


def collision(enemy_x, enemy_y, projectile_x, projectile_y):
    distance = math.sqrt(math.pow(enemy_x - projectile_x, 2) + math.pow(enemy_y - projectile_y, 2))
    if distance < 25:
        return True
    else:
        return False


# GAME
running = True
while running:
    screen.fill((0, 0, 80))
    screen.blit(backGround, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change_left = -4 * GAME_SPEED
            if event.key == pygame.K_RIGHT:
                playerX_change_right = 4 * GAME_SPEED
            if event.key == pygame.K_SPACE:
                if projectile_state is "ready":
                    projectileX = playerX
                    fire_projectile(projectileX, projectileY)
                    laser_fx.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change_left = 0
            if event.key == pygame.K_RIGHT:
                playerX_change_right = 0

    # PLAYER LOGIC
    playerX += (playerX_change_left + playerX_change_right)
    if playerX < 20:
        playerX = 20
    elif playerX > WIDTH - 80:
        playerX = WIDTH - 80

    # TODO : Create 'enemy outer bounds (at 80 and WIDTH - 140)' to make Y speed uniform
    # ENEMY LOGIC
    for i in range(enemy_amount):
        enemyX[i] += enemyX_change
        if enemyX[i] < 20:
            enemyX_change = 2 * GAME_SPEED
            for j in range(enemy_amount):
                enemyY[j] += enemyY_change
        elif enemyX[i] > WIDTH - 80:
            enemyX_change = -2 * GAME_SPEED
            for j in range(enemy_amount):
                enemyY[j] += enemyY_change
        hit = collision(enemyX[i], enemyY[i], projectileX, projectileY)
        if hit:
            projectileY = HEIGHT - 80
            projectile_state = "ready"
            score += 1
            explosion_fx.play()
            enemyX[i] = random.randint(80, WIDTH - 140)
            enemyY[i] = 20
        enemy(enemyX[i], enemyY[i])
        if enemyY[i] > HEIGHT - 80:
            for j in range(enemy_amount):
                enemyY[j] = HEIGHT*2
            game_over()
            break

    # PROJECTILE LOGIC
    if projectile_state == "fire":
        fire_projectile(projectileX, projectileY)
        projectileY -= projectileY_change
    if projectileY < 0:
        projectileY = HEIGHT - 80
        projectile_state = "ready"

    player(playerX)
    show_score()
    pygame.display.update()
