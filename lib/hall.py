# hallway generation code
import pygame, random
import imageloading, block

RIGHT = [1,0]
LEFT = [-1,0]
UP = [0,1]
DOWN = [0,-1]
THRESHOLD = 7

def allRoomsHere(rooms, id_list):
    # returns true is id_list contains all rooms
    print "CHECK: ",
    print "does id list: " + str(id_list) + " contain all rooms?",
    found = True
    for rm in rooms:
        id_check = rm.idnum
        found_this = False
        for ids in id_list:
            if id_check == ids:
                found_this = True
        if found_this == False:
            found = False
    print str(found)
    return found



def createHalls(levelsize, rooms, grid, hallnum):
    print "--------- creating hallways ---------"
    # creates all hallways for level, must not end until all rooms are connected
    hallways = []
    hall_count = 0
    created_hallways = False
    while created_hallways == False:
        # choose rooms
        if len(rooms) < 3:
            print "must have more then 2 rooms"
            exit()

        # choose start room
        connected_rooms = True
        for room in rooms:
            if room.connected == False:
                connected_rooms = False
                saved_id = room.idnum
                start_room = room
                break
        if connected_rooms == False:
            print "rooms left unconnected! - would choose: " + str(saved_id)
        else:
            print "no rooms left unconnected"
            start_room = random.choice(rooms)

        dest_room = start_room
        min_val = len(rooms)
        for room in rooms:
            if len(room.connectedTo) < min_val and room is not start_room:
                min_val = len(room.connectedTo)
                dest_room = room

        hall = Hall(start_room, dest_room,grid,rooms)
        start_room.connected = True
        dest_room.connected = True

        print ""
        print "HALL" + str(hall_count) + ": connecting room " + str(start_room.idnum),
        print "[" + str(start_room.connectedTo) + "] to room " + str(dest_room.idnum),
        print "[" + str(dest_room.connectedTo) + "] "
        for ids in dest_room.connectedTo:
            already_contains = False
            for startid in start_room.connectedTo:
                if startid == ids:
                    already_contains = True
            if already_contains == False:
                start_room.connectedTo.append(ids)
        for ids in start_room.connectedTo:
            already_contains = False
            for startid in dest_room.connectedTo:
                if startid == ids:
                    already_contains = True
            if already_contains == False:
                dest_room.connectedTo.append(ids)
        hallways.append(hall)
        hall_count += 1
        print "start room list: [" + str(start_room.connectedTo) + "]"
        print "dest room list: [" + str(dest_room.connectedTo) + "]"
        print "------------------------------"
        print ""

        # end only when hallway count is met AND all rooms are connected
        all_connected = True

        print "checking all rooms:"
        for check in rooms:
            check_id = check.idnum
            print "ROOM" + str(check_id) + ": ", 
            print " (connected? ",
            if check.connected == True:
                print "YES) ",
            else:
                print "NO) ",
            check_list = check.connectedTo
            result = allRoomsHere(rooms, check_list)
            if result == False:
                all_connected = False
        if all_connected == False:
            print "room connection test - FAILED"
        else:
            print "room connection test - PASSED"
        print "------------------------------"

        if hall_count >= hallnum and all_connected == True:
            created_hallways = True
    
    print "done! Created " + str(hall_count) + " hallways!"
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

