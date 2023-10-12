import pygame
from support import import_csv_layout, import_cut_graphic
from settings import tile_size
from tiles import Tile, StaticTile

class Level:
    def __init__(self, level_data, display_surface):
        # general setup
        self.display_surface = display_surface
        self.level_data = level_data
        self.world_shift = 0

        # Read csv created by tiled software
        # Terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

    # creates and returns a group depending on type
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, id in enumerate(row):
                if id != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('../graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(id)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)


        return sprite_group

    def run(self):
        # run the entire game/level
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

