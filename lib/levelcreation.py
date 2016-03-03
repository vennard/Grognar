# Contains methods and resources for level generation

import pygame
import random

WHITE = (255,255,255)
LEVEL_SIZE = 1000
ROOM_SIZE = 10

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
        # create randomized room
        rndx = random.randint(2,ROOM_SIZE)
        rndy = random.randint(2,ROOM_SIZE)
        self.size = [rndx,rndy]
        for x in range(0,rndx):
            for y in range(0,rndy):
                # get random image to create new block and add to blocks
                rnd_image = random.randint(0,len(floor_images)-1)
                newx = topleft[0] + 10*x 
                newy = topleft[1] + 10*y 
                self.blocks.append(Block(floor_images[rnd_image],[newx,newy]))




    def addBlock(self, block):
        self.blocks.append(block)
