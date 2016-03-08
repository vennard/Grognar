# Contains methods and resources for level generation

import pygame, random, os, imageloading, time

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

screen_width = 1000
screen_height = 1000

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

def initializeGame(mode):
    # mode: 0 - fullscreen, 1 - windowed
    # returns: screen, screenwh[w,h]
    pygame.init()
    if mode == 0: # TODO must implement an exit for fullscreen mode!!!
        print "fullscreen mode selected: " + str(screen_width) + "x" + str(screen_height)
        screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        screeninfo = pygame.display.Info()
        screenwh = [screeninfo.current_w,screeninfo.current_h]
    else:
        screenwh = [1000,1000]
        screen = pygame.display.set_mode((screenwh[0],screenwh[1]))
        print "windowed mode selected: " + str(screen_width) + "x" + str(screen_height)
    pygame.display.set_caption('Grognar in Action')
    return screen, screenwh

def createRooms(number, themes):
    # input: number - number of rooms to create
    #        themes - array of themes to use
    # returns: array of rooms
    rooms_created = 0
    rooms = [] 
    time0 = time.time()
    while rooms_created < number:
        # create new room with random xy and random theme 
        rndxy = [random.randint(0,screen_width), random.randint(0,screen_height)]
        new_room = Room(rndxy,random.choice(themes)) 

        # get size coords
        npos_s,npos_e = new_room.topleft,new_room.corners[2]

        # check for screen edge violation
        if (new_room.corners[2][0] >= screen_width) or (new_room.corners[2][1] >= screen_height):
            continue

        # check for first room
        if len(rooms) == 0:
            rooms.append(new_room)
            continue

        # check for existing room violation 
        no_conflict = True
        for rc in rooms:
            # check each corner of room for conflict
            for corner in new_room.corners:
                if rc.contains(corner,1):
                    print "found conflict with corner coords: " + str(corner)
                    no_conflict = False

        if no_conflict == True:
            rooms.append(new_room)
            rooms_created += 1

    for rm in rooms:
        rm.addWalls()
    time_elapsed = time.time() - time0
    print "done creating rooms in " + str(time_elapsed) + " seconds"
    return rooms
            
 


class Level:
    ''' This class holds important level data '''
    def __init__(self):
        self.rooms = []
        self.hallways = []
        self.items = []
        self.mobs = []


class Block(pygame.sprite.Sprite):
    '''This class represents the basic building blocks of the game level'''
    # TODO implementing choosing own image - must load once in init
    # always created with block_action = any _leading action
    def __init__(self, block_type, block_theme, pos):
        # call parent constructor
        super(Block, self).__init__()

        # default properties
        self.collision_detect = False # False means walkable, True is generally a wall
        self.side = None # For wall property, contains: LEFT, RIGHT, TOP, BOT
        self.block_type = block_type
        self.block_theme = block_theme

        # load image filepaths if not done
        if imageloading.ready == False: 
            imageloading.initialize()
            imageloading.ready = True

        # pick initial action and randomly chosen _*.png as start image
        self.actions = imageloading.getActions(block_type,block_theme)
        self.action_state = imageloading.getRandomStartAction(block_type,block_theme)

        # load image
        temp_path = imageloading.getRandomStartImage(block_type,block_theme,self.action_state)
        temp = pygame.image.load(temp_path).convert()
        self.image = pygame.transform.scale(temp,(BLOCK_SIZE,BLOCK_SIZE))

        # initialize rect and position
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def changeImage(self, newimage):
        self.image = pygame.image.load(newimage).convert()



class Room:
    #NOTE: class attributes applied to all instances of this class used without self.

    def __init__(self, topleft, theme):
        self.connected = False
        self.blocks = [] # initialize empty block list
        self.wallblocks = []
        self.theme = theme
        # create randomized room
        rndx = random.randint(MIN_ROOM_SIZE,MAX_ROOM_SIZE)
        rndy = random.randint(MIN_ROOM_SIZE,MAX_ROOM_SIZE)
        self.size = [rndx,rndy]
        self.topleft = topleft
        topright = [self.topleft[0]+(self.size[0]*BLOCK_SIZE),self.topleft[1]]
        bottomright = [self.topleft[0]+(self.size[0]*BLOCK_SIZE),self.topleft[1]+(self.size[1]*BLOCK_SIZE)]
        bottomleft = [self.topleft[0],self.topleft[1]+(self.size[1]*BLOCK_SIZE)]
        self.corners = [topleft,topright,bottomright,bottomleft]
        for x in range(0,rndx):
            for y in range(0,rndy):
                # get random image to create new block and add to blocks
                newx = topleft[0] + BLOCK_SIZE*x 
                newy = topleft[1] + BLOCK_SIZE*y 
                self.blocks.append(Block('floor',self.theme,[newx,newy]))

    def addBlock(self, block):
        self.blocks.append(block)

    def contains(self, xy, p):
        # returns true if xy coord is in room
        # p[lus] - searches border + plus value
        if (self.corners[0][0]-p <= xy[0] <= self.corners[1][0]+p) and (self.corners[0][1]-p <= xy[1] <= self.corners[2][1]+p):
            return True
        else:
            return False

    def addWalls(self):
        # used to create walls around rooms - assumes margins are wide enough for placement from room creation
        startxy = [(self.topleft[0]+(self.size[0]*BLOCK_SIZE)),self.topleft[1]-BLOCK_SIZE]
        for y in range(0,self.size[1]+2): # creating right wall 
            newxy = [startxy[0], startxy[1] + (y*BLOCK_SIZE)]
            newblock = Block('wall',self.theme,newxy)
            newblock.side = RIGHT
            newblock.collision_detect = True
            newblock.image = pygame.transform.rotate(newblock.image,90)
            self.blocks.append(newblock)
        startxy = [self.topleft[0]-BLOCK_SIZE, self.topleft[1]-BLOCK_SIZE] 
        for y in range(0,self.size[1]+1): # creation left wall 
            newxy = [startxy[0], startxy[1] + (y*BLOCK_SIZE)]
            newblock = Block('wall',self.theme,newxy)
            newblock.side = LEFT
            newblock.image = pygame.transform.rotate(newblock.image,270)
            newblock.collision_detect = True
            self.blocks.append(newblock)
        startxy = [self.topleft[0]-BLOCK_SIZE, self.topleft[1]-BLOCK_SIZE] 
        for x in range(0,self.size[0]+1): # creation top wall 
            newxy = [startxy[0] + (x*BLOCK_SIZE), startxy[1]]
            newblock = Block('wall',self.theme,newxy)
            newblock.side = UP 
            newblock.collision_detect = True
            self.blocks.append(newblock)
        startxy = [self.topleft[0]-BLOCK_SIZE, (self.topleft[1] + (self.size[1]*BLOCK_SIZE))] 
        for x in range(0,self.size[0]+2): # creation bottom wall 
            newxy = [startxy[0] + (x*BLOCK_SIZE), startxy[1]]
            newblock = Block('wall',self.theme,newxy)
            newblock.side = DOWN
            newblock.collision_detect = True
            newblock.image = pygame.transform.rotate(newblock.image,180)
            self.blocks.append(newblock)



class Hall:
    ''' when hall is created its only goal is to connect startxy and destxy '''
    # TODO add walls to hallway
    # TODO cleanup overlap with rooms
    # TODO add door at any intersection point with wall
    def __init__(self, startxy, start_direction, destxy, dest_room, theme):
        self.blocks = [] # initialize empty block list
        self.wallblocks = [] 
        self.theme = theme

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
                if dest_room.contains(newxy, 0) == True:
                    hallway_connected = True
                new_hall_block = Block('hall',self.theme,newxy)
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


# Loops until all rooms are connected, must be run after rooms are created
def createHallways(rooms,theme):
    # main loop waiting for all hallways to be connected
    # returns array of halls
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
                # TODO lies, ive seen unconnected rooms before -- what is happening?? FIX
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

        prev = max
        for wallblock in start_room.blocks:
            delta = [x - y for x, y in zip(wallblock.rect.topleft,destxy)]
            if wallblock.block_type == 'wall':
                val = abs(delta[0]) + abs(delta[1])
                if val < prev:
                    prev = val
                    startxy = wallblock.rect.topleft
                    start_direction = wallblock.side
        prev = max
        for wallblock in dest_room.blocks:
            if wallblock.block_type == 'wall':
                delta = [x - y for x, y in zip(wallblock.rect.topleft,startxy)]
                val = abs(delta[0]) + abs(delta[1])
                if val < prev:
                    prev = val
                    destxy = wallblock.rect.topleft

        print "startxy = " + str(startxy)
        print "destxy= " + str(destxy)
        new_hall = Hall(startxy, start_direction, destxy, dest_room, theme)
        hallways.append(new_hall)
        hallways_made = hallways_made + 1
        if hallways_made >= 7:
            created_all_hallways = True
    return hallways
        

                


        



                
                
