import random as r
from units import *

p1 = Player()
p2 = Player()

def createUnit(elem):
	a1 = r.randint(1,7)
	while a1 == elem.value:
		a1 = r.randint(1,7)
	a2 = r.randint(1,7)
	while a2 == elem.value or a2 == a1:
		a2=r.randint(1,7)
	u = Unit(elem,Type(a1),Type(a2),r.randint(7,12))
	return u

def initialize():
	types = list(Type)
	r.shuffle(types)
	for x in range(0,2):
		p1.add_unit(createUnit(types[x]))
		p2.add_unit(createUnit(types[x+3]))

def attack(attack, target):
	dmg = r.randint(3,5)
	if(
		attack is Type.fire and target.elem is (Type.grass or Type.ice)
		attack is Type.water and target.elem is (Type.fire or Type.rock)
		attack is Type.grass and target.elem is (Type.water or Type.rock)
		attack is Type.rock and target.elem is (Type.air or Type.electric)
		attack is Type.electric and target.elem is (Type.ice or Type.water)
		attack is Type.ice and target.elem is (Type.grass or Type.air)
		attack is Type.air and target.elem is (Type.electric or Type.fire)
	  ):
		dmg = dmg*2
	receiver.hp = receiver.hp - dmg

if __name__ == '__main__':
    main()