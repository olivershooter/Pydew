import pygame


# Class for the timer of the tool usage and hits
class Timer:
    def __init__(self, duration, func=None):
        # duration for the tool use
        self.duration = duration

        self.func = func
        # start time for the duration, 0 by default
        self.start_time = 0
        # boolean to check if active
        self.active = False

    def activate(self):
        self.active = True
        # set the start time to the ingame tick count
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        # set the current time to the pygame time
        current_time = pygame.time.get_ticks()
        # if the current time minus the start time is greater than the duration then
        if current_time - self.start_time >= self.duration:
            self.deactivate()
            if self.func:
                self.func()
