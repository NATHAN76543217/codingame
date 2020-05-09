import sys
import math
import time
import random

class pallet:
	def __init__(self, x, y):
		self.x = x
		self.y = y
class case():
	def __init__(self, x, y, ctype, obj = None):
		self.x = x
		self.y = y
		self.ctype = ctype
		self.obj = obj
class pac_man():
	def __init__(self, ID, x, y, type_id, speed_turns_lest, ability_cooldown, big_target = None):
		self.x = x
		self.y = y
		self.oldx = 0
		self.oldy = 0
		self.id = ID
		self.type_id = type_id
		if self.type_id == "ROCK":
			self.type = 1
		elif self.type_id == "SCISSORS":
			self.type = 2
		elif self.type_id == "PAPER":
			self.type = 3
		self.speed_turns_left = speed_turns_left
		self.ability_cooldown = ability_cooldown
		self.big_target = big_target
		self.target = []

#fonction map() pour cree la map (une fois pour chaque liste)

def Sqr(a):
#recupere la carré de la valeur
	return a*a
def Distance(x1,y1,x2,y2):
#recupere la disctance netre deux points
	return math.sqrt(Sqr(y2-y1)+Sqr(x2-x1))	
def get_random_pos():
#renvoi une position random dans les limites de la map
	w = random.randint(0, width -1)
	h = random.randint(0, height -1)
	return w, h
def create_case(x, y, char):
	if char == '#':
		return case(x, y, MUR)
	else:
		return case(x, y, PALLET, pallet(x, y))

width, height = [int(i) for i in input().split()]
#CONSTANTES POUR LA MAP
VIDE = 0
MUR = 1
PALLET = 2
PACMAN = 3

#initialise la map avec les mur et les pastilles
my_map = []
for y in range(height):
	x = 0
	my_line = []
	for char in input():
		my_line.append(create_case(x, y, char))
		x += 1
	my_map.append(my_line)

# game loop
while True:
	my_score, opponent_score = [int(i) for i in input().split()]
	visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
	#RAFRAICHIR LA MAP (VIRER TOUT LES PACMAN)
	for row in my_map:
		for my_case in row:
			if my_case.ctype == PACMAN:
				my_case.ctype = VIDE
				my_case.obj = None
	#RECUPERE INFO POUR CHAQUE PACMAN VISIBLE
	myPacList = []
	for i in range(visible_pac_count):
		#RECUPERE INFO PACMAN
		pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
		pac_id = int(pac_id)
		mine = mine != "0"
		x = int(x)
		y = int(y)
		speed_turns_left = int(speed_turns_left)
		ability_cooldown = int(ability_cooldown)
		#CREE UN PAC MAN
		new_pac = pac_man(pac_id, x, y, type_id, speed_turns_left, ability_cooldown)
		#L'AJOUTE A LA MAP
		my_map[y][x].ctype = PACMAN
		my_map[y][x].obj = new_pac
		#SI IL EST A MOI, L'AJOUTE A MYPACLIST
		if mine == 1:
			myPacList.append(new_pac)
	visible_pellet_count = int(input())  # all pellets in sight
	for i in range(visible_pellet_count):
		# value: amount of points this pellet is worth
		x, y, value = [int(j) for j in input().split()]
	#POUR CHAQUE PACMAN
	for pac in myPacList:
		#MISE A JOUR DE LA MAP
		#SI BESOIN DE SWITCH
		if ...:
		#SINON SI POSSIBILITE DE SPEED
		elif pac.ability_cooldown == 0:
		#SINON SI BIG PROCHE
		
		#SINON SI AUCUNE PASTILLE SUR LES CHEMINS
		#SINON ALLER AU BOUT DU MEILLEUR CHEMIN