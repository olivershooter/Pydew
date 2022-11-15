import pygame
from settings import *


class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports - new surface tools not the players tools
        overlay_path = '../graphics/overlay/'
        self.tools_surface = {tool: pygame.image.load(f"{overlay_path}{tool}.png").convert_alpha() for tool in
                              player.tools}
        self.seeds_surface = {seeds: pygame.image.load(f"{overlay_path}{seeds}.png").convert_alpha() for seeds in
                              player.seeds}

    def display(self):
        # show the tools
        tool_surface = self.tools_surface[self.player.selected_tool]
        tool_rectangle = tool_surface.get_rect(midbottom=OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surface, tool_rectangle)

        # show the seeds
        seeds_surface = self.seeds_surface[self.player.selected_seed]
        seeds_rectangle = seeds_surface.get_rect(midbottom=OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seeds_surface, seeds_rectangle)
