import myo
from myo.lowlevel import pose_t, stream_emg
from myo.six import print_
import random
import pygame
from pygame.locals import *
import sys
import time
import random

pygame.init()
myo.init()


background_colour = (255,255,255)
black = (0,0,0)
display_width = 800
display_height = 500
bubbles_width=70
fireball_width=55
fire=False


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

def gameOver():
	GAME.over=True
	screen.fill(background_colour)
	font = pygame.font.Font(None, 36)		
	text = font.render("Game Over!", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	screen.blit(text, textpos)
	print_vader(250,100)
	pygame.display.update()
	while GAME.over:
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

	
	while GAME.intro:
		print "hit"
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:	
				GAME.intro = False

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
class State:
	def __init__(self):
		self.bulletsUser=[]
		self.dist_ship=0
		self.x=display_width/2
		self.y=display_height-70
		self.myo=0
		self.over=True
GAME=State()

class EnnemyShip:
	number_of_ships=0
	ennemy_width = 64
	number_of_rows = 1

	def __init__(self):
		self.direction=1
		self.y=20+EnnemyShip.ennemy_width*(EnnemyShip.number_of_rows-1)
		self.x=10+EnnemyShip.ennemy_width*EnnemyShip.number_of_ships
		EnnemyShip.number_of_ships+=1
		self.number=EnnemyShip.number_of_ships
		if EnnemyShip.number_of_ships>=1:
			self.x+=5*EnnemyShip.number_of_ships
		if EnnemyShip.number_of_rows>1:
			self.y+=5*EnnemyShip.number_of_rows
	def move(self,dist):
		if self.direction==1: 
			dist = 5
			self.x += self.direction*dist
	  		if self.x >= display_width-64 and self.number==EnnemyShip.number_of_ships:
	  			self.direction = -1
	  		elif self.x >= display_width-64-(EnnemyShip.ennemy_width+5)*(EnnemyShip.number_of_ships-self.number):
	  			self.direction = -1

		if self.direction == -1:
			dist = 5
			self.x += self.direction*dist
	  		if self.x <= (EnnemyShip.ennemy_width+5)*self.number-64:
	  		  self.direction = 1
class Bullet:

	def __init__(self,x,y):
		self.x=x
		self.y=y
class Listener(myo.DeviceListener):
    # return False from any method to stop the Hub

    def on_connect(self, myo, timestamp):
        print_("Connected to Myo")
        myo.vibrate('short')
        myo.request_rssi()
        GAME.myo=myo

    def on_rssi(self, myo, timestamp, rssi):
        #print_("RSSI:", rssi)
        print_('');

    def on_event(self, event):
        r""" Called before any of the event callbacks. """

    def on_event_finished(self, event):
        r""" Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub. """

    def on_pair(self, myo, timestamp):
        print_('Paired')
        print_("If you don't see any responses to your movements, try re-running the program or making sure the Myo works with Myo Connect (from Thalmic Labs).")
        print_("Double tap enables EMG.")
        print_("Spreading fingers disables EMG.\n")

    def on_disconnect(self, myo, timestamp):
        print_('on_disconnect')

    def on_pose(self, myo, timestamp, pose):
        if pose == pose_t.fist:
        	if GAME.over:
        		GAME.over=False
        	else:
        		fire()
               
    def on_orientation_data(self, myo, timestamp, orientation):
        show_output('orientation', orientation)

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        show_output('acceleration', acceleration)

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
    	if gyroscope[0]>15:
    		move_left()
    	if gyroscope[0]<-15:
    		move_right()
        show_output('gyroscope', gyroscope)

    def on_unlock(self, myo, timestamp):
        print_('unlocked')

    def on_lock(self, myo, timestamp):
        print_('locked')

    def on_sync(self, myo, timestamp, arm, x_direction):
        print_('synced', arm, x_direction)

    def on_unsync(self, myo, timestamp):
        print_('unsynced')
        
    def on_emg(self, myo, timestamp, emg):
        show_output('emg', emg)

def show_output(message, data):
    '''if random.random() < 0.1: 
        print_(message + ':' + str(data))'''
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
	if ((rx <= x + ennemy_width) and (rx >= x)) or ((rx+r_width<=x+ennemy_width) and (rx+r_width >= x)) or ((rx+r_width/2<=x+ennemy_width) and (rx+r_width/2>=x)):
		if ry <= y + ennemy_width and ry >= y:
			return True
def fire():
	if(len(GAME.bulletsUser)<3):
		GAME.bulletsUser.append(Bullet(GAME.x,GAME.y))
def move_left():
	GAME.dist_ship = -5
def move_right():
	GAME.dist_ship = 5
hub = myo.Hub()
hub.set_locking_policy(myo.locking_policy.none)
hub.run(500, Listener())

def game_loop():
	
	dist = 0
	direction = 1


	running = True;
	one= EnnemyShip()
	two=EnnemyShip()
	three=EnnemyShip()
	four=EnnemyShip()

	Ennemies=[one,two,three,four]
	bulletsEnnemy=[]
	shot_counter =0
	running = True
	shot = False
	onscreen = False
	dis = 5
	user_lives=3
	#game_intro()
	
	while running:
		#Ship
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
		if (GAME.x+GAME.dist_ship) >= 0 and (GAME.x+GAME.dist_ship) <= (display_width - EnnemyShip.ennemy_width) :
			GAME.x += GAME.dist_ship	

		#Shots from ship
		
		#Shots
		

		

		# screen.fill(background_colour)
		print_background()
		for z in Ennemies:
			z.move(dist)
			print_ennemy(z.x,z.y)

		if random.randint(0,40)==6:
			index=random.randint(0,len(Ennemies)-1)
			bulletsEnnemy.append(Bullet(Ennemies[index].x,Ennemies[index].y))

		for bullets in bulletsEnnemy:
			bullets.y+=dis
			if collision(bullets.x, bullets.y, GAME.x, GAME.y,fireball_width, EnnemyShip.ennemy_width):
				bulletsEnnemy.remove(bullets)
				GAME.myo.vibrate('long')

				user_lives-=1
			if bullets.y <= display_height:
				print_e_shot(bullets.x,bullets.y)
			else:
				bulletsEnnemy.remove(bullets)
		
		for bullets in GAME.bulletsUser:
			bullets.y-=dis
			if bullets.y >= 0:
				print_shot(bullets.x,bullets.y)
			else:
				GAME.bulletsUser.remove(bullets)
			for bulletsOpp in bulletsEnnemy:
				if collision(bullets.x, bullets.y, bulletsOpp.x, bulletsOpp.y, bubbles_width, fireball_width):
					bulletsEnnemy.remove(bulletsOpp)
					GAME.bulletsUser.remove(bullets)
			for ennemies in Ennemies:
				if collision(bullets.x, bullets.y, ennemies.x, ennemies.y,bubbles_width, EnnemyShip.ennemy_width):
					Ennemies.remove(ennemies)


		
		if(len(Ennemies)<1 or user_lives<1):
			screen.fill(background_colour)
			gameOver()
			running=False


		print_player(GAME.x,GAME.y)
		pygame.display.update()
		clock.tick(60)	
		
game_loop()

hub.stop(True)

pygame.quit()
quit()
		
