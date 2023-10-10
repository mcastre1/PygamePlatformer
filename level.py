import pygame
from tiles import Tile
from settings import *
from player import Player

class Level():
    def __init__(self, level_data, surface):
        # Screen from main file
        self.display_surface = surface

        # Sprite groups
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.setup_level(level_data)

        # Amount of pixels level is shifted on the x coordinate
        self.world_shift = 0
        
        self.current_x = 0

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if col == 'X':
                    self.tiles.add(Tile((x, y), tile_size))

                if col == 'P':
                    self.player.add(Player((x, y)))

    # This function helps scroll the whole level when player reaches a threshold
    # This simulates a 'camera'
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < (screen_width * .25) and direction_x == -1:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width * .75) and direction_x == 1:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    # Updates player horizontal movement
    # and checks for collisions on the x axis
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x == -1:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x == 1:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x) or player.direction.x >= 0:
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x) or player.direction.x <= 0:
            player.on_right = False


    # Updates player vertical movement
    # and checks for collisions on the y axis
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.on_ceiling = True
                
                player.direction.y = 0
                
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):
        # Level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # player
        self.player.update()
        self.horizontal_movement_collision() # For player
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        