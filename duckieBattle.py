import pygame, sys
from pygame.locals import *
import random as r
from enum import Enum

class Status(Enum):
	wait = 1
	attackSelect = 2
	targetSelect = 3

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

BLACK = (0,0,0)
WHITE = (255,255,255)
display_width = 800
display_height = 500

def main():
	global status, screen, selectedUnit, selectedAttack, selectedTarget, p1, p2
	pygame.init()
	screen = pygame.display.set_mode((display_width, display_height))
	pygame.display.set_caption('DUCKY BATTLE')
	screen.fill(WHITE)
	clock = pygame.time.Clock()
	status = Status.attackSelect # Placeholders
	p1 = Player()
	p2 = Player()
	createPlayers(p1,p2)
	selectedUnit = p1.units[0]
	selectedAttack = p1.units[0].elem
	selectedTarget = p2.units[1]
	status = Status.attackSelect

	while True:
		print_background()
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
status = Status.attackSelect #placeholders to initialize global variables
selectedUnit = Unit(1,1,1,1) 
selectedAttack = Type.fire
selectedTarget = Unit(1,1,1,1)
p1 = Player()
p2 = Player()
'''
background = pygame.image.load("assets/bg.png")
background = pygame.transform.scale(background, (display_width, display_height))

fireduck = pygame.image.load("assets/fire_duck.png")
fireduck= pygame.transform.scale(fireduck, (64,64))
waterduck = pygame.image.load("assets/water_duck.png")
waterduck= pygame.transform.scale(waterduck, (64,64))
grassduck = pygame.image.load("assets/grass_duck.png")
grassduck= pygame.transform.scale(grassduck, (64,64))
rockduck = pygame.image.load("assets/rock_duck.png")
rockduck= pygame.transform.scale(rockduck, (64,64))
elecduck = pygame.image.load("assets/lightning_duck.png")
elecduck= pygame.transform.scale(elecduck, (64,64))
iceduck = pygame.image.load("assets/ice_duck.png")
iceduck= pygame.transform.scale(iceduck, (64,64))
airduck = pygame.image.load("assets/air_duck.png")
airduck= pygame.transform.scale(airduck, (64,64))

fireball = pygame.image.load("assets/fireball.png")
fireball= pygame.transform.scale(fireball, (24,24))
bubbles = pygame.image.load("assets/bubbles.png")
bubbles= pygame.transform.scale(bubbles, (24,24))
leaf = pygame.image.load("assets/leaf.png")
leaf= pygame.transform.scale(leaf, (24,24))
rock = pygame.image.load("assets/rock.png")
rock= pygame.transform.scale(rock, (24,24))
lightning = pygame.image.load("assets/lightning.png")
lightning= pygame.transform.scale(lightning, (24,24))
ice = pygame.image.load("assets/ice.png")
ice= pygame.transform.scale(ice, (24,24))
wind = pygame.image.load("assets/wind.png")
wind= pygame.transform.scale(wind, (24,24))

'''
def text_objects(text, font):
	textSurface = font.render(text, 1, BLACK)
	return textSurface, textSurface.get_rect()
'''

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
	target.hp = target.hp - dmg

def print_background():
	screen.blit(background, (0,0))
'''
def game_intro():

	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:	
				intro = False

		screen.fill(WHITE)
		largeText = pygame.font.Font('freesansbold.ttf',80)
		smallText = pygame.font.Font('freesansbold.ttf',45)
		TextSurf, TextRect = text_objects("BATTLE DUCKIES", largeText)
		TextSurf1, TextRect1 = text_objects("Press Any Key To Continue...", smallText)
		TextRect.center = ((display_width/2),(display_height/2))
		TextRect1.center = ((display_width/2),(display_height/2 + 150))
		screen.blit(TextSurf, TextRect)
		screen.blit(TextSurf1, TextRect1)
		pygame.display.update()
		clock.tick(15)
'''
def checkForQuit():
	for event in pygame.event.get((QUIT, KEYUP)): # event handling loop
		if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

def goLeft():
	if status is Status.attackSelect:
		if selectedAttack is selectedUnit.elem:
			selectedAttack = selectedUnit.att1
		if selectedAttack is selectedUnit.att1:
			selectedAttack = selectedUnit.att2
		if selectedAttack is selectedUnit.att2:
			selectedAttack = selectedUnit.elem
	if status is Status.targetSelect:
		index = p2.units.index(selectedUnit)
		selectedUnit = p2.units[(index-1)%3]

def goRight():
	if status is Status.attackSelect:
		if selectedAttack is selectedUnit.elem:
			selectedAttack = selectedUnit.att2
		if selectedAttack is selectedUnit.att1:
			selectedAttack = selectedUnit.elem
		if selectedAttack is selectedUnit.att2:
			selectedAttack = selectedUnit.att1
	if status is Status.targetSelect:
		index = p2.units.index(selectedTarget)
		selectedTarget = p2.units[(index+1)%3]

def accept():
	global status, selectedTarget,selectedAttack, selectedUnit, p1
	if status is Status.targetSelect:
		attack(selectedAttack,selectedTarget)
		status = Status.wait
		index = p1.units.index(selectedUnit)
		selectedUnit = p1.units[(index+1)%3]
	if status is Status.attackSelect:
		status = Status.targetSelect

def goBack():
	if status is Status.targetSelect:
		status = Status.attackSelect

'''
runGame()
pygame.quit()
quit()
'''

if __name__ == '__main__':
	main()