#!/usr/bin/python2

import pygame
from lib import levelgen, imageloading 

# Test Zone
pygame.init()
imageloading.initialize()
screen = pygame.display.set_mode((1000,1000))
level = levelgen.Level([100,100])

# Create rooms
level.generateRooms(4)
level.writeToGrid()

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
            print("Pressed KEYDOWN")
            pass
        else:
            pass
        clk.tick(60) # update x times per second
        # update and display game world
        level.updateLevel(screen)
        pygame.display.flip()

