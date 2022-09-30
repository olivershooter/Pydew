import pygame
from settings import *


class Player(pygame.sprite.Sprite):  # because it's a sprite
    def __init__(self, pos, group):
        super().__init__(group)  # instance of this class it'll be initialized within the group

        # general setup
        self.image = pygame.Surface((32, 64))  # what sprite looks like
        self.image.fill('green')  # fill it green
        self.rect = self.image.get_rect(center=pos)  # position based on the parameter position

        # movement attributes
        self.direction = pygame.math.Vector2()

        # stored in a vector because delta time using floating points, keeps it smooth
        self.pos = pygame.math.Vector2(self.rect.center)

        self.speed = 200

    # user input stuff
    def input(self):
        keys = pygame.key.get_pressed()  # get the key press

        # cardinal directions, left right up down
        # if you're not pressing a key else make it 0, i.e. stop the movement
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

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
        self.move(dt)
