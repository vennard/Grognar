# new level generation code (updated from levelcreation.py)
import pygame, random 
import room, block, hall

SHADOW_ON = True

class Level:
    '''
    Grid layout: [x][y]
        visible = active_layer
        hidden = background layer
    '''
    def __init__(self, size):
        # level info
        self.rooms = []
        self.hallways = []

        # Generate grid related data
        self.grid = []
        self.grid_shadow = [] # holds transparent black grid to sit above all other layers
        self.grid_active = []
        self.size = size
        # generate blank grid
        for row in range(size[0]):
            self.grid.append([])
            self.grid_active.append([])
            self.grid_shadow.append([])
            for col in range(size[1]):
                self.grid[row].append(block.Block((row,col)))
                self.grid_active[row].append(block.Block((row,col)))
                surf = pygame.Surface((block.SCALE,block.SCALE))
                surf.set_alpha(255) # set default to full black
                surf.fill((0,0,0)) # set to black
                self.grid_shadow[row].append(surf)

    def updateLayer(self, blk, num):
        # num: 0 - updates active layer, 1 - updates both layers
        if num == 0:
            self.grid_active[blk.pos[0]][blk.pos[1]] = blk
        else:
            self.grid_active[blk.pos[0]][blk.pos[1]] = blk
            self.grid[blk.pos[0]][blk.pos[1]] = blk
        

    def updateLevel(self, screen):
        # update and display each block in level
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.grid_active[x][y].visible == True:
                    # only update and display visible, active layer grid locations 
                    if self.grid_active[x][y].active == True:
                        # if active display background and then active layer block
                        self.grid_active[x][y].update() 
                        screen.blit(self.grid[x][y].image,self.grid[x][y].rect)
                        screen.blit(self.grid_active[x][y].image,self.grid_active[x][y].rect)
                    else:
                        screen.blit(self.grid_active[x][y].image,self.grid_active[x][y].rect)
                    # display shadow last
                    if SHADOW_ON == True:
                        screen.blit(self.grid_shadow[x][y],[x*block.SCALE,y*block.SCALE])
                else:
                    pass

    def moveActive(self, block, newpos):
        # moves active block to newpos and restores old pos
        #   returns block with updated pos, returns block without updated pos on fail
        # check for conflict with edge of map
        if newpos[0] > self.size[0] or newpos[1] > self.size[1]:
            return block
        # check for conflict with .solid property
        if self.grid_active[newpos[0]][newpos[1]].solid == True:
            return block
        oldpos = block.pos
        self.grid_active[oldpos[0]][oldpos[1]] = self.grid[oldpos[0]][oldpos[1]]
        block.moveBlock(newpos)
        self.grid_active[block.pos[0]][block.pos[1]] = block
        return block

    def processShadows(self, pos, light_level):
        # alter grid_shadows given the characters position and light level
        # default 3
        ''' C - character, X - light
        .3210123
        3...X...
        2..XXX..
        1.XXXXX.
        0XXXCXXX
        1.XXXXX.
        2..XXX..
        3...X...

        '''
        # clears discovered areas as you move
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.grid_shadow[x][y].set_alpha(255)
        for x in range(-light_level,light_level+1):
            for y in range(-light_level,light_level+1):
                # check for out of level size
                if pos[0]+x >= self.size[0] or pos[0]+x < 0 or pos[1]+y >= self.size[1] or pos[1]+y < 0:
                    continue
                total = (light_level+1) - (abs(x) + abs(y))
                light_scale = (light_level+1) - (abs(x) + abs(y))
                scale = 220 - (light_scale*120)
                if scale < 0:
                    scale = 0
                elif scale > 255:
                    scale = 255
                if total >= 0:
                    self.grid_shadow[pos[0]+x][pos[1]+y].set_alpha(scale)
                else:
                    self.grid_shadow[pos[0]+x][pos[1]+y].set_alpha(255)

    def generateRooms(self, num):
        self.rooms = room.createRooms(num, self.size)

    def generateHalls(self, num):
        self.hallways = hall.createHalls(self.size, self.rooms, self.grid, num)

    def writeToGrid(self, block_list):
        # write rooms, hallways, etc to grid for display
        # writes to both layers
        for room in block_list:
            for blk in room.blocks:
                self.grid_active[blk.pos[0]][blk.pos[1]] = blk 
                self.grid[blk.pos[0]][blk.pos[1]] = blk 




