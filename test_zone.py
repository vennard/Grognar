#!/usr/bin/python2

import pygame
import random
from lib import levelcreation

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
levelcreation.testcall()

# initialize screen and background
pygame.init()
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

#TODO testing multiple room creation and smart placement
num_rooms = 10
#num_rooms = random.randint(1,10)
floor_images = ['images/floor_tiles/tile0.png','images/floor_tiles/tile1.png','images/floor_tiles/tile2.png','images/floor_tiles/tile3.png','images/floor_tiles/tile4.png']
#if ((npos_e[0] >= cpos_s[0]) and (npos_s[0] <= cpos_e[0])) or ((npos_e[1] >= cpos_s[1]) and (npos_s[1] <= cpos_e[1])):
#cpos_s = check_room.topleft
#cpos_e = [cpos_s[0]+check_room.size[0],cpos_s[1]+check_room.size[1]]
room_check = []
for i in range(0,num_rooms):
    #Create new room at random coords
    rndx = random.randint(0,levelcreation.LEVEL_SIZE)
    rndy = random.randint(0,levelcreation.LEVEL_SIZE)
    nroom = levelcreation.Room([rndx,rndy],floor_images)
    npos_s = nroom.topleft
    npos_e = [npos_s[0]+(nroom.size[0]*levelcreation.BLOCK_SIZE),npos_s[1]+(nroom.size[1]*levelcreation.BLOCK_SIZE)]
    print "adding room %d at x=%d and y=%d with xend=%d and yend=%d" % (i,rndx,rndy,npos_e[0],npos_e[1])
    # check for screen size violation
    if (npos_e[0] >= levelcreation.LEVEL_SIZE) or (npos_e[1] >= levelcreation.LEVEL_SIZE):
        print "screen size violation on attempt %d" % i 
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
                    print "block violation on attempt %d" % i
                    no_conflict = False

            if no_conflict == True:
                room_check.append(nroom)

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
            rr.addWall(newblock)

# TODO testing hallway add
hallways = []
hallway_image = 'images/floor_tiles/tile5.png'
hallways_connected = False
while hallways_connected == False:
    '''
     Plan for hallway 'algorithm'
        1.Get wall coords from room (not corner)
        2.Convert to doorway and pick room to connect to
            a.Pick room using closest side to doorway
        3.build hallway (TODO room conflicts) using random y x movement
            a.must exit on meeting target room 
            b.mark both rooms connected
        4.check for all rooms connected to exit
    '''
    for nr in room_check:
        if nr.connected == False:
            sel_room = nr
            break
    #get wall coords
    wallblock = sel_room.wallblocks[0]
    rndxy = wallblock.rect.topleft
    #TODO picking dumb dest coords for testing
    '''
    dest_xy = [1000,1000]
    crude_change = [rndxy[0]-dest_xy[0],rndxy[1]-dest_xy[1]]
    # example [717-1000 = -283,8-1000=-9992]
    if crude_change < [0,0]:
        numtoadd = random.randint(3,10)
        for j in range(0,numtoadd):
            print "add hallway"
            bb = levelcreation.Block(hallway_image,[rndxy[0]+(j*10),rndxy[1]])
            hallways.append(bb)
    '''
    destxy = [1000,1000]
    currxy = rndxy
    connect_test = False
    while connect_test == False:
        print "loopping"
        addval = random.randint(4,10)
        xory = random.randint(0,1)
        newcurr = currxy
        if ((currxy[0]+(addval*10)) > destxy[0]) and ((currxy[1]+(addval*10)) > destxy[1]):
            connect_test = True
        elif (currxy[0]+(addval*10)) > destxy[0]:
            xory = 1
        elif (currxy[1]+(addval*10)) > destxy[1]: 
            xory = 0

        if xory == 0: # x chosen
            for j in range(1,addval):
                newcur = [currxy[0]+(j*10),currxy[1]]
                bb = levelcreation.Block(hallway_image,newcur)
                hallways.append(bb)
        else: # y chosen
            for j in range(1,addval):
                newcur = [currxy[0],currxy[1]+(j*10)]
                bb = levelcreation.Block(hallway_image,newcur)
                hallways.append(bb)
        currxy = newcur
        if currxy > destxy:
            connect_test = True




    print "test done"
    hallways_connected = True
    # TODO don't forget check for hallways connected to exit loop


# display all rooms in room_list
for room in room_check:
    for k in room.blocks:
        screen.blit(k.image, k.rect)

# display all hallways
for hall in hallways:
    screen.blit(hall.image,hall.rect)

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
