import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):  # because it's a sprite
    def __init__(self, pos, group):
        super().__init__(group)  # instance of this class it'll be initialized within the group

        self.import_assets()  # from support.py
        self.status = 'down_idle'  # which animation
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]  # what sprite looks like
        self.rect = self.image.get_rect(center=pos)  # position based on the parameter position
        self.z = LAYERS['main']

        # movement attributes
        self.direction = pygame.math.Vector2()

        # stored in a vector because delta time using floating points, keeps it smooth
        self.pos = pygame.math.Vector2(self.rect.center)

        # player speed
        self.speed = 200

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }
        # tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seeds for game
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

    def use_tool(self):
        pass
        # print(self.selected_tool)

    def use_seed(self):
        pass
        # print(self.selected_tool)

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

        # if a player is using the tool we dont want them to move
        if not self.timers['tool use'].active:
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

            # tool use
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                # stops the player from moving with the tool use is active
                self.direction = pygame.math.Vector2()
                # make the animation smoother
                self.frame_index = 0

            # changing the tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                # if the tool index is > length of tools available then set the tool index to 0
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]

            # seed use
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                # stops the player from moving with the tool use is active
                self.direction = pygame.math.Vector2()
                # make the animation smoother
                self.frame_index = 0
                print('use seed')

            # change seeds
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                # if the tool index is > length of tools available then set the tool index to 0
                self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
                self.selected_seed = self.seeds[self.seed_index]
                # print('changed selected seed')

    def get_status(self):

        # idle animation
        if self.direction.magnitude() == 0:  # if the player stops moving then add _idle
            self.status = self.status.split('_')[0] + '_idle'  # splits the code at _ so we dont just add lots of _idle

        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        # update all the timer values to use for the animations and tooling
        for timer in self.timers.values():
            timer.update()

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
        self.update_timers()
        self.move(dt)
        self.animate(dt)
