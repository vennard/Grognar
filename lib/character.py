# Contains methods and resources for character generation and control
import pygame

class Character(pygame.sprite.Sprite):
    ''' Player controlled character for the game
        Attributes
            image -- surface representing player
            ...
    '''
    image = None

    def __init__(self):
        super(self).__init__()

        self.image = pygame.image.load(image).convert() # Why convert?

    def update(self):
        self.rect.topleft = self.pos

    def move_char(self, key_press):
        self.update()
