import pygame
from support import import_csv_layout, import_cut_graphic
from settings import tile_size, screen_height, screen_width
from tiles import StaticTile, Crate, Coin, Palm, Tile
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect


class Level:
    def __init__(self, level_data, display_surface):
        # general setup
        self.display_surface = display_surface
        self.level_data = level_data
        self.world_shift = 0
        self.current_x = None

        # Player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        
        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

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
        self.clouds = Clouds(400, level_width, 30)


    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, id in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size  
                if id == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)

                if id == '1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    # create jump particle animations when jumping
    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10, -5)

        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

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

        # Updates player horizontal movement
    # and checks for collisions on the x axis
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidable_sprites:
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

    # Check whether player is on ground
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    # create a landing dust particle when player lands on our 
    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)
        
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

    # Updates player vertical movement
    # and checks for collisions on the y axis
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidable_sprites:
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

         # player
        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()

        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        self.scroll_x()
        self.player.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)        



        

        

