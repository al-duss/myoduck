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
		self.elem = elem
		self.att1 = att1
		self.att2 = att2
		self.hp = hp

class Player:
	'Player with his playable units'

	def __init__(self):
		self.units = []

	def add_unit(self, unit):
		self.units.append(unit)