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
        
    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if col == 'X':
                    self.tiles.add(Tile((x, y), tile_size))

                if col == 'P':
                    self.player.add(Player((x, y)))

    def run(self):
        # Level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        
        # player
        self.player.update()
        self.player.draw(self.display_surface)