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
pygame.display.set_caption('Ducky Strikes Back')
screen.fill(background_colour)
clock = pygame.time.Clock()

ennemy = pygame.image.load("assets/fox.png")
ennemy = pygame.transform.scale(ennemy, (64, 64))
player = pygame.image.load("assets/duck.png")
player = pygame.transform.scale(player, (64, 64))
iplayer = pygame.image.load("assets/invincible_duck.png")
iplayer = pygame.transform.scale(iplayer,(64,64))
p_shot = pygame.image.load("assets/bubbles.png")
p_shot = pygame.transform.scale(p_shot,(70,70))
e_shot = pygame.image.load("assets/fireball.png")
e_shot = pygame.transform.scale(e_shot,(55,90))
background = pygame.image.load("assets/bg.png")
background = pygame.transform.scale(background, (display_width, display_height))
duck_vader = pygame.image.load("assets/vader.png")
duck_vader = pygame.transform.scale(duck_vader, (300,300))
log = pygame.image.load("assets/log.png")
log = pygame.transform.scale(log, (250,50))
life = pygame.image.load("assets/life.png")
life = pygame.transform.scale(life, (35,45))

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
def continue_next_level(user_lives):
	font = pygame.font.Font(None, 36)		
	text = font.render("Congratulations! Shoot to continue to next level!", 1, (10, 10, 10))																												
	print_background()
	screen.blit(text, (60,display_height/2))
	if user_lives == 3:
		print_life(125,display_height-50)
	if user_lives >= 2:
		print_life(75,display_height-50)
	if user_lives >= 1:
		print_life(25,display_height-50)
	display_level(GAME.level)
	print_player(display_width/2,display_height-70)
	pygame.display.update()
	over = True
	while over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:	
				over = False
def youWin():
	screen.fill(background_colour)
	font = pygame.font.Font(None, 36)		
	text = font.render("You Win! You destroyed the Fox Death Star!", 1, (10, 10, 10))
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

def invicibility(time):
	if time <= 0.4:
		return True
	else:
		return False

class State:
	def __init__(self):
		self.level=1
		self.speed=1
		self.bulletPercentage=40
		self.log_health=3
		self.invicible = False
		self.startTime = 0
GAME=State()
class EnnemyShip:
	number_of_ships=[0,0,0]
	ennemy_width = 64
	number_of_rows = 0


	def __init__(self):
		self.row=EnnemyShip.number_of_rows
		self.direction=1
		self.y=20+EnnemyShip.ennemy_width*EnnemyShip.number_of_rows
		self.x=10+EnnemyShip.ennemy_width*EnnemyShip.number_of_ships[EnnemyShip.number_of_rows]
		EnnemyShip.number_of_ships[EnnemyShip.number_of_rows]+=1
		self.number=EnnemyShip.number_of_ships[EnnemyShip.number_of_rows]
		if EnnemyShip.number_of_ships[EnnemyShip.number_of_rows]>=1:
			self.x+=5*EnnemyShip.number_of_ships[EnnemyShip.number_of_rows]
		if EnnemyShip.number_of_rows>1:
			self.y+=5*EnnemyShip.number_of_rows
	def move(self,dist):
		if self.direction==1: 
			self.x += self.direction*dist*GAME.speed
	  		if self.x >= display_width-64 and self.number==EnnemyShip.number_of_ships[self.row]:
	  			self.direction = -1
	  		elif self.x >= display_width-64-(EnnemyShip.ennemy_width+5)*(EnnemyShip.number_of_ships[self.row]-self.number):
	  			self.direction = -1

		if self.direction == -1:
			self.x += self.direction*dist*GAME.speed
			if self.x <= 0 and self.number==1:
	  			self.direction = 1
	  		elif self.x <= 0+(EnnemyShip.ennemy_width+5)*(self.number-1):
	  			self.direction = 1
			'''self.x += self.direction*dist*GAME.level
	  		if self.x <= (EnnemyShip.ennemy_width+5)*self.number-64:
	  		  self.direction = 1'''
	def move_y(self):
		self.y+=50
class Bullet:

	def __init__(self,x,y):
		self.x=x
		self.y=y

def print_ennemy(x,y):
	screen.blit(ennemy, (x,y))

def print_player(x,y):
	screen.blit(player, (x,y))

def print_iplayer(x,y):
	screen.blit(iplayer, (x,y))

def print_shot(x,y):
	screen.blit(p_shot, (x,y))

def print_e_shot(x,y):
	screen.blit(e_shot, (x,y))

def print_vader(x,y):
	screen.blit(duck_vader,(x,y))

def print_log(x,y):
	screen.blit(log,(x,y))

def print_life(x,y):
	screen.blit(life,(x,y))

def print_background():
	screen.blit(background, (0,0))

def collision(rx, ry, x, y,r_width, ennemy_width):
	if (rx < x + ennemy_width and rx > x) or (rx+r_width<x+ennemy_width and rx+r_width>x) or (rx+r_width/2<x+ennemy_width and rx+r_width/2>x):
		if (ry < y + ennemy_width and ry > y) or (ry+r_width<y+ennemy_width and ry+r_width>y) or (ry+r_width/2<y+ennemy_width and ry+r_width/2>y):
			return True

def rect_collision(rx, ry, x, y,r_width, ennemy_width):
	if (rx < x + ennemy_width and rx > x) or (rx+r_width<x+ennemy_width and rx+r_width>x) or (rx+r_width/2<x+ennemy_width and rx+r_width/2>x):
		if ry == y:
			return True

def display_level(level):
	font = pygame.font.Font(None, 24)		
	text = font.render("Level: " + str(level), 1, (10, 10, 10))
	screen.blit(text, (display_width-80,18))

def game_loop():
	x=display_width/2
	y=display_height-70
	dist = 5
	direction = 1
	dist_ship = 0


	running = True;
	one= EnnemyShip()
	two=EnnemyShip()
	EnnemyShip.number_of_rows+=1
	three=EnnemyShip()
	four=EnnemyShip()

	Ennemies=[one,two,three,four]
	bulletsEnnemy=[]
	bulletsUser=[]
	shot_counter =0
	running = True
	shot = False
	dis = 5
	user_lives=3
	ennemy_y_counter=0

	logx = display_width/8
	logy = display_height-250
	log_hit = 0

	logx1 = 3 * display_width/5
	logy1 = display_height-250
	log_hit1 = 0

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

		#time since last hit
		endTime=time.time()

		
		#log
		if log_hit < GAME.log_health:
			print_log(logx,logy)
		else:
			logx=display_width
			logy=display_height
		
		if log_hit1 < GAME.log_health:
			print_log(logx1,logy1)
		else:
			logx1=display_width
			logy1=display_height

		for z in Ennemies:
			ennemy_y_counter+=1
			z.move(dist)
			print_ennemy(z.x,z.y)
			if collision(z.x,z.y,x,y,EnnemyShip.ennemy_width,EnnemyShip.ennemy_width):
				screen.fill(background_colour)
				gameOver()
				running=False
		if ennemy_y_counter%2100==0:
			for z in Ennemies:
				z.move_y()

		if random.randint(0,GAME.bulletPercentage)==6:
			index=random.randint(0,len(Ennemies)-1)
			bulletsEnnemy.append(Bullet(Ennemies[index].x,Ennemies[index].y))

		for bullets in bulletsEnnemy:
			bullets.y+=dis
			if collision(bullets.x, bullets.y, x, y,fireball_width, EnnemyShip.ennemy_width):
				bulletsEnnemy.remove(bullets)
				endTime=time.time()
				if not invicibility(endTime-GAME.startTime):
					user_lives-=1
					GAME.startTime = time.time()
				if endTime-GAME.startTime >= 0.4:
					GAME.startTime = endTime
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
			if rect_collision(bullets.x, bullets.y, logx, logy, bubbles_width, 250):
				log_hit += 1
				try:
					bulletsUser.remove(bullets)
				except Exception:
					print "ExceptionI"
			if rect_collision(bullets.x, bullets.y, logx1, logy1, bubbles_width, 250):
				log_hit1 += 1
				try:
					bulletsUser.remove(bullets)
				except Exception:
					print "ExceptionI"

		if user_lives == 3:
			print_life(125,display_height-50)
		if user_lives >= 2:
			print_life(75,display_height-50)
		if user_lives >= 1:
			print_life(25,display_height-50)


		display_level(GAME.level)

		if len(Ennemies)<1:
			bulletsEnnemy=[]
			bulletsUser=[]
			GAME.level+=1
			logx = display_width/8
			logy = display_height-250
			log_hit = 0

			logx1 = 3 * display_width/5
			logy1 = display_height-250
			log_hit1 = 0
			EnnemyShip.number_of_ships=[0,0,0]
			EnnemyShip.number_of_rows=0
			one=EnnemyShip()
			two=EnnemyShip()
			three=EnnemyShip()
			four=EnnemyShip()
			Ennemies=[one,two,three,four]

			if GAME.level>=5:
				EnnemyShip.number_of_rows+=1
				Ennemies.append(EnnemyShip())
				Ennemies.append(EnnemyShip())
			if GAME.level>=8:
				Ennemies.append(EnnemyShip())
				Ennemies.append(EnnemyShip())
			if GAME.level>=11:
				EnnemyShip.number_of_rows+=1
				Ennemies.append(EnnemyShip())
				Ennemies.append(EnnemyShip())
			if GAME.level>=14:
				Ennemies.append(EnnemyShip())
				Ennemies.append(EnnemyShip())
			if GAME.level>15:
				screen.fill(background_colour)
				youWin()
				running=False
			if(GAME.level%3==0 and GAME.bulletPercentage>30):
				GAME.bulletPercentage-=2
			elif(GAME.level%3==1 and GAME.log_health<6):
				GAME.log_health+=1
				
			ennemy_y_counter=0
			if GAME.level<15:
				continue_next_level(user_lives)
			x=display_width/2
			y=display_height-70

		if user_lives<1:
			screen.fill(background_colour)
			gameOver()
			running=False

		endTime = time.time()
		if endTime-GAME.startTime >= 0.4:
			print_player(x,y)
		else:
			print_iplayer(x,y)
		pygame.display.update()
		clock.tick(60)	
		
game_loop()
pygame.quit()
quit()
		