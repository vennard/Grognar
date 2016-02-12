#!/usr/bin/python3.5

import pygame
from pygame.locals import *

def debugtext(screen, textout):
  # JLV debug text output
  font=pygame.font.Font(None,30)
  text=font.render("DEBUG:"+str(textout),1,(255,255,0))
  screen.blit(text, (100,100))

def create_test_shape(size = (32,32), color = (255,255,255)):
  surface = pygame.Surface(size)
  surface.fill(color)
  surface = surface.convert()
  return surface

MOVEMENTS = {pygame.K_LEFT : (-1,0),
                        pygame.K_RIGHT : (1,0),
                        pygame.K_UP : (0,-1),
                        pygame.K_DOWN : (0,1),
                        }

class Main_Character(pygame.sprite.Sprite):
    '''The main character of the game.
     
    Attributes
        pos     -- position on the screen
        image   -- surface object representing the player
        rect    -- rectangle of the the main character
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = [0,0]
        self.image = create_test_shape()
        self.rect = self.image.get_rect()
        self.size = self.rect.size
         
    def update(self):
        self.rect.topleft = self.pos
         
    def move_char(self,keys_pressed, rect):
        '''For each key that is currently pressed down, move
        the rectangle of the player in the right direction
        '''
        pixels = 2
         
        for key in keys_pressed.list:
            self.pos[0] = self.pos[0] + MOVEMENTS[key][0] * pixels        
            self.pos[1] = self.pos[1] + MOVEMENTS[key][1] * pixels
        self.rect.move(self.pos)
        self.update()

def main():
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	pygame.display.set_caption('Basic Pygame program')

	# Fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	# Display some text
	font = pygame.font.Font(None, 36)
	text = font.render("Hello There", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)

	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()

	# Custom test intantiations
	character = Main_Character()
	allsprites = pygame.sprite.RenderPlain((character))

	screen.blit(background, (0, 0))

	# Event loop
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
			   return
			elif event.type == KEYDOWN:
			   if event.key == pygame.K_LEFT:
				   debugtext(screen, "dick")
			else:
			   pass

		#allsprites.update()
		#allsprites.draw(screen)
		#debugtext(screen, "blabla")
		pygame.display.flip()


if __name__ == '__main__': main()


