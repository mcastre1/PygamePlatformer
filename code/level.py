import pygame
from support import import_csv_layout, import_cut_graphic
from settings import tile_size, screen_height
from tiles import StaticTile, Crate, Coin, Palm, Tile
from enemy import Enemy
from decoration import Sky, Water, Clouds


class Level:
    def __init__(self, level_data, display_surface):
        # general setup
        self.display_surface = display_surface
        self.level_data = level_data
        self.world_shift = -6

        # Player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Read csv created by tiled software
        # Terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # Grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # Crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # Coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # FG palms
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

        # BG palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

        # enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraints
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

        # DECORATIONS
        # sky
        self.sky = Sky(8)

        # water
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height-25, level_width)

        # clouds
        self.clouds = Clouds(400, level_width, 20)


    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, id in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size  
                if id == '0':
                    print('player goes here')
                if id == '1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

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

                    if type == 'grass':
                        grass_tile_list = import_cut_graphic('../graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(id)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    
                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    if type == 'coins':
                        if id == '0':
                            sprite = Coin(tile_size, x, y, '../graphics/coins/gold')
                        elif id == '1':
                            sprite = Coin(tile_size, x, y, '../graphics/coins/silver')

                    if type == 'fg palms':
                        if id == '0':
                            sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_small', 38)
                        elif id == '1':
                            sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_large', 64)

                    if type == 'bg palms':
                        sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_bg', 64)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)
                    
                    sprite_group.add(sprite)


        return sprite_group
    
    # This method reverses enemy image when it collides with one of the constraints
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def run(self):
        # decoration
        # sky
        self.sky.draw(self.display_surface)

        # clouds
        self.clouds.draw(self.display_surface, self.world_shift)

        # bg palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # fg palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        # enemies
        self.enemy_sprites.update(self.world_shift)
        # These contraints are there to reverse the enemies.
        # We dont draw them, but they do exist in the level
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse() # Call reverse on enemy collisions

        self.enemy_sprites.draw(self.display_surface)
       

        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        #player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)        
        
        

        

