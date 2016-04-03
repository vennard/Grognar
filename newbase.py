#!/usr/bin/python2

import pygame
from lib import levelgenerator, imageloading 
from lib import block

# Test Zone
pygame.init()
imageloading.initialize()
screen = pygame.display.set_mode((1000,1000))
level = levelgenerator.Level([100,100])

# Create rooms
level.generateRooms(4)
level.writeToGrid(level.rooms)
level.generateHalls()
level.writeToGrid(level.hallways)

start = level.rooms[0].topleft
char = block.Block(start)
image, array_images = imageloading.getActionImages('mob','blob','initia')
char.loadImages(array_images)
level.grid[char.pos[0]][char.pos[1]] = char

# End 
#test_images = ['images/test/type0/_initial/0.png','images/test/type0/_initial/1.png','images/test/type0/_initial/2.png','images/test/type0/_initial/3.png']
#level.grid[1][1].loadImages(test_images)
level.updateLevel(screen)

# start main game loop
clk = pygame.time.Clock() # initialize game clock
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exited through canceling screen")
            exit()
        elif event.type == pygame.KEYDOWN:
            # capture keypress
            if event.key == pygame.K_UP:
                char.pos[1] -= 1
                print("UP")
            elif event.key == pygame.K_DOWN:
                char.pos[1] += 1
                print("DOWN")
            elif event.key == pygame.K_RIGHT:
                char.pos[0] += 1
                print("RIGHT")
            elif event.key == pygame.K_LEFT:
                char.pos[0] -= 1
                print("LEFT")
            else:
                print("not mapped keypress")
            pass
        else:
            pass
        clk.tick(60) # update x times per second
        # update and display game world
        char.moveBlock(char.pos)
        level.grid[char.pos[0]][char.pos[1]] = char
        level.updateLevel(screen)
        pygame.display.flip()

