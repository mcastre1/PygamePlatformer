import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32,64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        # Vector to keep track of player movement
        self.direction = pygame.math.Vector2(0, 0)

        self.speed = 8

    # Function checks for pygame event key pressed
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        # Check for key pressed event
        self.get_input()
        # Move player left or right
        self.rect.x += self.direction.x * self.speed