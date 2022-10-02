import pygame
from settings import *
from support import *


class Player(pygame.sprite.Sprite):  # because it's a sprite
    def __init__(self, pos, group):
        super().__init__(group)  # instance of this class it'll be initialized within the group

        self.import_assets()  # from support.py
        self.status = 'down_idle'  # which animation
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]  # what sprite looks like
        self.rect = self.image.get_rect(center=pos)  # position based on the parameter position

        # movement attributes
        self.direction = pygame.math.Vector2()

        # stored in a vector because delta time using floating points, keeps it smooth
        self.pos = pygame.math.Vector2(self.rect.center)

        self.speed = 200

    # importing the pixel art for the different animations
    # dictionary of the keys plus their values
    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}

        # select the right folder in relation to the key
        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)
        # print(self.animations)

    def animate(self, dt):
        self.frame_index += 4 * dt  # returns a floating point number so need to convert to int later

        # need to make sure self.frame_index is never above 4 (due to animation sprites)
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    # user input stuff
    def input(self):
        keys = pygame.key.get_pressed()  # get the key press

        # cardinal directions, left right up down
        # if you're not pressing a key else make it 0, i.e. stop the movement
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

    def get_status(self):
        if self.direction.magnitude() == 0:  # if the player stops moving then add _idle

            self.status += self.status.split('_')[0] + '_idle'  # splits the code at _ so we dont just add lots of _idle

    def move(self, dt):

        # normalizing the vector (stop player going fast when going diagonally for example)
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt  # add the two values and make it the new position
        self.rect.centerx = self.pos.x  # update the above to the new center of the rect

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt  # add the two values and make it the new position
        self.rect.centery = self.pos.y  # update the above to the new center of the rect

    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
