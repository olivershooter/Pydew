from os import walk  # walk lets you step through different folders
import pygame


def import_folder(path):
    surface_list = []  # store all the surfaces

    # for loop grabs the folder list in path, ignoring the first two folders with underscores
    # we want the image files, for every image grab the full path of it and print it as such
    # the image surface is of course that full path to the image (0.png or 1.png) in whatever folder will be needed
    # finally store said list in the surface list
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list
