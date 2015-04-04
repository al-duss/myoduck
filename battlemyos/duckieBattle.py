import pygame, sys
from pygame.locals import *
import random as r
from enum import Enum

DISPLAYSURF = pygame.display.set_mode((500,500))
pygame.display.set_caption('DUCKY BATTLE')

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None
BASICFONTSIZE=20

WHITE = (255,255,255)
BLUE=(0,0,128)
GREEN=(0,128,0)
RED=(255,0,0)
BROWN=(139,69,19)
YELLOW=(255,255,0)
LIGHTBLUE=(240,248,255)
SILVER=(230,230,250)

LEFT='left'
RIGHT='right'

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, GAMESTATE

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	pygame.display.set_caption('DUCKY BATTLE')
	fontObj = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

	game_intro()
	while True:
		runGame()
		showGameOverScreen()

def runGame():
	p1 = Player() #Initialize the players with their units
	p2 = Player()
	createPlayers(p1,p2)
	selectedUnit = p1.unit[1]
	while True:
		if p1.units[0].hp < 1 and p1.units[1].hp < 1 and p1.units[2].hp < 1:
			showGameOverScreen()
		if p2.units[0].hp < 1 and p2.units[1].hp < 1 and p2.units[2].hp < 1:
			showVictoryScreen()

		checkForQuit()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					goLeft()
				if event.key == pygame.K_RIGHT:
					goRight()
				if event.key == pygame.K_SPACE:
					accept()
				if event.key == pygame.K_LCTRL:
					goBack()
'''
while True:
	DISPLAYSURF.fill(WHITE)
	DISPLAYSURF.blit(textSurfaceObj, textRectObj)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		pygame.display.update()
'''
class Status(Enum):
	wait = 1
	unitSelect = 2
	attackSelect = 3
	targetSelect = 4

class Type(Enum):
	fire = 1
	water = 2
	grass = 3
	rock = 4
	electric = 5
	ice = 6
	air = 7

class Unit:
	'Unit used in combat, having one type and three attacks'

	def __init__(self, elem, att1, att2, hp):
		self.elem = elem #The Type of the unit, which determines how it receives damage and one attack
		self.att1 = att1 #The Type of the second attack
		self.att2 = att2 #The Type of the third attack
		self.hp = hp #The hit points of the unit before it is defeated

class Player:
	'Player with his playable units'

	def __init__(self):
		self.units = [] #List of all units to be used by one player

	def add_unit(self, unit):
		self.units.append(unit)

def createUnit(elem):
	a1 = r.randint(1,7)
	while a1 == elem.value:
		a1 = r.randint(1,7)
	a2 = r.randint(1,7)
	while a2 == elem.value or a2 == a1:
		a2=r.randint(1,7)
	u = Unit(elem,Type(a1),Type(a2),r.randint(7,12))
	return u

def createPlayers(p1, p2):
	types = list(Type)
	r.shuffle(types)
	for x in range(0,2):
		p1.add_unit(createUnit(types[x]))
		p2.add_unit(createUnit(types[x+3]))

def attack(attack, target):
	dmg = r.randint(3,5)
	if(
		(attack is Type.fire and target.elem is (Type.grass or Type.ice)) or
		(attack is Type.water and target.elem is (Type.fire or Type.rock)) or
		(attack is Type.grass and target.elem is (Type.water or Type.rock)) or
		(attack is Type.rock and target.elem is (Type.air or Type.electric)) or
		(attack is Type.electric and target.elem is (Type.ice or Type.water)) or
		(attack is Type.ice and target.elem is (Type.grass or Type.air)) or
		(attack is Type.air and target.elem is (Type.electric or Type.fire))
	  ):
		dmg = dmg*2
	receiver.hp = receiver.hp - dmg

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

def checkForQuit():
	for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
		if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

if __name__ == '__main__':
	main()