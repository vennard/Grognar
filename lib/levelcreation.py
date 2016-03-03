# Contains methods and resources for level generation

import pygame
import random

WHITE = (255,255,255)

def testcall():
    print("successfully called testcall in lib/levelcreation.py")

class Block(pygame.sprite.Sprite):
    blockType = None
    image = None


    '''This class represents the basic building blocks of the game level'''
    def __init__(self, image, pos):
        # call parent constructor
        super(Block, self).__init__()

        # initialize image and position
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Room:
    size = [0,0]    # contains x and y size of room
    topleft = [0,0]     #contains top left coords of room
    floor_images = []
    blocks = []     # initialized empty list for blocks

    def __init__(self, size, topleft, floor_images):
        self.size = size
        self.topleft = topleft
        self.floor_images = floor_images 
        test = Block('images/tile0.png', pos)
        self.blocks.append(test)
