# Contains methods and resources for level generation

import pygame

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

class Room(Block):
    pos = [0,0]  # contains top left corner coords
    size = [0,0]    # contains x and y size of room
    blocks = []     # initialized empty list for blocks

    def __init__(self, pos):
        super(Room, self).__init__()

        #TODO start just initializing a single block to test
