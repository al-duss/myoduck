import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((500,500))
pygame.display.set_caption('DUCKY BATTLE')

WHITE = (255,255,255)
BLUE=(0,0,128)
GREEN=(0,128,0)
RED=(255,0,0)
BROWN=(139,69,19)
YELLOW=(255,255,0)
LIGHTBLUE=(240,248,255)
SILVER=(230,230,250)

fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj = fontObj.render('DUCKIES WILL BATTLE!', True, GREEN, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200,150)

while True:
	DISPLAYSURF.fill(WHITE)
	DISPLAYSURF.blit(textSurfaceObj, textRectObj)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		pygame.display.update()