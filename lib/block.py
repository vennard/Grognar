import pygame 
import imageloading

class Block(pygame.sprite.Sprite):
    '''base building block'''
    def __init__(self, pos):
        super(Block,self).__init__()
        # set defaults
        self.visible = True
        self.images = [] # holds images for animation
        self.rate = 10 # division factor for animation speed from 60fps total game speed
        self.rate_count = 0
        self.index = 0
        
        # initialize blank (black) square image
        temp = pygame.image.load('images/test/type0/_initial/6.png').convert() # black square
        self.black = pygame.transform.scale(temp,(10,10))
        self.image = self.black
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos[0]*10,pos[1]*10] # actual position
        self.pos = pos # grid position

    def setBlack(self):
        self.image = self.black

    def setImage(self, block_type, block_theme):
        # set static image using type and theme
        path = imageloading.getRandomStartImage(block_type, block_theme, 'initial')
        temp = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(temp,(10,10))

    def setActionImages(self, block_type, block_theme, block_action):
        # set images using type, theme, and action
        start_action = imageloading.getRandomStartAction(block_type, block_theme)
        start_path, paths = imageloading.getActionImages(block_type, block_theme, start_action)
        self.image = pygame.transform.scale(pygame.image.load(start_path).convert(),(10,10))
        for path in paths:
            temp = pygame.image.load(path).convert()
            self.images.append(pygame.transform.scale(temp,(10,10)))

    def changeImage(self, new_image):
        temp = pygame.image.load(new_image).convert()
        self.image = pygame.transform.scale(temp,(10,10))

    def loadImages(self, load_images):
        for image in load_images:
            temp = pygame.image.load(image).convert()
            self.images.append(pygame.transform.scale(temp,(10,10)))

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

