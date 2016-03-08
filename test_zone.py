#!/usr/bin/python2

import pygame
import random
from lib import levelcreation
from lib import imageloading

'''
parser = argparse.ArgumentParser(description='A Nethack inspired poor excuse for a game')
parser.add_argument('-d', action="store_true", default=False, dest='debug_mode', help='debug mode on')
args = parser.parse_args()
DEBUG = False
if args.debug_mode == True:
    print 'debug mode on'
    DEBUG = True
'''

# test call to all aux scripts
print("Startin TEST ZONE script -- YOU ARE IN DEBUG / TEST MODE")
'''
imageloading.initialize()
print str(imageloading.getActionImages('mob','glow','initial'))
print str(imageloading.getRandomStartAction('wall','brick'))
print str(imageloading.getRandomStartImage('wall','test','initial'))
exit()
'''


# initialize screen and background
pygame.init()
#screen = pygame.display.get_surface()
screen = pygame.display.set_mode((1000,1000))
pygame.display.set_caption('Basic Pygame Program')

# initialize Game Clock
clk = pygame.time.Clock()

# TODO testing custom Block class instantiation
'''
position = [10,10]
test = levelcreation.Block('images/tile_sample1.png', position)
#testimage = pygame.image.load('images/tile_sample1.png')
screen.blit(test.image, test.rect)
pygame.display.flip()
'''

# TODO testing custom room class instantiation
'''
pos = [100,100]
test1 = levelcreation.Block('images/tile1.png', pos)
size = [1,1]
floor_images = ['images/tile0.png','images/tile1.png','images/tile2.png']
test_room = levelcreation.Room(pos,floor_images)
#test_room.addBlock(test)
#test_room.addBlock(test1)
for i in test_room.blocks:
    screen.blit(i.image, i.rect)
'''

#screen.blit(test_room.blocks[*].image, test_room.blocks[*].rect)
#screen.blit(test_room.blocks[0].image, test_room.blocks[0].rect)

#testing Level implementation
#level0 = leLevel()

#TODO testing multiple room creation and smart placement
num_rooms = 20
#num_rooms = random.randint(1,10)
#floor_images = ['images/floor_tiles/tile0.png','images/floor_tiles/tile1.png','images/floor_tiles/tile2.png','images/floor_tiles/tile3.png','images/floor_tiles/tile4.png']
#if ((npos_e[0] >= cpos_s[0]) and (npos_s[0] <= cpos_e[0])) or ((npos_e[1] >= cpos_s[1]) and (npos_s[1] <= cpos_e[1])):
#cpos_s = check_room.topleft
#cpos_e = [cpos_s[0]+check_room.size[0],cpos_s[1]+check_room.size[1]]
room_check = []
number_rooms = 0
while number_rooms < 5:
#for i in range(0,num_rooms):
    #Create new room at random coords
    rndx = random.randint(0,levelcreation.LEVEL_SIZE)
    rndy = random.randint(0,levelcreation.LEVEL_SIZE)
    nroom = levelcreation.Room([rndx,rndy],'brick')
    npos_s = nroom.topleft
    npos_e = [npos_s[0]+(nroom.size[0]*levelcreation.BLOCK_SIZE),npos_s[1]+(nroom.size[1]*levelcreation.BLOCK_SIZE)]
    #print "adding room %d at x=%d and y=%d with xend=%d and yend=%d" % (i,rndx,rndy,npos_e[0],npos_e[1])
    # check for screen size violation
    if (npos_e[0] >= levelcreation.LEVEL_SIZE) or (npos_e[1] >= levelcreation.LEVEL_SIZE):
        pass
        #print "screen size violation on attempt %d" % i 
    else:
        if len(room_check) == 0 :
            room_check.append(nroom)
        else:
            # check for existing room violation -- loop through previously added rooms
            no_conflict = True
            for c_room in room_check:
                cpos_s = c_room.topleft
                cpos_e = [cpos_s[0]+(c_room.size[0]*levelcreation.BLOCK_SIZE),cpos_s[1]+(c_room.size[1]*levelcreation.BLOCK_SIZE)]
                #TODO add margin of separation between rooms
                if ((npos_e[0] >= cpos_s[0]) and (npos_s[0] <= cpos_e[0])) or ((npos_e[1] >= cpos_s[1]) and (npos_s[1] <= cpos_e[1])):
                    #print "block violation on attempt %d" % i
                    no_conflict = False

            if no_conflict == True:
                room_check.append(nroom)
                number_rooms += 1

# TODO testing add walls
'''
for sroom in room_list:
    # lay border of block tile5.img
    #wallxy = [room.topleft[0]-levelcreation.BLOCK_SIZE, room.topleft[1]-levelcreation.BLOCK_SIZE] 
    for x in range(0,sroom.size[0]):
        for y in range(0,sroom.size[1]):
            startx = sroom.topleft[0]-levelcreation.BLOCK_SIZE
            starty = sroom.topleft[1]-levelcreation.BLOCK_SIZE
            newx = startx + (levelcreation.BLOCK_SIZE*x)
            newy = starty + (levelcreation.BLOCK_SIZE*y)
            sroom.addBlock(levelcreation.Block('images/floor_tiles/tile5.png',[newx,newy])
'''
'''
for rr in room_check:
    sxy = [rr.topleft[0]-levelcreation.BLOCK_SIZE,rr.topleft[1]-levelcreation.BLOCK_SIZE]
    print "testing" + str(sxy)
    for xval in range(0,rr.size[0]+1):
        for yval in range(0,rr.size[1]+1):
            if ((xval > 0) and (xval < rr.size[0])) and ((yval > 0) and (yval < rr.size[1])):
                continue
            newxy = [sxy[0] + xval*levelcreation.BLOCK_SIZE,sxy[1] + yval*levelcreation.BLOCK_SIZE]
            #print "final val" + str(newxy)
            newblock = levelcreation.Block('images/floor_tiles/tile5.png',newxy)
            rr.topleft = [rr.topleft[0]-10,rr.topleft[1]-10]
            rr.size = [rr.size[0]+10,rr.size[1]+10]
            rr.addBlock(newblock)
            rr.wallblocks.append(newblock)
'''
'''
# TODO testing hallway add
hallways = []
hallway_image = 'images/floor_tiles/tile5.png'
humble_start = False
# calculate startxy and destxy
#startxy = room_check[random.randint(0,len(room_check))].wallblocks[random.randint(0,len(room_check.wallblocks))].rect.topleft
startxy = [0,0]
got_valid_room = False
while got_valid_room == False:
    ran_sel = random.randint(0,len(room_check)-1)
    getroom = room_check[ran_sel]
    getwallblocks = getroom.wallblocks
    getwallblock = getwallblocks[random.randint(0,len(getwallblocks)-1)]
    startxy = getwallblock.rect.topleft
    if getroom.connected == False:
        room_check[ran_sel].connected = True
        got_valid_room = True



destxy = [0,0]
got_valid_room = False
while got_valid_room == False:
    ran_sel = random.randint(0,len(room_check)-1)
    getroom = room_check[ran_sel]
    getwallblocks = getroom.wallblocks
    getwallblock = getwallblocks[random.randint(0,len(getwallblocks)-1)]
    destxy = getwallblock.rect.topleft
    if getroom.connected == False:
        room_check[ran_sel].connected = True
        got_valid_room = True

#destxy = room_check[random.randint(0,len(room_check))].wallblocks[random.randint(0,len(room_check.wallblocks))].rect.topleft
currxy = startxy
touched = False
x_start_var = 1
y_start_var = 1
print "startxy = " + str(startxy) + " and destxy = " + str(destxy)
'''
'''
TODO - #1: Room interception checks for hallways
       #2: Overall loop
       #3: Refinement (prevent multiple same direction builds)
       #4: Add doorway
while humble_start == False:
    addval = random.randint(4,10)
    xory = random.randint(0,1)
    # zip stops when first iterable is exhausted -- USING LIST COMPREHENSION
    diffxy = [cur - des for cur, des in zip(currxy,destxy)]
    #print "THIS IS DIFXY " + str(diffxy)
    #diffxy = (currxy - destxy)
    if xory == 0: # x chosen
        if diffxy[0] < 0: # negative diff means we need to go pos
            val = 1
        else:
            val = -1
        for j in range(1,addval):
            newxy = [currxy[0]+((val)*(j*10)),currxy[1]]
            bb = levelcreation.Block(hallway_image,newxy)
            hallways.append(bb)
    else: # y chosen
        if diffxy[1] < 0:
            val = 1
        else:
            val = -1
        for j in range(1,addval):
            newxy = [currxy[0],currxy[1]+((val)*(j*10))]
            bb = levelcreation.Block(hallway_image,newxy)
            hallways.append(bb)
    currxy = newxy
    # smart end condition check
    if touched == False:
        touched = True
        if diffxy[0] < 0:
            x_start_var = -1
        if diffxy[1] < 0:
            y_start_var = -1

    # if original change variables have changed then stop
    stop = 0
    if (diffxy[0] < 0) and (x_start_var == 1): # x was positive and now is negative
        stop = stop + 1
    if (diffxy[0] > 0) and (x_start_var == -1): # x was negative and now is positive
        stop = stop + 1
    if (diffxy[1] < 0) and (y_start_var == 1): # y was positive and now is negative
        stop = stop + 1
    if (diffxy[1] > 0) and (y_start_var == -1): # y was negative and now is positive
        stop = stop + 1
    if stop >= 2:
        humble_start = True
    if currxy == destxy:
        print "miracles do happen eventually"
        humble_start = True

    
        

'''

# test out "better" wall and hallway creation
for room in room_check:
    room.addWalls()

# TODO call test hallway stuff
'''
hallways = []
image = ['images/floor_tiles/tile5.png']
startxy = [0,0]
dest_room = random.choice(room_check)
destxy = random.choice(dest_room.wallblocks).rect.topleft
newhall = levelcreation.Hall(startxy, levelcreation.DOWN, destxy, image,dest_room)
hallways.append(newhall)
'''
levelcreation.rooms = room_check
hallways = []
#image = ['images/floor_tiles/tile5.png']
hallways = levelcreation.createHallways('brick')

# display all rooms in room_list
for room in levelcreation.rooms:
    for k in room.blocks:
        screen.blit(k.image, k.rect)
    for k in room.wallblocks:
        screen.blit(k.image, k.rect)

# display all hallways
for hall in hallways:
    for k in hall.blocks:
        screen.blit(k.image,k.rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exited through canceling screen")
            exit()
        elif event.type == pygame.KEYDOWN:
            print("Pressed KEYDOWN")
            pass
        else:
            pass
        clk.tick(60) # update x times per second
        pygame.display.flip()
