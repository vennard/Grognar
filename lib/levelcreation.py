# Contains methods and resources for level generation

import pygame
import random

WHITE = (255,255,255)
LEVEL_SIZE = 1000
MAX_ROOM_SIZE = 20
MIN_ROOM_SIZE = 3
MAX_HALL_SIZE = 8
MIN_HALL_SIZE = 2
HALLWAY_THRESH = 8 # threshold for slowing down approach on hallway creation
BLOCK_SIZE = 10
# Direction defines used to modify multiplicants when adding coords
RIGHT = [1,0]
LEFT = [-1,0]
UP = [0,1]
DOWN = [0,-1]

def testcall():
    print("successfully called testcall in lib/levelcreation.py")

class Block(pygame.sprite.Sprite):
    '''This class represents the basic building blocks of the game level'''
    def __init__(self, image, pos):
        # call parent constructor
        super(Block, self).__init__()

        # default properties
        self.collision_detect = False # False means walkable, True is generally a wall
        self.side = None # For wall property, contains: LEFT, RIGHT, TOP, BOT

        # initialize image and position
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def changeImage(self, newimage):
        self.image = pygame.image.load(newimage).convert()


class Room:
    #NOTE: class attributes applied to all instances of this class used without self.

    def __init__(self, topleft, floor_images):
        self.connected = False
        self.blocks = [] # initialize empty block list
        self.wallblocks = []
        self.topleft = topleft
        self.floor_images = floor_images 
        # create randomized room
        rndx = random.randint(MIN_ROOM_SIZE,MAX_ROOM_SIZE)
        rndy = random.randint(MIN_ROOM_SIZE,MAX_ROOM_SIZE)
        self.size = [rndx,rndy]
        for x in range(0,rndx):
            for y in range(0,rndy):
                # get random image to create new block and add to blocks
                rnd_image = random.randint(0,len(floor_images)-1)
                newx = topleft[0] + BLOCK_SIZE*x 
                newy = topleft[1] + BLOCK_SIZE*y 
                self.blocks.append(Block(floor_images[rnd_image],[newx,newy]))

    def addBlock(self, block):
        self.blocks.append(block)

    def contains(self, xy):
        # returns true if xy coord is in room
        if self.topleft[0] > xy[0]:
            return False
        elif xy[0] > (self.topleft[0] + (self.size[0]*BLOCK_SIZE)):
            return False
        elif self.topleft[1] > xy[1]:
            return False
        elif xy[1] > (self.topleft[1] + (self.size[1]*BLOCK_SIZE)):
            return False
        else:
            return True

    def addWalls(self, image):
        # used to create walls around rooms - assumes margins are wide enough for placement from room creation
        #startxy = [top_left - block_size for top_left,block_size in zip(self.topleft,BLOCK_SIZE)]
        # create walls in order right, left, top, bottom
        startxy = [(self.topleft[0]+(self.size[0]*BLOCK_SIZE)),self.topleft[1]-BLOCK_SIZE]
        for y in range(0,self.size[1]+2): # creating right wall 
            newxy = [startxy[0], startxy[1] + (y*BLOCK_SIZE)]
            newblock = Block(image,newxy)
            newblock.side = RIGHT
            newblock.collision_detect = True
            self.wallblocks.append(newblock)
        startxy = [self.topleft[0]-BLOCK_SIZE, self.topleft[1]-BLOCK_SIZE] 
        for y in range(0,self.size[1]+1): # creation left wall 
            newxy = [startxy[0], startxy[1] + (y*BLOCK_SIZE)]
            newblock = Block(image,newxy)
            newblock.side = LEFT
            newblock.collision_detect = True
            self.wallblocks.append(newblock)
        startxy = [self.topleft[0]-BLOCK_SIZE, self.topleft[1]-BLOCK_SIZE] 
        for x in range(0,self.size[0]+1): # creation top wall 
            newxy = [startxy[0] + (x*BLOCK_SIZE), startxy[1]]
            newblock = Block(image,newxy)
            newblock.side = UP 
            newblock.collision_detect = True
            self.wallblocks.append(newblock)
        startxy = [self.topleft[0]-BLOCK_SIZE, (self.topleft[1] + (self.size[1]*BLOCK_SIZE))] 
        for x in range(0,self.size[0]+2): # creation bottom wall 
            newxy = [startxy[0] + (x*BLOCK_SIZE), startxy[1]]
            newblock = Block(image,newxy)
            newblock.side = DOWN
            newblock.collision_detect = True
            self.wallblocks.append(newblock)



class Hall:
    ''' when hall is created its only goal is to connect startxy and destxy '''
    def __init__(self, startxy, destxy, images, dest_room):
        self.blocks = [] # initialize empty block list
        self.wallblocks = [] 
        self.floor_images = images

        # generate hallway
        currxy = startxy # holds current xy variable as hallway moves along during creation
        first_run = True 
        hallway_connected = False
        max_hall = MAX_HALL_SIZE
        min_hall = MIN_HALL_SIZE
        threshold_level = 0
        while hallway_connected == False:
            # calculate delta to destination from start using list comprehension
            diffxy = [cur - des for cur, des in zip(currxy,destxy)]
            # if first section made then choose direction based on right,left,top,bottom property of wall block
            if first_run == True:
                direction = start_direction  
                first_run = False
            else:
                xory = random.randint(0,1) # pick x or y - consider weighting based off large delta (between x or y)
                # pick pos or neg -- consider adding weighting based on diff (ie let it go the wrong way 1/3 of the time)
                if xory == 0: # x path chosen
                    if diffxy[0] < 0: # negative delta means we need to go +x direction
                        direction = RIGHT
                    else:
                        direction = LEFT
                else: # y path chosen
                    if diffxy[1] < 0: # negative delta means we need to go +y direction
                        direction = UP
                    else:
                        direction = DOWN
            # check for near end condition 
            new_diffxy = [cur - des for cur, des in zip(currxy,destxy)]
            if (abs(new_diffxy[0]) > HALLWAY_THRESH) or (abs(new_diffxy[1]) > HALLWAY_THRESH):
                print "lowering hallway section creation to try and narrow in on destination"
                ++threshold_level
                if threshold_level > MAX_HALL_SIZE-2:
                    threshold_level = MAX_HALL_SIZE-2
                max_hall = max_hall - threshold_level
                min_hall = 1
            section_length = random.randint(min_hall,max_hall)
            # create hallway and update variables
            for i in range(0,section_length):
                # TODO while placing hallway blocks must check for collisions
                # 1. Collision with dest in which case halt successfully
                # 2. maybe implement collision with rooms -- TODO
                newxy = [currxy[0] + (direction[0]*i*BLOCK_SIZE),currxy[1] + (direction[1]*i*BLOCK_SIZE)]
                if dest_room.contains(newxy) == True:
                    hallway_connected = True
                rnd_hall_image = random.choice(self.floor_images)
                new_hall_block = Block(rnd_hall_image,newxy)
                self.wallblocks.append(new_hall_block)
            currxy = newxy
            # check for more basic end condition TODO change of delta 
            





# Loops until all rooms are connected, must be run after rooms are created
def createHallways(images, rooms):
    # global defaults for method TODO return saved_rooms to replace previous (needs updates)
    saved_rooms = rooms
    
    # main loop waiting for all hallways to be connected
    created_all_hallways = False
    hallways_made = 0
    hallways = [] # TODO replaces above and must return along with rooms
    while created_all_hallways == False:

        # pick start and dest room
        startxy, destxy = [[0,0],[0,0]]
        start_direction, dest_direction = [None,None] # holds right, left, top, bot for 
        valid = [False,False]
        for start_room in saved_rooms:
            if start_room.connected == True:
                continue
            wallblock = random.choice(start_room.wallblocks)
            startxy = wallblock.rect.topleft
            start_direction = wallblock.side
            valid[0] = True
        for dest_room in saved_rooms:
            if dest_room.connected == True:
                continue
            wallblock = random.choice(dest_room.wallblocks)
            destxy = wallblock.rect.topleft
            dest_direction = wallblock.size
            valid[1] = True
        # special condition when left to 1 unconnected room
        if (valid[0] == False) or (valid[1] == False):
            print "down to the end of rooms to connected"
            if (valid[0] == False) and (valid[1] == False): # special case I guess TODO
                print "both valid variables are false - no rooms left to connect? should i be here?"
            if valid[0] == False:
                # need to find a valid startxy
                print "have you ever seen me? REMOVE THIS PLEASE"
            else:
                # need to find a valid destxy should always be this one
                # TODO implement properly by picking random room excluding startxy room
                destxy = random.choice(random.choice(saved_rooms).wallblocks).rect.topleft
                valid[1] = True
        print "got to the end of picking startxy and destxy valid looks like: " + str(valid)
        print "startxy = " + str(startxy)
        print "destxy = " + str(destxy)
        new_hall = Hall(startxy,destxy,images)

        

                


        



                
                
