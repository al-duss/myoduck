import pygame
from pygame.locals import *
import sys
import time

pygame.init()
background_colour = (255,255,255)
display_width = 800
display_height = 600
ennemy_width = 35

screen = pygame.display.set_mode((display_width, display_width))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)
clock = pygame.time.Clock()

ennemy = pygame.image.load("assets/square.png")
def hit():
	message_display("You've been hit!")

def text_objects(text, font):
	textSurface = font.render(text, true, black)
	return textSurface, textSurface.get_rect()

def message_display(text):
	hitText = pygame.font.Font('freesansbold.ttf', 115)
	TextSurf, TextRect = text_objects(text, hitText)
	TextRect.center = ((display_width/2), (display_height/2))
	screen.blit(TextSurface, TextRect)
	pygame.display.update()
	time.sleep(2)
	game_loop()

def print_ennemy(x,y):
	screen.blit(ennemy, (x,y))

def game_loop():
	x=10
	y=20
	dist = 0
	direction = 1

	running = True;
	while running:
#		for event in pygame.event.get():
#			if event.type == QUIT:
#				running = False
#			if event.type == pygame.KEYDOWN:
#				if event.key == pygame.K_LEFT:
#					dist = -5
#				elif event.key == pygame.K_RIGHT:
#					dist = 5
#			if event.type == pygame.KEYUP:
#				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
#					dist = 0

#		x += dist	
#		screen.fill(background_colour)		
#		print_ennemy(x,y)
		
#		pygame.display.update()
#		clock.tick(60)
		if direction==1: 
			dist = 5
			x += direction*dist
			screen.fill(background_colour)
			print_ennemy(x,y)
	  		pygame.display.update()
	  		clock.tick(60)
	  		if x >= display_width-ennemy_width:
	  		  direction = -1

		if direction == -1:
			dist = 5
			x += direction*dist
			screen.fill(background_colour)
			print_ennemy(x,y)
	  		pygame.display.update()
	  		clock.tick(60)
	  		if x <= 0:
	  		  direction = 1

game_loop()
pygame.quit()
quit()
		