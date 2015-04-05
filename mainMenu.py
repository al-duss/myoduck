import pygame
from pygame.locals import *
import sys
import os

pygame.init()
background_colour = (255,255,255)
display_width = 800
display_height = 500
black = (0,0,0)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Ducky Strikes Back')
screen.fill(background_colour)
clock = pygame.time.Clock()

def text_objects(text, font):
	textSurface = font.render(text, 1, black)
	return textSurface, textSurface.get_rect()

def game_intro():

	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					os.system("python GUI-2.py")
				if event.key == pygame.K_m:
					os.system("python myoDucks.py")

		screen.fill(background_colour)
		largeText = pygame.font.Font('freesansbold.ttf',80)
		smallText = pygame.font.Font('freesansbold.ttf',45)
		TextSurf, TextRect = text_objects("Ducky Strikes Back", largeText)
		TextSurf1, TextRect1 = text_objects("M for myo, S for regular", smallText)
		TextRect.center = ((display_width/2),(display_height/2))
		TextRect1.center = ((display_width/2),(display_height/2 + 150))
		screen.blit(TextSurf, TextRect)
		screen.blit(TextSurf1, TextRect1)
		pygame.display.update()
		clock.tick(15)

game_intro()
pygame.quit()
quit()