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
pygame.display.set_caption('Ducky Strikes Back')
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
log = pygame.image.load("assets/log.png")
log = pygame.transform.scale(log, (250,50))
life = pygame.image.load("assets/life.png")
life = pygame.transform.scale(life, (35,45))

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
def continue_next_level(user_lives):
	font = pygame.font.Font(None, 36)		
	text = font.render("Congratulations! Shoot to continue to next level!", 1, (10, 10, 10))																												
	print_background()
	screen.blit(text, (80,display_height/2))
	if user_lives == 3:
		print_life(125,display_height-50)
	if user_lives >= 2:
		print_life(75,display_height-50)
	if user_lives >= 1:
		print_life(25,display_height-50)
	display_level(GAME.level)
	print_player(display_width/2,display_height-70)
	pygame.display.update()
	GAME.next_level = True
	while GAME.next_level:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:	
				GAME.next_level = False
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
	while GAME.win:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:	
				GAME.win = False
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


class State:
	def __init__(self):
		self.bulletsUser=[]
		self.dist_ship=0
		self.x=display_width/2
		self.y=display_height-70
		self.myo=0
		self.over=True
		self.level=1
		self.speed=1
		self.bulletPercentage=40
		self.log_health=3
		self.win=False
		self.next_level=False
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
        	if GAME.win:
        		GAME.win=False
        	if GAME.next_level:
        		GAME.next_level=False
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
	
	dist = 5
	direction = 1


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
			if collision(z.x,z.y,GAME.x,GAME.y,EnnemyShip.ennemy_width,EnnemyShip.ennemy_width):
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

			if rect_collision(bullets.x, bullets.y, logx, logy, bubbles_width, 250):
				log_hit += 1
				try:
					GAME.bulletsUser.remove(bullets)
				except Exception:
					print "ExceptionI"
			if rect_collision(bullets.x, bullets.y, logx1, logy1, bubbles_width, 250):
				log_hit1 += 1
				try:
					GAME.bulletsUser.remove(bullets)
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
			GAME.bulletsUser=[]
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
			GAME.x=display_width/2
			GAME.y=display_height-70

		if user_lives<1:
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
		
