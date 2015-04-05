import pygame
from pygame.locals import *
import sys
import os
import myo
from myo.lowlevel import pose_t, stream_emg
from myo.six import print_

pygame.init()
background_colour = (255,255,255)
display_width = 800
display_height = 500
black = (0,0,0)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('The Myo Ducks')
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
				if event.key == pygame.K_k:
					os.system("python GUI-2.py")
				if event.key == pygame.K_m:

					os.system("python myoDucks.py")
				if event.key == pygame.K_d:
					os.system("python rockPaperScissors.py")
				if event.key == pygame.K_b:
					os.system("python duckieBattle.py")

		screen.fill(background_colour)
		largeText = pygame.font.Font('freesansbold.ttf',45)
		smallText = pygame.font.Font('freesansbold.ttf',30)
		TextSurf, TextRect = text_objects("The Myo Ducks", largeText)
		TextSurf2, TextRect2 = text_objects("Ducky Strikes Back: Press M for Myo, K for Keyboard", smallText)
		TextSurf3, TextRect3 = text_objects("Duck, Paper Scissors: Press D", smallText)
		TextSurf4, TextRect4 = text_objects("Battle Duckies: Press B", smallText)
		TextRect.center = ((display_width/2),40)
		TextRect2.center = ((display_width/2),(display_height/2 + 100))
		TextRect3.center = ((display_width/2),(display_height/2 + 150))
		TextRect4.center = ((display_width/2),(display_height/2 + 200))
		duck = pygame.image.load("assets/duck.png")
		duck = pygame.transform.scale(duck, (150, 150))
		screen.blit(duck, ((display_width/2-80),150))
		screen.blit(TextSurf, TextRect)
		screen.blit(TextSurf2, TextRect2)
		screen.blit(TextSurf3, TextRect3)
		screen.blit(TextSurf4, TextRect4)
		pygame.display.update()
		clock.tick(15)

game_intro()
pygame.quit()
quit()