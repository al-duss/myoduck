import pygame
from pygame.locals import *
import sys
import time
import random

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
ship = pygame.image.load("assets/square2.png")
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

def print_ship(x,y):
	screen.blit(ship, (x,y))

def game_loop():
	x=display_width/2
	y=display_height-40
	ennemyx=10
	ennemyy=20
	dist = 0
	direction = 1
	dist_ship = 0

	running = True;
	while running:
		#Ship
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					dist_ship = -5
				elif event.key == pygame.K_RIGHT:
					dist_ship = 5
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					dist_ship = 0
		x += dist_ship	

		#Ennemies	
		if direction==1: 
			dist = 5
			ennemyx += direction*dist
	  		if ennemyx >= display_width-ennemy_width:
	  		  direction = -1

		if direction == -1:
			dist = 5
			ennemyx += direction*dist
	  		if ennemyx <= 0:
	  		  direction = 1

		screen.fill(background_colour)
		print_ennemy(ennemyx, ennemyy)
		print_ship(x,y)
		pygame.display.update()
		clock.tick(60)	
		
game_loop()
pygame.quit()
quit()
		