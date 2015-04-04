import pygame
from pygame.locals import *
import sys
import time
import random

pygame.init()
background_colour = (255,255,255)
display_width = 800
display_height = 600


screen = pygame.display.set_mode((display_width, display_width))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)
clock = pygame.time.Clock()

ennemy = pygame.image.load("assets/square.png")
ship = pygame.image.load("assets/square.png")
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

class EnnemyShip:
	number_of_ships=0
	ennemy_width = 35
	y=20

	def __init__(self):
		self.direction=1
		self.x=10+EnnemyShip.ennemy_width*EnnemyShip.number_of_ships
		EnnemyShip.number_of_ships+=1
		self.number=EnnemyShip.number_of_ships
		if EnnemyShip.number_of_ships>=1:
			self.x+=5*EnnemyShip.number_of_ships
	def move(self,dist):
		if self.direction==1: 
			dist = 5
			self.x += self.direction*dist
	  		if self.x >= display_width-50 and self.number==EnnemyShip.number_of_ships:
	  			self.direction = -1
	  		elif self.x >= display_width-50-(EnnemyShip.ennemy_width+5)*(EnnemyShip.number_of_ships-self.number):
	  			self.direction = -1

		if self.direction == -1:
			dist = 5
			self.x += self.direction*dist
	  		if self.x <= (EnnemyShip.ennemy_width+5)*self.number:
	  		  self.direction = 1

def print_ennemy(x,y):
	screen.blit(ennemy, (x,y))

def print_ship(x,y):
	screen.blit(ship, (x,y))
def game_loop():
	x=display_width/2
	y=display_height-40
	dist = 0
	direction = 1
	dist_ship = 0

	running = True;
	one= EnnemyShip()
	two=EnnemyShip()
	three=EnnemyShip()
	four=EnnemyShip()

	Ennemies=[one,two,three,four]
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

		

		screen.fill(background_colour)
		for z in Ennemies:
			z.move(dist)
			print str(z.number)+": "+str(z.x)
			print_ennemy(z.x,EnnemyShip.y)
		
		print_ship(x,y)
		pygame.display.update()
		clock.tick(60)	
		
game_loop()
pygame.quit()
quit()
		