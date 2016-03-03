#!/usr/bin/python2

import pygame
import random
from lib import levelcreation

# test call to all aux scripts
print("Launching main.py script")
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
num_rooms = 100
#num_rooms = random.randint(1,10)
floor_images = ['images/tile0.png','images/tile1.png','images/tile2.png','images/tile3.png','images/tile4.png']
room_list = []
#if ((npos_e[0] >= cpos_s[0]) and (npos_s[0] <= cpos_e[0])) or ((npos_e[1] >= cpos_s[1]) and (npos_s[1] <= cpos_e[1])):
#cpos_s = check_room.topleft
#cpos_e = [cpos_s[0]+check_room.size[0],cpos_s[1]+check_room.size[1]]
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
        for b in nroom.blocks:
            b.changeImage('images/tile1.png')
    else:
        room_list.append(nroom)


# display all rooms in room_list
for room in room_list:
    for k in room.blocks:
        screen.blit(k.image, k.rect)



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
