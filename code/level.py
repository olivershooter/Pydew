import pygame
from settings import *
from player import Player


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()  # lets the level draw on the same display from main

        # sprite groups
        self.all_sprites = pygame.sprite.Group()  # draw and update things in the game

        self.setup()

    def setup(self):
        self.player = Player((640, 360), self.all_sprites)

    def run(self, dt):
        self.display_surface.fill('black')  # drawing a black colour, so we don't see the previous frame when running
        self.all_sprites.draw(self.display_surface)  # drawing on the display surface
        self.all_sprites.update(dt)  # updates all the sprites // also runs the player update method
