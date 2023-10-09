import pygame, sys
from settings import *


# Pygame setup
pygame.init()
# Screen width and screen height from settings
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')

    pygame.display.update()
    clock.tick(60)
