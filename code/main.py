import pygame
import sys  # to help close the game properly
from level import Level
from settings import *


class Game:
    # Initialize the game with the settings, display from settings,
    # caption is game name, clock is clock, level comes from the level.py
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pydew Valley')
        self.clock = pygame.time.Clock()
        self.level = Level()

    # the function where everything runs
    def run(self):
        # little method to close the game properly
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # dt = delta time(https: // www.youtube.com / watch?v = XuyrHE6GIsc) good video
            # basically framerate independence so if the games running at 30fps its not physically slower than at 60
            dt = self.clock.tick() / 1000
            self.level.run(dt)  # need the argument for the level to run with delta time
            pygame.display.update()


# make sure we're in the main file, create object from the class then run
if __name__ == '__main__':
    game = Game()
    game.run()
