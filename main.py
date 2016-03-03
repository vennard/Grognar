#!/usr/bin/python2

import pygame
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
position = [10,10]
test = levelcreation.Block('images/tile_sample1.png', position)
#testimage = pygame.image.load('images/tile_sample1.png')
screen.blit(test.image, test.rect)
pygame.display.flip()

# TODO testing custom room class instantiation
pos = [100,100]
test1 = levelcreation.Block('images/tile1.png', pos)
size = [1,1]
floor_images = ['images/tile0.png','images/tile1.png','images/tile2.png']
test_room = levelcreation.Room(size,pos,floor_images)
#test_room.addBlock(test)
#test_room.addBlock(test1)
for i in test_room.blocks:
    screen.blit(i.image, i.rect)

#screen.blit(test_room.blocks[*].image, test_room.blocks[*].rect)
#screen.blit(test_room.blocks[0].image, test_room.blocks[0].rect)


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
