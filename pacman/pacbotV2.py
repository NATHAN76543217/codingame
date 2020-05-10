#MODULES EXTERNES
import sys
import math
import time
import random

#CLASSES
class pallet:
	def __init__(self, x, y):
		self.x = x
		self.y = y
class case():
	def __init__(self, x, y, char, ctype, obj = None):
		self.x = x
		self.y = y
		self.char = char
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
		self.target = []
	def get_path(self, pallet_list, my_map, dx, dy):
	#renvoi deux tuples pour les coord de la 1er et derniere case plus le score	
		mx = dx
		my = dy
		score = 0
		while 1:
			#Pour chaques cases dans le chemin 
			found = 0
			#Pour gerer le passage d'un cote a l'autre de la map
			if self.x + mx == width -1 and my_map[self.y + my][self.x + mx] != '#':
				mx -= width -1
			elif self.x + mx == width:
				mx -= width
			elif self.x + mx == 0 and my_map[self.y + my][self.x + mx].char != '#' and dx == -1:
				mx += width - 1
			#Pour gerer le type de la case
			ma_case = my_map[self.y + my][self.x + mx]
			if ma_case.ctype == VIDE:
				score -= 1
			elif ma_case.ctype == MUR:
				return (self.x + dx, self.y + dy)(ma_case.x - dx, ma_case.y - dy), score
			elif ma_case.ctype == PACMAN:
				score -= 3
				return (self.x + dx, self.y + dy)(ma_case.x - dx, ma_case.y - dy), score
			elif ma_case.ctype == PALLET:
				#Si il y a la position un pallet de meme position que la case
				for pallet in pallet_list:
					if pallet[0] == case.x and pallet[1] == case.y:
						found = 1
						score += 1
				if found == 0:
					ma_case.ctype == VIDE
					del(ma_case.obj)
			#passe a la case d'apres
			mx += dx
			my += dy

	def checkNESW(self, my_map):
		#renvoie une liste de chemins
		#doit gerer la sortie droite
		ways = []
		for i in range(4):
			#Pour chacunes des 4 directions
			dx = 0
			dy = 0
			if i == 0:
				dy = -1
			elif i == 1:
				dx = 1
			elif i == 2:
				dy = 1
			elif i == 3:
				dy = -1
			if my_map[self.y+dy][self.x + dx].char != '#':
					ways.append(self.get_path(my_map, dx, dy))
		return ways

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
		return case(x, y, char, MUR)
	else:
		return case(x, y, '.', PALLET, pallet(x, y))
def print_map(my_map):
	for row in my_map:
		for case in row:
			print(case.char, end=' ')
		print('')
#affiche la map
def print_path(path):
#affiche un chemin
	print("PATH from: %s to : %s score: %s", path[0], path[1], path[2])
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
	myPacList = []
	pallet_list = []
	big_pallet_list = []

	my_score, opponent_score = [int(i) for i in input().split()]
	visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
	#RAFRAICHIR LA MAP (VIRER TOUT LES PACMAN)
	for row in my_map:
		for my_case in row:
			if my_case.ctype == PACMAN:
				my_case.ctype = VIDE
				del(my_case.obj)
	#RECUPERE INFO POUR CHAQUE PACMAN VISIBLE
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
		pallet_list.append((x, y, value))
		if value > 1:
			big_pallet_list.append([x, y, value, 0])
		

	print_map(my_map)
	#POUR CHAQUE PACMAN
	for pac in myPacList:
		#MISE A JOUR DE LA MAP
		pac.checkNESW(my_map)
		#SI BESOIN DE SWITCH
		if ...:
		#SINON SI POSSIBILITE DE SPEED
		elif pac.ability_cooldown == 0:
		#SINON SI BIG PROCHE

		#SINON SI AUCUNE PASTILLE SUR LES CHEMINS
		#SINON ALLER AU BOUT DU MEILLEUR CHEMIN