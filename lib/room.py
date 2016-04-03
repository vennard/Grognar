# room generation code
import pygame, random
import imageloading, block

# defaults
MAX = 20
MIN = 3
RIGHT = [1,0]
LEFT = [-1,0]
UP = [0,1]
DOWN = [0,-1]

def createRooms(num, levelsize):
    rooms = []
    rooms_created = 0
    while rooms_created < num:
        # create new room at xy
        rndxy = [random.randrange(levelsize[0]),random.randrange(levelsize[1])]
        new = Room(rndxy)

        # get size coords
        npos_s, npos_e = new.topleft, new.botright

        # check for screen edge violation
        if (new.botright[0] >= levelsize[0]) or (new.botright[1] >= levelsize[1]):
            continue

        # check for first room
        if len(rooms) == 0:
            new.addWalls()
            rooms.append(new)
            rooms_created += 1
            continue

        # check for conflicts with existing rooms
        no_conflict = True
        for rc in rooms:
            if rc.containsRoom(new) == True:
                no_conflict = False
        if no_conflict == True:
            new.addWalls()
            rooms.append(new)
            rooms_created += 1
    return rooms

class Room:
    def __init__(self, topleft):
        self.connected = False
        self.theme = random.choice(imageloading.getThemes('floor')) 
        self.blocks = [] # initialize empty block list
        # create randomized room
        self.size = [random.randint(MIN,MAX),random.randint(MIN,MAX)]
        self.topleft = topleft
        self.botright = [topleft[0]+self.size[0],topleft[1]+self.size[1]]
        for x in range(0,self.size[0]):
            for y in range(0,self.size[1]):
                # get random image to create new block and add to blocks
                pos = [topleft[0] + x, topleft[1] + y]
                new_block = block.Block(pos)
                new_block.solid = False
                new_block.setImage('floor',self.theme)
                self.blocks.append(new_block)
                

    def containsRoom(self, room):
        # returns true if self.room overlaps with room
        if ((self.topleft[0] <= room.topleft[0] <= self.botright[0]) or (self.topleft[0] <= room.botright[0] <= self.botright[0])) and ((self.topleft[1] <= room.topleft[1] <= self.botright[1]) or (self.topleft[1] <= room.botright[1] <= self.botright[1])):
            return True
        return False

    def contains(self, xy):
        # returns true if self.room overlaps with room
        if ((self.topleft[0] <= xy[0] <= self.botright[0]) or (self.topleft[0] <= xy[0] <= self.botright[0])) and ((self.topleft[1] <= xy[1] <= self.botright[1]) or (self.topleft[1] <= xy[1] <= self.botright[1])):
            return True
        return False


    def addWalls(self):
        # used to create walls around rooms - assumes margins are wide enough for placement from room creation
        startxy = [(self.topleft[0]+self.size[0]),self.topleft[1]-1]
        # get new theme
        wall_theme = random.choice(imageloading.getThemes('wall'))
        for y in range(0,self.size[1]+2): # creating right wall 
            newxy = [startxy[0], startxy[1] + y]
            newblock = block.Block(newxy)
            newblock.setImage('wall',wall_theme)
            newblock.side = RIGHT
            newblock.solid = True
            newblock.image = pygame.transform.rotate(newblock.image,90)
            self.blocks.append(newblock)
        startxy = [self.topleft[0]-1, self.topleft[1]-1] 
        for y in range(0,self.size[1]+1): # creation left wall 
            newxy = [startxy[0], startxy[1] + y]
            newblock = block.Block(newxy)
            newblock.setImage('wall',wall_theme)
            newblock.side = LEFT
            newblock.image = pygame.transform.rotate(newblock.image,270)
            newblock.solid = True
            self.blocks.append(newblock)
        startxy = [self.topleft[0]-1, self.topleft[1]-1] 
        for x in range(0,self.size[0]+1): # creation top wall 
            newxy = [startxy[0] + x, startxy[1]]
            newblock = block.Block(newxy)
            newblock.setImage('wall',wall_theme)
            newblock.side = UP 
            newblock.solid = True
            self.blocks.append(newblock)
        startxy = [self.topleft[0]-1, (self.topleft[1] + self.size[1])] 
        for x in range(0,self.size[0]+2): # creation bottom wall 
            newxy = [startxy[0] + x, startxy[1]]
            newblock = block.Block(newxy)
            newblock.setImage('wall',wall_theme)
            newblock.side = DOWN
            newblock.solid = True
            newblock.image = pygame.transform.rotate(newblock.image,180)
            self.blocks.append(newblock)





