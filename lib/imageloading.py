# contains methods and resources for image loading and storage

import os

'''
LEVELS : BASE, TYPE, <THEME>, NAME 
'''

# defines
BASE = 'images/'
EXCLUDE = 'README'
types = [] # will hold all image types (ie floor,wallup,etc) based on folders in images/
themes = [] # store will same directory tree and then (theme, fullpath)
actions = []
images = []

def loadImages():
    # get all types
    ntypes = os.listdir(BASE) 
    types = [ x for x in ntypes if x != EXCLUDE] # exclude README from list
    print str(types)

    # get all themes for each type store in 2d list
    for ty in types:
        theme = [os.listdir(BASE+ty),[BASE + ty + '/' + name for name in os.listdir(BASE + ty)]]
        themes.append(theme)
    print str(themes)

    # get all actions and store in 3d list
    for ty in themes:
        for th in ty[1]: 
            action = os.listdir(th)
            print "found actions" + str(action)
            actions.append([action,[th + '/' + name for name in action]])
            print "found these actions" + str(actions)

    # get all image names
    for ty in actions:
        for th in ty[1]:
            names = os.listdir(th)
            print "found names: " + str(name)
            images.append([th + '/' + name for name in names])
            print "found these names" + str(images)







