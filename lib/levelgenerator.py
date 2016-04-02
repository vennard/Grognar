# new level generation code (updated from levelcreation.py)
import pygame, random 
import room, block 

class Level:
    def __init__(self, size):
        # level info
        self.rooms = []

        # Generate grid related data
        self.grid = []
        self.size = size
        # generate blank grid
        for row in range(size[0]):
            self.grid.append([])
            for col in range(size[1]):
                self.grid[row].append(block.Block((row,col)))

    def updateLevel(self, screen):
        # update and display each block in level
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.grid[x][y].visible == True:
                    self.grid[x][y].update()
                    screen.blit(self.grid[x][y].image,self.grid[x][y].rect)
                else:
                    pass

    def generateRooms(self, num):
        self.rooms = room.createRooms(num, self.size)

    def writeToGrid(self):
        # write rooms, hallways, etc to grid for display
        for room in self.rooms:
            for blk in room.blocks:
                self.grid[blk.pos[0]][blk.pos[1]] = blk 






