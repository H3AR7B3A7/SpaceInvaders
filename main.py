import pygame
import random

pygame.init()

# WINDOW
WIDTH = 800
HEIGHT = 600
GAME_SPEED = .5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
backGround = pygame.image.load('bg.jpg')
backGround = pygame.transform.scale(backGround, (WIDTH, HEIGHT))

# PLAYER
playerImg = pygame.image.load('player1.png')
playerImg = pygame.transform.scale(playerImg, (60, 60))
playerX = WIDTH / 2 - 30
playerY = HEIGHT - 80
playerX_change_left = 0
playerX_change_right = 0


def player(x):
    screen.blit(playerImg, (x, playerY))


# ENEMY
enemyImg = pygame.image.load('icon.png')
enemyImg = pygame.transform.scale(enemyImg, (60, 60))
enemyX = random.randint(20, WIDTH - 80)
enemyY = 20
enemyX_change = 2 * GAME_SPEED
enemyY_change = 30


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


# PROJECTILE
projectileImg = pygame.image.load('blue_laser.png')
projectileImg = pygame.transform.scale(projectileImg, (20, 50))
projectileX = 0
projectileY = HEIGHT - 80
projectileY_change = 5 * GAME_SPEED
projectile_state = "ready"


def fire_projectile(x, y):
    global projectile_state
    projectile_state = "fire"
    screen.blit(projectileImg, (x + 20, y + 20))


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

    # ENEMY LOGIC
    enemyX += enemyX_change
    if enemyX < 20:
        enemyX_change = 2 * GAME_SPEED
        enemyY += enemyY_change
    elif enemyX > WIDTH - 80:
        enemyX_change = -2 * GAME_SPEED
        enemyY += enemyY_change

    # PROJECTILE LOGIC
    if projectile_state == "fire":
        fire_projectile(projectileX, projectileY)
        projectileY -= projectileY_change
    if projectileY < 0:
        projectileY = HEIGHT - 80
        projectile_state = "ready"

    player(playerX)
    enemy(enemyX, enemyY)
    pygame.display.update()
