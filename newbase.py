#!/usr/bin/python2

import pygame
from lib import levelgenerator, imageloading 
from lib import block, mob

# Test Zone
pygame.init()
imageloading.initialize()
SIZE = 1300
level_size = SIZE / block.SCALE
print "level size is " + str(level_size)

screen = pygame.display.set_mode((SIZE,SIZE))
level = levelgenerator.Level([level_size,level_size])

# Create rooms
level.generateRooms(7)
level.writeToGrid(level.rooms)
level.generateHalls(4)
level.writeToGrid(level.hallways)

# character creation
char = mob.Character(level.rooms[0],'blob','initial')
level.updateLayer(char.block, 0)

# End 
#test_images = ['images/test/type0/_initial/0.png','images/test/type0/_initial/1.png','images/test/type0/_initial/2.png','images/test/type0/_initial/3.png']
#level.grid[1][1].loadImages(test_images)
level.updateLevel(screen)

# start main game loop
clk = pygame.time.Clock() # initialize game clock
while 1:
    for event in pygame.event.get():
        xadd = 0
        yadd = 0
        if event.type == pygame.QUIT:
            print("Exited through canceling screen")
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                exit()
            # capture keypress - check for diagonal (two keys pressed at same time) first
            if event.key == pygame.K_UP or event.key == pygame.K_KP8:
                yadd = -1
                print("UP")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                yadd = 1
                print("DOWN")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                xadd = 1
                print("RIGHT")
            elif event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                xadd = -1
                print("LEFT")
            elif event.key == pygame.K_KP7:
                xadd = -1
                yadd = -1
                print("UP LEFT")
            elif event.key == pygame.K_KP9:
                xadd = 1
                yadd = -1
                print("UP RIGHT")
            elif event.key == pygame.K_KP3:
                xadd = 1
                yadd = 1
                print("DOWN RIGHT")
            elif event.key == pygame.K_KP1:
                xadd = -1
                yadd = 1
                print("DOWN LEFT")
            else:
                print("not mapped keypress")
            pass
        else:
            pass
        clk.tick(60) # update x times per second
        # update and display game world
        level.moveActive(char.block, [char.block.pos[0]+xadd,char.block.pos[1]+yadd])
        level.processShadows(char.block.pos,6)
        level.updateLevel(screen)
        pygame.display.flip()

