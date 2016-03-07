# Contains methods and resources for level generation

import pygame, random, os

WHITE = (255,255,255)
LEVEL_SIZE = 1000
MAX_ROOM_SIZE = 20
MIN_ROOM_SIZE = 3
MAX_HALL_SIZE = 8
MIN_HALL_SIZE = 2
HALLWAY_THRESH = 75 # threshold for slowing down approach on hallway creation
BLOCK_SIZE = 10
# Direction defines used to modify multiplicants when adding coords
RIGHT = [1,0]
LEFT = [-1,0]
UP = [0,1]
DOWN = [0,-1]


rooms = [] # holds all rooms for level

'''
all_image_paths format
0 - floor tiles
1 - door tiles
2 - item tiles
3 - wall right 
4 - wall left
5 - wall up
6 - wall down
7 - test tiles
'''
def loadImagePaths():
    print("attempting to load all images")
    path0='images/'
    pathfloor = 'floor_tiles/'
    pathdoor = 'door_tiles/'
    pathitem = 'item_tiles/'
    wallright = 'wall_tiles/RIGHT/'
    wallleft = 'wall_tiles/LEFT/'
    wallup = 'wall_tiles/UP/'
    walldown = 'wall_tiles/DOWN/'
    test = 'test_tiles/'
    iarray = [pathfloor,pathdoor,pathitem,wallright,wallleft,wallup,walldown,test]
    image_paths = []
    for path1 in iarray:
        image_names = os.listdir(path0 + path1)
        image_paths.append([path0 + path1 + name for name in image_names])
    print "done loading image paths"
    return image_paths

    
class Level:
    ''' This class holds important level data '''
    def __init__(self):
        #load images
        self.all_image_paths = loadImagePaths()
        self.rooms = []


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
    def __init__(self, startxy, start_direction, destxy, images, dest_room):
        self.blocks = [] # initialize empty block list
        self.wallblocks = [] 
        self.floor_images = images

        print "CREATING NEW HALL"
        # generate hallway
        currxy = startxy # holds current xy variable as hallway moves along during creation
        first_run = True 
        hallway_connected = False
        max_hall = MAX_HALL_SIZE
        min_hall = MIN_HALL_SIZE
        original_direction = [0,0]
        threshold_level = 0
        while hallway_connected == False:
            # calculate delta to destination from start using list comprehension
            diffxy = [cur - des for cur, des in zip(currxy,destxy)]
            # if first section made then choose direction based on right,left,top,bottom property of wall block
            if first_run == True:
                direction = start_direction  
                if diffxy[0] < 0:
                    original_direction[0] = RIGHT
                else:
                    original_direction[0] = LEFT
                if diffxy[1] < 0:
                    original_direction[1] = UP
                else:
                    original_direction[1] = DOWN
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
            #if (abs(diffxy[0]) < HALLWAY_THRESH) and (abs(diffxy[1]) < HALLWAY_THRESH):
            if abs(diffxy[0]) + abs(diffxy[1]) < HALLWAY_THRESH:
                threshold_level = threshold_level + 1
                max_hall = max_hall - threshold_level
                min_hall = min_hall - threshold_level
                if max_hall < 3:
                    max_hall = 3
                if min_hall < 2:
                    min_hall = 2
                print "threshold zone " + str(threshold_level) + "with diffxy " + str(diffxy)
            section_length = random.randint(min_hall,max_hall)
            # create hallway and update variables
            for i in range(0,section_length):
                # while placing hallway blocks must check for collisions
                newxy = [currxy[0] + (direction[0]*i*BLOCK_SIZE),currxy[1] + (direction[1]*i*BLOCK_SIZE)]
                if dest_room.contains(newxy) == True:
                    hallway_connected = True
                rnd_hall_image = random.choice(self.floor_images)
                new_hall_block = Block(rnd_hall_image,newxy)
                self.blocks.append(new_hall_block)
            currxy = newxy
            # check for more basic end condition TODO change of delta 
            stop = 0
            if (diffxy[0] < 0) and (original_direction[0] == LEFT):
                stop = stop + 1
            if (diffxy[0] > 0) and (original_direction[0] == RIGHT):
                stop = stop + 1
            if (diffxy[1] < 0) and (original_direction[1] == DOWN):
                stop = stop + 1
            if (diffxy[1] > 0) and (original_direction[1] == UP):
                stop = stop + 1
            if stop >= 2:
                hallway_connected = True
                print "stop value is " + str(stop)
            # TODO add hallway cleanup and doorways


# Loops until all rooms are connected, must be run after rooms are created
def createHallways(images):
    # main loop waiting for all hallways to be connected
    created_all_hallways = False
    hallways_made = 0
    hallways = [] # TODO replaces above and must return along with rooms
    while created_all_hallways == False:
        # pick start and dest room
        startxy, destxy = [[0,0],[0,0]]
        start_direction, dest_direction = [None,None] # holds right, left, top, bot for 
        startid = 0 
        # assurance on choosing rooms
        start_room_chosen = False
        if len(rooms) < 3:
            print "must have more then 2 rooms"
            exit()
        while start_room_chosen == False:
            for room in rooms:
                if room.connected == False:
                    # found an unconnected room aka the best option
                    start_room = room
                    start_room_chosen = True
                    room.connected = True
            # policy is if no unconnected rooms exist there should be no start room...
            if start_room_chosen == False:
                start_room = random.choice(rooms)
                start_room_chosen = True
                print "start room not finding unconnected room - chosen random one with id " + str(startid)
            
        # assurance finding destination room
        dest_room_chosen = False
        while dest_room_chosen == False:
            for room in rooms:
                if room.connected == False:
                    dest_room = room
                    dest_room_chosen = True
                    room.connected = True
            if dest_room_chosen == False:
                print "no available unconnected rooms for dest so picking random one"
                rnd_room = random.choice(rooms)
                if rnd_room is start_room:
                    print "youre trying to grab the same room again dammit"
                    continue
                else:
                    dest_room = rnd_room
                    dest_room_chosen = True

        # choose near sided walls to generate startxy and destxy on
        startxy = start_room.topleft
        destxy = dest_room.topleft
        # find closest startxy first
        # startxy - destxy = deltaxy or exp if -13,0 we need to go +x to reach dest
        '''
        example: startxy = [8,0] destxy = [4,6]
            delta = startxy - destxy
        1: delta = [4,-6] newxy 10,0 
        1: delta = 6, -6
        
        '''
        prev = 2000
        for wallblock in start_room.wallblocks:
            delta = [x - y for x, y in zip(wallblock.rect.topleft,destxy)]
            val = abs(delta[0]) + abs(delta[1])
            if val < prev:
                prev = val
                startxy = wallblock.rect.topleft
                start_direction = wallblock.side
        prev = 2000
        for wallblock in dest_room.wallblocks:
            delta = [x - y for x, y in zip(wallblock.rect.topleft,startxy)]
            val = abs(delta[0]) + abs(delta[1])
            if val < prev:
                prev = val
                destxy = wallblock.rect.topleft

        print "startxy = " + str(startxy)
        print "destxy= " + str(destxy)
        new_hall = Hall(startxy, start_direction, destxy, images, dest_room)
        hallways.append(new_hall)
        hallways_made = hallways_made + 1
        if hallways_made >= 7:
            created_all_hallways = True
        print "HALLWAYS CREATED " + str(hallways_made)
    return hallways
        

                


        



                
                
