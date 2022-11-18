import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, Wildflower, Tree
from pytmx.util_pygame import load_pygame
from support import *


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()  # lets the level draw on the same display from main

        # sprite groups
        self.all_sprites = CameraGroup()  # draw and update things in the game

        self.setup()
        self.overlay = Overlay(self.player)  # happens after setup because in setup you create te player

    def setup(self):
        tmx_data = load_pygame('../data/map.tmx')  # load the map data

        # importing the house from tiled map data
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:  # in the tiled class
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():  # for the x, y and surface in the data
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # importing the fence from tiled
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        # importing the water
        water_frames = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # importing the trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, self.all_sprites, obj.name)

        # importing the wildflowers
        for obj in tmx_data.get_layer_by_name(
                'Decoration'):  # obj is the object in the class Decoration and you can use that
            Wildflower((obj.x, obj.y), obj.image, self.all_sprites)

        self.player = Player((640, 360), self.all_sprites)  # setting up the player
        Generic(pos=(0, 0),
                surf=pygame.image.load('../graphics/world/ground.png').convert_alpha(),
                groups=self.all_sprites,
                z=LAYERS['ground'])  # setting up the level ground image

    def run(self, dt):
        self.display_surface.fill('black')  # drawing a black colour, so we don't see the previous frame when running
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)  # updates all the sprites // also runs the player update method
        self.overlay.display()


# Camera logic
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()  # logic for following the player

    def custom_draw(self, player):
        # this works out how much to offset the player by and keep them in the centre
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
