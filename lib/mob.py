import pygame, random
import block, imageloading

class Character:
    # holds character data
    def __init__(self, room, theme, action):
        # pick random spot in room 1 for character to start 
        no_walls = [x for x in room.blocks if x.block_type == 'floor']
        start_location = random.choice(no_walls).pos

        # create block for character
        self.block =  block.Block(start_location)
        self.block.active = True
        image, images = imageloading.getActionImages('mob',theme,action)
        self.block.loadImages(images)

