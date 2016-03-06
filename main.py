#!/usr/bin/python2

''' Defines '''
NUMBER_OF_ROOMS = 7

import argparse, pygame, random, os, sys, getopt
from lib import levelcreation

# initialize screen and background
pygame.init()
screen = pygame.display.set_mode((1000,1000))
pygame.display.set_caption('Basic Pygame Program')

# initialize Game Clock
clk = pygame.time.Clock()

# load in images
floor_images = os.listdir('images/floor_tiles')
ss = "images/floor_tiles/"
floor_images = [ss + s for s in floor_images]
#character_image = 'images/dumb_guy.png'

print floor_images
# Generate Rooms
room_check = []
rooms_created = 0
while rooms_created < NUMBER_OF_ROOMS:
    # TODO get random room theme (subset of floor_tiles)
    room_images = floor_images # TODO change this

    # get random coords for rooms topleft and create room
    rndxy = [random.randint(0,levelcreation.LEVEL_SIZE), random.randint(0,levelcreation.LEVEL_SIZE)]
    new_room = levelcreation.Room(rndxy, room_images)

    # get new_room size coords
    npos_s = new_room.topleft
    npos_e = [npos_s[0]+(new_room.size[0]*levelcreation.BLOCK_SIZE),npos_s[1]+(new_room.size[1]*levelcreation.BLOCK_SIZE)]
    
    # check for screen edge violations
    if (npos_e[0] >= levelcreation.LEVEL_SIZE) or (npos_e[1] >= levelcreation.LEVEL_SIZE):
        continue
    
    # check for first room
    if len(room_check) == 0:
        room_check.append(new_room)
        continue

    # check for existing room violation 
    no_conflict = True
    for rc in room_check:
        # get existing room dimensions
        cpos_s = rc.topleft
        cpos_e = [cpos_s[0]+(rc.size[0]*levelcreation.BLOCK_SIZE), cpos_s[1]+(rc.size[1]*levelcreation.BLOCK_SIZE)]
        # TODO add margin of separation between rooms
        if ((npos_e[0] > cpos_s[0]) and (npos_s[0] < cpos_e[0])) or ((npos_e[1] > cpos_s[1]) and (npos_s[1] < cpos_e[1])):
        #if ((npos_e[0] >= cpos_s[0]) and (npos_s[0] <= cpos_e[0])) or ((npos_e[1] >= cpos_s[1]) and (npos_s[1] <= cpos_e[1])):
            no_conflict = False

    # TODO add walls and check for conlficts... conflicts here can reset room creation
    if no_conflict == True:
        room_check.append(new_room)
        rooms_created = rooms_created + 1

# TODO create hallways -- use similar while loop as above

# display all rooms in room_list
for room in room_check:
    for k in room.blocks:
        screen.blit(k.image, k.rect)


# start main game loop
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
