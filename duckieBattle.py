import pygame, sys, time
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

FPS = 0
WHITE = (0,0,0)
BLACK = (255,255,255)
display_width = 800
display_height = 500

pygame.init()
screen = pygame.display.set_mode((display_width, display_height))

clock = pygame.time.Clock()


def main():
	global clock, status, screen, selectedUnit, selectedAttack, selectedTarget, p1, p2
	status = Status.attackSelect # Placeholders
	p1 = Player()
	p2 = Player()
	createPlayers(p1,p2)
	selectedUnit = p1.units[0]
	selectedAttack = p1.units[0].elem
	selectedTarget = p2.units[1]
	status = Status.attackSelect

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
		print_background()
		
		if p2.units[0].hp > 0:
			printDuck(p2.units[0],160,50)
		if p2.units[1].hp > 0:
			printDuck(p2.units[1],380,50)
		if p2.units[2].hp > 0:
			printDuck(p2.units[2],600,50)
		if p1.units[0].hp > 0:
			printDuck(p1.units[0],160,300)
			printElem(p1.units[0].att1,120,380)
			printElem(p1.units[0].elem,172,380)
			printElem(p1.units[0].att2,224,380)
		if p1.units[1].hp > 0:
			printDuck(p1.units[1],380,300)
			printElem(p1.units[1].att1,340,380)
			printElem(p1.units[1].elem,392,380)
			printElem(p1.units[1].att2,444,380)
		if p1.units[2].hp > 0:
			printDuck(p1.units[2],600,300)
			printElem(p1.units[2].att1,560,380)
			printElem(p1.units[2].elem,612,380)
			printElem(p1.units[2].att2,664,380)

		if status is Status.attackSelect:
			index = p1.units.index(selectedUnit)
			while selectedUnit.hp < 1:
				index = (index+1)%3
				selectedUnit = p1.units[index]
			if index == 0:
				if selectedAttack is p1.units[0].elem:
					print_ring(162,375)
				if selectedAttack is p1.units[0].att1:
					print_ring(110,375)
				if selectedAttack is p1.units[0].att2:
					print_ring(214,375)
			elif index == 1:
				if selectedAttack is p1.units[1].elem:
					print_ring(382,375)
				if selectedAttack is p1.units[1].att1:
					print_ring(330,375)
				if selectedAttack is p1.units[1].att2:
					print_ring(434,375)
			elif index == 2:
				if selectedAttack is p1.units[2].elem:
					print_ring(602,375)
				if selectedAttack is p1.units[2].att1:
					print_ring(550,375)
				if selectedAttack is p1.units[2].att2:
					print_ring(654,375)

		elif status is Status.targetSelect:
			index = p2.units.index(selectedTarget)
			while selectedTarget.hp < 1:
				index = (index+1)%3
				selectedTarget = p2.units[index]
			if index == 0:
				print_circle(140,40)
			if index == 1:
				print_circle(360,40)
			if index == 2:
				print_circle(580,40)

		elif status is Status.wait:
			i = r.randint(0,2)
			while p2.units[i].hp < 1:
				i = r.randint(0,2)
			e = r.randint(1,3)
			t = r.randint(0,2)
			while p1.units[i].hp < 1:
				t = r.randint(0,2)
			if e == 1:
				attack(p2.units[i].elem,p1.units[t])
			elif e == 2:
				attack(p2.units[i].att1, p1.units[t])
			elif e == 3:
				attack(p2.units[i].att2, p1.units[t])
			status = Status.attackSelect
		pygame.display.update()


background = pygame.image.load("assets/wasteland.png")
background = pygame.transform.scale(background, (display_width, display_height))
circle = pygame.image.load("assets/circle.png")
circle= pygame.transform.scale(circle, (100,100))
ring = pygame.image.load("assets/circle.png")
ring= pygame.transform.scale(ring, (55,55))

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
fireball= pygame.transform.scale(fireball, (32,32))
bubbles = pygame.image.load("assets/bubbles.png")
bubbles= pygame.transform.scale(bubbles, (32,32))
leaf = pygame.image.load("assets/leaf.png")
leaf= pygame.transform.scale(leaf, (32,32))
rock = pygame.image.load("assets/rock.png")
rock= pygame.transform.scale(rock, (32,32))
lightning = pygame.image.load("assets/lightning.png")
lightning= pygame.transform.scale(lightning, (32,32))
ice = pygame.image.load("assets/ice.png")
ice= pygame.transform.scale(ice, (32,32))
wind = pygame.image.load("assets/wind.png")
wind= pygame.transform.scale(wind, (32,32))

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
	for x in range(0,3):
		p1.add_unit(createUnit(types[x]))
		p2.add_unit(createUnit(types[x+3]))

def printDuck(unit,x,y):
	if unit.elem is Type.fire:
		print_fireduck(x,y)
	elif unit.elem is Type.water:
		print_waterduck(x,y)
	elif unit.elem is Type.grass:
		print_grassduck(x,y)
	elif unit.elem is Type.rock:
		print_rockduck(x,y)
	elif unit.elem is Type.electric:
		print_elecduck(x,y)
	elif unit.elem is Type.ice:
		print_iceduck(x,y)
	elif unit.elem is Type.air:
		print_airduck(x,y)
	
def printElem(t,x,y):
	if t is Type.fire:
		print_fireball(x,y)
	elif t is Type.water:
		print_bubbles(x,y)
	elif t is Type.grass:
		print_leaf(x,y)
	elif t is Type.rock:
		print_rock(x,y)
	elif t is Type.electric:
		print_lightning(x,y)
	elif t is Type.ice:
		print_ice(x,y)
	elif t is Type.air:
		print_wind(x,y)

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
	print typeName(target.elem) + " took " + str(dmg) + " damage."
	if target.hp < 1:
		print typeName(target.elem) + " was defeated."

def typeName(t):
	if t is Type.fire:
		return "Fireduck"
	if t is Type.water:
		return "Waterduck"
	if t is Type.grass:
		return "Grassduck"
	if t is Type.rock:
		return "Rockduck"
	if t is Type.electric:
		return "Electricduck"
	if t is Type.ice:
		return "Iceduck"
	if t is Type.air:
		return "Airduck"

def print_circle(x,y):
	screen.blit(circle,(x,y))

def print_ring(x,y):
	screen.blit(ring,(x,y))

def print_background():
	screen.blit(background, (0,0))

def print_fireduck(x,y):
	screen.blit(fireduck, (x,y))

def print_waterduck(x,y):
	screen.blit(waterduck, (x,y))

def print_grassduck(x,y):
	screen.blit(grassduck, (x,y))

def print_rockduck(x,y):
	screen.blit(rockduck, (x,y))

def print_elecduck(x,y):
	screen.blit(elecduck, (x,y))

def print_iceduck(x,y):
	screen.blit(iceduck, (x,y))

def print_airduck(x,y):
	screen.blit(airduck, (x,y))

def print_fireball(x,y):
	screen.blit(fireball, (x,y))

def print_bubbles(x,y):
	screen.blit(bubbles, (x,y))

def print_leaf(x,y):
	screen.blit(leaf, (x,y))

def print_rock(x,y):
	screen.blit(rock, (x,y))

def print_lightning(x,y):
	screen.blit(lightning, (x,y))

def print_ice(x,y):
	screen.blit(ice, (x,y))

def print_wind(x,y):
	screen.blit(wind, (x,y))


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
	global status, selectedUnit, selectedAttack, selectedTarget
	if status is Status.attackSelect:
		if selectedAttack is selectedUnit.elem:
			selectedAttack = selectedUnit.att1
		elif selectedAttack is selectedUnit.att1:
			selectedAttack = selectedUnit.att2
		elif selectedAttack is selectedUnit.att2:
			selectedAttack = selectedUnit.elem
	elif status is Status.targetSelect:
		index = p2.units.index(selectedTarget)
		selectedTarget = p2.units[(index-1)%3]
		while selectedUnit.hp < 1:
				index = (index-1)%3
				selectedTarget = p2.units[index]

def goRight():
	global status, selectedUnit, selectedAttack, selectedTarget
	if status is Status.attackSelect:
		if selectedAttack is selectedUnit.elem:
			selectedAttack = selectedUnit.att2
		elif selectedAttack is selectedUnit.att1:
			selectedAttack = selectedUnit.elem
		elif selectedAttack is selectedUnit.att2:
			selectedAttack = selectedUnit.att1
	elif status is Status.targetSelect:
		index = p2.units.index(selectedTarget)
		selectedTarget = p2.units[(index+1)%3]
		while selectedUnit.hp < 1:
				index = (index+1)%3
				selectedTarget = p2.units[index]

def accept():
	global status, selectedTarget,selectedAttack, selectedUnit, p1
	if status is Status.targetSelect:
		attack(selectedAttack,selectedTarget)
		index = p1.units.index(selectedUnit)
		index = (index+1)%3
		while p1.units[index].hp < 1:
			index = (index+1)%3
		selectedUnit = p1.units[index]
		status = Status.wait
	elif status is Status.attackSelect:
		status = Status.targetSelect

def goBack():
	global status
	if status is Status.targetSelect:
		status = Status.attackSelect

if __name__ == '__main__':
	main()