from enum import Enum

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
		self.units = []

	def add_unit(self, unit):
		self.units.append(unit)