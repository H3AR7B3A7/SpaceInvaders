import pygame

pygame.init()

# WINDOW
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# PLAYER
playerImg = pygame.image.load('player1.png')
playerImg = pygame.transform.scale(playerImg, (60, 60))
playerX = 370
playerY = 520


def player(x):
    screen.blit(playerImg, (x, playerY))


# ENEMY
enemyImg = pygame.image.load('icon.png')
enemyImg = pygame.transform.scale(enemyImg, (60, 60))
enemyX = 370
enemyY = 20


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


# GAME
running = True
while running:
    screen.fill((0, 0, 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX -= 0.2
        if event.key == pygame.K_RIGHT:
            playerX += 0.2

    if playerX <= 20:
        playerX = 20
    elif playerX >= 720:
        playerX = 720

    player(playerX)
    enemy(enemyX, enemyY)
    pygame.display.update()
