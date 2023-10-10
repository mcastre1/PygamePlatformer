import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15 # how fast animation updates

        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # player movement
        # Vector to keep track of player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8 # Like jump speed, this has to be positive because y coordinates are positive on the lower side of screen
        self.jump_speed = -16 # This is negative because y coordinates are positive on the lower side of screen

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    # Loads in all images in character graphics folder
    def import_character_assets(self):
        character_path = './graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [],  'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path) # Helping function to iterate and create image surfaces from images in folder

    # Animates character sprite
    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Keeping track of image selected
        image = animation[int(self.frame_index)]
        # Check if player is facing right or left
        if self.facing_right:
            self.image = image
        else: # flip the image on the x axis, horizontally, if player is facing left
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # Set the rect agains sprites
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
             self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)


    # Function checks for pygame event key pressed
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1: # this is one to keep animation of fall and idle to spas out during collisions
            self.status = 'fall'
        else:
            if self.direction.x > 0:
                self.status = 'run'
            elif self.direction.x < 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    # The more the player falls, the faster the character falls
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        # Check for key pressed event
        self.get_input()
        self.get_status()
        self.animate()
