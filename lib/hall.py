# hallway generation code
import pygame, random
import imageloading, block

RIGHT = [1,0]
LEFT = [-1,0]
UP = [0,1]
DOWN = [0,-1]
THRESHOLD = 7

def createHalls(levelsize, rooms, grid, hallnum):
    # creates all hallways for level, must not end until all rooms are connected
    hallways = []
    retval = True
    hall_count = 0
    created_hallways = False
    for r in rooms:
        r.connected = False
    while created_hallways == False:
        # choose rooms
        if len(rooms) < 3:
            print "must have more then 2 rooms"
            exit()

        # choose start room
        start_room_chosen = False
        for room in rooms:
            if room.connected == False:
                # found unconnected room aka the best option
                start_room = room
                #room.connected = True
                start_room_chosen = True
                break
        if start_room_chosen == False:

            rnd_room = random.choice(rooms)

        # choose destination room
        dest_room_chosen = False
        while dest_room_chosen == False:
            for room in rooms:
                if room.connected != False:
                    continue
                else:
                    dest_room = room
                    dest_room_chosen = True
                    room.connected = True
            if dest_room_chosen == False:
                rnd_room = random.choice(rooms)
                if rnd_room is start_room:
                    continue
                else:
                    dest_room = rnd_room
                    room.connected = True
                    dest_room_chosen = True
        hall = Hall(start_room, dest_room,grid,rooms)
        hallways.append(hall)
        hall_count += 1
        if hall_count >= hallnum:
            created_hallways = True

        # final check
        for rm in rooms:
            if rm.connected == False: 
                print "this room is unconnected: " + str(rm)

    return hallways

class Hall:
    # hall has one mission on creation, to connect start_room to dest_room 
    def __init__(self, start_room, dest_room, grid, rooms):
        self.blocks = []
        self.theme = random.choice(imageloading.getThemes('hall'))

        # temp variables
        rooms_connected = False
        startxy = start_room.topleft
        destxy = dest_room.topleft
        max_hall = 8
        min_hall = 2

        # choose closest start location
        minval = 1000
        for blk in start_room.blocks:
            if blk.block_type == 'wall':
                diffxy = [cur - des for cur, des in zip(blk.pos,destxy)]
                val = abs(diffxy[0]) + abs(diffxy[1])  
                if val < minval:
                    minval = val
                    startxy = blk.pos
                    start_direction = blk.side 


        # choose closest dest location
        minval = 1000
        for blk in dest_room.blocks:
            if blk.block_type == 'wall':
                diffxy = [cur - des for cur, des in zip(blk.pos,startxy)]
                val = abs(diffxy[0]) + abs(diffxy[1])  
                if val < minval:
                    minval = val
                    destxy = blk.pos
        

        # create hallway sections until startxy is connected to destxy
        currxy = startxy
        firstRun = True
        direction = [0,0]
        threshold_level = 0
        while rooms_connected == False:
            diffxy = [cur - des for cur, des in zip(currxy,destxy)]
            if firstRun == True:
                direction = start_direction
                firstRun = False
            else:
                xory = random.randint(0,1) # pick x or y
                if xory == 0: # x chosen
                    if diffxy[0] < 0: # -delta means we need +x direction
                        direction = RIGHT
                    else:
                        direction = LEFT
                else: # y chosen
                    if diffxy[1] < 0: # -detal means we need +y direction
                        direction = UP
                    else:
                        direction = DOWN
            # check threshold then throttle hallway length
            val = abs(diffxy[0]) + abs(diffxy[1])  
            if val < THRESHOLD:
                threshold_level += 1
                max_hall = max_hall - threshold_level
                min_hall = min_hall - threshold_level
                if max_hall < 3:
                    max_hall = 3
                if min_hall < 2:
                    min_hall = 2

            section_length = random.randint(min_hall,max_hall)
            # create hallway section and update variables
            for i in range(section_length):
                newxy = [currxy[0] + (direction[0]*i),currxy[1] + (direction[1]*i)]
                # check for edge collision
                if newxy[0] >= len(grid) or newxy[1] >= len(grid[0]):
                    newxy = currxy
                    break
                # check for collision with destination
                if dest_room.contains(newxy) == True:
                    rooms_connected = True

                newblock = block.Block(newxy)
                newblock.solid = False
                newblock.setImage('hall',self.theme)
                self.blocks.append(newblock)
            currxy = newxy

        # cleanup overlapping hall 
        blocks_new = []
        for hallblk in self.blocks:
            grid_block = grid[hallblk.pos[0]][hallblk.pos[1]]
            if grid_block.block_type != None:
                # place door TODO consider limiting placements
                if grid_block.block_type == 'wall':
                    hallblk.setImage('door',random.choice(imageloading.getThemes('door')))
                    blocks_new.append(hallblk)
            else:
                blocks_new.append(hallblk)
        self.blocks = blocks_new

