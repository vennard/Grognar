#!/usr/bin/python2

import argparse, pygame, random, os, sys, getopt
from lib import levelcreation

''' Defines '''

# initialize screen 0 - full screen, or 1 - windowed mode
screen, wh = levelcreation.initializeGame(1)

level = levelcreation.Level()
level.rooms = levelcreation.createRooms(7,'brick') # TODO fix with better number and theme array
level.hallways = levelcreation.createHallways(level.rooms,'brick') # TODO fix with better theme


# display all rooms in room_list
for room in level.rooms:
    for k in room.blocks:
        screen.blit(k.image, k.rect)

for hall in level.hallways:
    for k in hall.blocks:
        screen.blit(k.image, k.rect)

# start main game loop
clk = pygame.time.Clock() # initialize game clock
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
