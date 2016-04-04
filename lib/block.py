import pygame 
import imageloading

SCALE = 20

class Block(pygame.sprite.Sprite):
    '''base building block'''
    def __init__(self, pos):
        super(Block,self).__init__()
        # set defaults
        self.visible = True
        self.solid = True # collision detection variable
        self.active = False # tells animation whether or not to display background first
        self.side = None # for wall type: RIGHT, LEFT, UP, DOWN
        self.block_type = None # see imageloading for details
        self.images = [] # holds images for animation
        self.rate = 10 # division factor for animation speed from 60fps total game speed
        self.rate_count = 0
        self.index = 0
        
        # initialize blank (black) square image
        temp = pygame.image.load('images/test/type0/_initial/6.png').convert().convert_alpha() # black square
        self.black = pygame.transform.scale(temp,(SCALE,SCALE))
        self.image = self.black
        self.image.set_alpha(8)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos[0]*SCALE,pos[1]*SCALE] # actual position
        self.pos = pos # grid position

    def setAlpha(self, newval):
        self.image.set_alpha(newval)

    def moveBlock(self, pos):
        self.rect.topleft = [pos[0]*SCALE,pos[1]*SCALE] # set actual position
        self.pos = pos

    def setBlack(self):
        self.image = self.black
        self.block_type = None

    def setRed(self):
        self.image = pygame.transform.scale(pygame.image.load('images/test/type0/_initial/1.png').convert(),(SCALE,SCALE))

    def setImage(self, block_type, block_theme):
        # set static image using type and theme
        self.block_type = block_type
        path = imageloading.getRandomStartImage(block_type, block_theme, 'initial')
        temp = pygame.image.load(path).convert().convert_alpha()
        self.image = pygame.transform.scale(temp,(SCALE,SCALE))

    def setActionImages(self, block_type, block_theme, block_action):
        # set images using type, theme, and action
        self.block_type = block_type
        start_action = imageloading.getRandomStartAction(block_type, block_theme)
        start_path, paths = imageloading.getActionImages(block_type, block_theme, start_action)
        self.image = pygame.transform.scale(pygame.image.load(start_path).convert().convert_alpha(),(SCALE,SCALE))
        for path in paths:
            temp = pygame.image.load(path).convert().convert_alpha()
            self.images.append(pygame.transform.scale(temp,(SCALE,SCALE)))

    def changeImage(self, new_image):
        temp = pygame.image.load(new_image).convert().convert_alpha()
        self.image = pygame.transform.scale(temp,(SCALE,SCALE))

    def loadImages(self, load_images):
        for image in load_images:
            temp = pygame.image.load(image).convert().convert_alpha()
            temp.set_alpha(0)
            self.images.append(pygame.transform.scale(temp,(SCALE,SCALE)))

    def update(self):
        # update animation image
        total = len(self.images)
        if total > 0:
            # check to see if rate has triggered
            self.rate_count += 1
            if self.rate_count >= self.rate:
                # reset rate count and update image
                self.rate_count = 0
                if self.index >= (len(self.images)-1):
                    self.index = 0
                else:
                    self.index += 1
                self.image = self.images[self.index]

