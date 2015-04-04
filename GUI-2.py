import pygame
from pygame.locals import *
import sys
import time
import random

pygame.init()
background_colour = (255,255,255)
black = (0,0,0)
display_width = 800
display_height = 500
ennemy_width = 35

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)
clock = pygame.time.Clock()

ennemy = pygame.image.load("assets/square.png")
ship = pygame.image.load("assets/square.png")
e_bullet = pygame.image.load("assets/rsquare.png")

def hit():
	# message_display("You've been hit!")
	font = pygame.font.Font(None, 36)		
	text = font.render("Hello There", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	screen.blit(text, textpos)

def text_objects(text, font):
	textSurface = font.render(text, 1, black)
	return textSurface, textSurface.get_rect()

def message_display(text):
	hitText = pygame.font.Font(None, 115)
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

def print_shot(x,y):
	screen.blit(ship, (x,y))

def print_e_shot(x,y):
	screen.blit(e_bullet, (x,y))

def collision(rx, ry, x, y, ennemy_width):
	if rx < x + ennemy_width and rx > x:
		if ry < y + ennemy_width and ry > y:
			return True

def game_loop():
	x=display_width/2
	y=display_height-40
	ennemyx=10
	ennemyy=20
	dist = 0
	direction = 1
	dist_ship = 0
	shot_counter =0
	running = True
	shot = False
	onscreen = False
	dis = 5
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
				elif event.key == pygame.K_SPACE:
					shot=True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					dist_ship = 0

		if ((x+dist_ship) >= 0 and (x+dist_ship)) <= (display_width - ennemy_width) :
			x += dist_ship	

		#Shots from ship
		if shot:
			if shot_counter ==0:
				shotx = x
				shoty = y
				shot_counter +=1
			else:
				shoty += -5
				if shoty<=0:
					shot = False;
					shot_counter=0

		#Shots
		if random.randint(0,40)==6:
			if not onscreen:
				print "hello"
				rx = ennemyx
				ry = ennemyy
				onscreen = True
		if onscreen:
			ry += dis
			if collision(rx, ry, x, y, ennemy_width):
				hit()
			if ry >= display_height:
				onscreen = False

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
		if shot:
			print "ok"
			print_shot(shotx, shoty)
		if onscreen:
			print_e_shot(rx, ry)
		print_ennemy(ennemyx, ennemyy)
		print_ship(x,y)
		pygame.display.update()
		clock.tick(60)	
		
game_loop()
pygame.quit()
quit()
		