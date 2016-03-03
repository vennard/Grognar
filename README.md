# Grognar

Goal: Creating a simple rogue/nethack like 2D dungeon rpg

Basic Development Plan:
1. Level Creation
2. Movement / Collision Detection
3. Goal / Level Save / Item Mechanics

Level Generation Structure (Rough Outline):
1. Creation of basic block sprite structure
    a. block can be: floor, wall, hallway (to start)
    b. collision detection on/off (wall vs. floor)
    c. instantiates pygames sprite class
    d. use default size (10x10?) with 8-bit graphics

2. Generate Rooms 
    a. Use collection (list?) of block sprites
    b. Utilize random (intelligent) placement of rooms (with random sizes)
    c. utilize semi-random floor graphics choices
    d. add walls and doorways after all rooms are placed (controlled-random)

