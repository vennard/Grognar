# Grognar

Goal: Creating a simple rogue/nethack like 2D dungeon rpg

Resources:
1. Vim Quick Reference Card: http://users.ece.utexas.edu/~adnan/vimqrc.html
    a.Some of my favorite commands are the split screening using :sp or :vs to open another file with a vertical or horizontal split then you can move between with ctrl+ww
    
2. Quick and Dirty guide to using git
    a.Always use git pull when starting to work to make sure you pull in the latest work
    b.git clone <link to repo> : redownload repo to current directory, useful if you break everything
    c.git status 
        ---git diff--- and use q to exit
    d.git commit -a -m "add a relevant message of what you're adding here" : this is how you save your work to the local machine
    e.git push : this is how you push your locally saved commits out to the github 'cloud'

Quick reference for commands:
git pull
git clone <http link>
git status
git diff
git commit -a -m "my message"
git push

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

