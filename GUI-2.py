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
bubbles_width=70
fireball_width=55



screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)
clock = pygame.time.Clock()

ennemy = pygame.image.load("assets/fox.png")
ennemy = pygame.transform.scale(ennemy, (64, 64))
player = pygame.image.load("assets/duck.png")
player = pygame.transform.scale(player, (64, 64))
p_shot = pygame.image.load("assets/bubbles.png")
p_shot = pygame.transform.scale(p_shot,(70,70))
e_shot = pygame.image.load("assets/fireball.png")
e_shot = pygame.transform.scale(e_shot,(55,90))
background = pygame.image.load("assets/bg.png")
background = pygame.transform.scale(background, (display_width, display_height))
duck_vader = pygame.image.load("assets/vader.png")
duck_vader = pygame.transform.scale(duck_vader, (300,300))

def hit():
	# message_display("You've been hit!")
	font = pygame.font.Font(None, 36)		
	text = font.render("Hello There!", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	screen.blit(text, textpos)
def gameOver():
	screen.fill(background_colour)
	font = pygame.font.Font(None, 36)		
	text = font.render("Game Over!", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	screen.blit(text, textpos)
	print_vader(250,100)
	pygame.display.update()
	over = True
	while over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:	
				over = False

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

def game_intro():

	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:	
				intro = False

		screen.fill(background_colour)
		largeText = pygame.font.Font('freesansbold.ttf',80)
		smallText = pygame.font.Font('freesansbold.ttf',45)
		TextSurf, TextRect = text_objects("Ducky Strikes Back", largeText)
		TextSurf1, TextRect1 = text_objects("Press Any Key To Continue...", smallText)
		TextRect.center = ((display_width/2),(display_height/2))
		TextRect1.center = ((display_width/2),(display_height/2 + 150))
		screen.blit(TextSurf, TextRect)
		screen.blit(TextSurf1, TextRect1)
		pygame.display.update()
		clock.tick(15)

class EnnemyShip:
	number_of_ships=0
	ennemy_width = 64
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
class Bullet:

	def __init__(self,x,y):
		self.x=x
		self.y=y

def print_ennemy(x,y):
	screen.blit(ennemy, (x,y))

def print_player(x,y):
	screen.blit(player, (x,y))

def print_shot(x,y):
	screen.blit(p_shot, (x,y))

def print_e_shot(x,y):
	screen.blit(e_shot, (x,y))

def print_vader(x,y):
	screen.blit(duck_vader,(x,y))

def print_background():
	screen.blit(background, (0,0))

def collision(rx, ry, x, y,r_width, ennemy_width):
	if (rx < x + ennemy_width and rx > x) or (rx+r_width<x+ennemy_width and rx+r_width>x) or (rx+r_width/2<x+ennemy_width and rx+r_width/2>x):
		if ry < y + ennemy_width and ry > y:
			return True

def game_loop():
	x=display_width/2
	y=display_height-70
	dist = 0
	direction = 1
	dist_ship = 0


	running = True;
	one= EnnemyShip()
	two=EnnemyShip()
	three=EnnemyShip()
	four=EnnemyShip()

	Ennemies=[one,two,three,four]
	bulletsEnnemy=[]
	bulletsUser=[]
	shot_counter =0
	running = True
	shot = False
	onscreen = False
	dis = 5
	user_lives=3

	game_intro()

	while running:
		#Ship
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			if event.type == KEYDOWN:
				if event.key == pygame.K_LEFT:
					dist_ship = -5
				elif event.key == pygame.K_RIGHT:
					dist_ship = 5
				elif event.key == pygame.K_SPACE:
					if(len(bulletsUser)<3):
						bulletsUser.append(Bullet(x,y))
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					dist_ship = 0

		if (x+dist_ship) >= 0 and (x+dist_ship) <= (display_width - EnnemyShip.ennemy_width) :
			x += dist_ship	

		#Shots from ship
		
		#Shots
		

		

		# screen.fill(background_colour)
		print_background()
		for z in Ennemies:
			z.move(dist)
			print_ennemy(z.x,EnnemyShip.y)

		if random.randint(0,40)==6:
			bulletsEnnemy.append(Bullet(Ennemies[random.randint(0,len(Ennemies)-1)].x,EnnemyShip.y))

		for bullets in bulletsEnnemy:
			bullets.y+=dis
			if collision(bullets.x, bullets.y, x, y,fireball_width, EnnemyShip.ennemy_width):
				hit()
				bulletsEnnemy.remove(bullets)
				user_lives-=1
			if bullets.y <= display_height:
				print_e_shot(bullets.x,bullets.y)
			else:
				bulletsEnnemy.remove(bullets)
		
		for bullets in bulletsUser:
			bullets.y-=dis
			if bullets.y >= 0:
				print_shot(bullets.x,bullets.y)
			else:
				bulletsUser.remove(bullets)
			for bulletsOpp in bulletsEnnemy:
				if collision(bullets.x, bullets.y, bulletsOpp.x, bulletsOpp.y, bubbles_width, fireball_width):
					bulletsEnnemy.remove(bulletsOpp)
					bulletsUser.remove(bullets)
			for ennemies in Ennemies:
				if collision(bullets.x, bullets.y, ennemies.x, ennemies.y,bubbles_width, EnnemyShip.ennemy_width):
					Ennemies.remove(ennemies)


		
		if(len(Ennemies)<1 or user_lives<1):
			screen.fill(background_colour)
			gameOver()
			running=False


		print_player(x,y)
		pygame.display.update()
		clock.tick(60)	
		
game_loop()
pygame.quit()
quit()
		