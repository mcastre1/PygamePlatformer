import pygame
from tiles import Tile
from settings import *

class Level():
    def __init__(self, level_data, surface):
        # Screen from main file
        self.display_surface = surface

        # Sprite group to add to when iterating through level data
        self.tiles = pygame.sprite.Group()

        self.setup_level(level_data)
        
    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col == 'X':
                    self.tiles.add(Tile((col_index*tile_size, row_index*tile_size), tile_size))

    def run(self):
        self.tiles.draw(self.display_surface)