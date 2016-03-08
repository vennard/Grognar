# contains methods and resources for image loading and storage

import os, random 

'''
LEVELS : BASE, TYPE, <THEME>, NAME 
'''

# defines
BASE = 'images/'
EXCLUDE = 'README'
ready = False 
types = [] # will hold all image types (ie floor,wallup,etc) based on folders in images/
themes = [] # store will same directory tree and then (theme, fullpath)
actions = []
images = []

# TODO MUST IMPLEMENT THIS:
#   pick random image if no appropriate found
def initialize():
    print "--- loading images filepaths ---"
    # get all types
    ntypes = os.listdir(BASE) 
    types = [ x for x in ntypes if x != EXCLUDE] # exclude README from list

    # get all themes for each type store in 2d list
    for ty in types:
        theme = [os.listdir(BASE+ty),[BASE + ty + '/' + name for name in os.listdir(BASE + ty)]]
        themes.append(theme)

    # get all actions and store in 3d list
    for ty in themes:
        for th in ty[1]: 
            action = os.listdir(th)
            actions.append([action,[th + '/' + name for name in action]])

    # get all image names
    for ty in actions:
        for th in ty[1]:
            names = os.listdir(th)
            images.append([th + '/' + name for name in names])

    print "complete!"
    ready = True


def getTypes():
    return types

def getThemes(block_type):
    # returns array of themes associated with given block_type
    themes_returned = []
    found_valid = False
    for blk in themes:
        for name, paths in zip(blk[0],blk[1]):
            if block_type in paths:
                found_valid = True
                themes_returned.append(name)
    if found_valid == False:
        print "ERROR: tried to get themes for invalid block type"
        return -1
    else:
        return themes_returned

def getActions(block_type, theme_type):
    # returns array of actions associated with given block_type and theme_type
    actions_returned = []
    found_valid = False
    for blk in actions:
        for action, paths in zip(blk[0],blk[1]):
            if (block_type in paths) and (theme_type in paths):
                found_valid = True
                actions_returned.append(action)
    if found_valid == False:
        print "ERROR: tried to get actions for invalid block or theme type"
        return -1
    else:
        return actions_returned


def getRandomStartAction(block_type, block_theme):
    # returns action randomly chosen from all actions with _ marker
    found_valid = False 
    temp = []
    for blk in actions:
        for action, paths in zip(blk[0],blk[1]):
            if (block_type in paths) and (block_theme in paths) and ('_' in paths):
                found_valid = True 
                temp.append(action)
    if found_valid == False:
        print "ERROR: tried to get random start action -- invalid block or theme type"
        return -1
    else:
        return random.choice(temp)

def getActionImages(block_type, block_theme, block_action):
    # retrieves list of images associated with one action for type and theme
    # RETURNS: array with following structure [image_list[], index_of_static[]] TODO implement simple first 
    images_returned = []
    found_valid = False
    for action_list in images:
        for action in action_list:
            # find appropriate action image list
            if (block_type in action) and (block_theme in action) and (block_action in action):
                found_valid = True
                images_returned.append(action)
    if found_valid == False:
        print "ERROR: tried to get action images from type: " + str(block_type) + " theme: " + str(block_theme) + " action: " + str(block_action)
    else:
        return images_returned

def getRandomStartImage(block_type, block_theme, block_action):
    # grabs random start image chosen from all images with _ leading name 
    temp = []
    found_valid = False 
    for action_list in images:
        for action in action_list:
            # find appropriate action image list
            if (block_type in action) and (block_theme in action) and (block_action in action) and ('_' in action):
                found_valid = True
                temp.append(action)
    if found_valid == False:
        print "ERROR: tried to get action images from type: " + str(block_type) + " theme: " + str(block_theme) + " action: " + str(block_action)
        return -1
    else:
        return random.choice(temp)
