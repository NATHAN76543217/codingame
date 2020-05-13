# MODULES EXTERNES
import sys
import math
import time
import random

#CLASSES
class pallet:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.targeted = 0
class case():
	def __init__(self, x, y, char, ctype, obj = None):
		self.x = x
		self.y = y
		self.char = char
		self.ctype = ctype
		self.obj = obj
class pac_man():
	def __init__(self, mine, ID, x, y, type_id, speed_turns_lest, ability_cooldown, big_target = None):
		self.x = x
		self.y = y
		self.oldx = 0
		self.oldy = 0
		self.id = ID
		self.speed_turns_left = speed_turns_left
		self.ability_cooldown = ability_cooldown
		self.transformed = 0
		self.mine = mine
		self.big = None
		self.have_target = 0
		self.target = None
		self.ignored = 0
		self.needToSwitch = 0
		self.my_switch = None
		self.type_id = type_id
		if self.type_id == "ROCK":
			self.type = 1
		elif self.type_id == "SCISSORS":
			self.type = 2
		elif self.type_id == "PAPER":
			self.type = 3
		
	def get_path(self, pallet_list, big_list, my_map, dx, dy):
	#renvoi deux tuples pour les coord de la 1er et derniere case plus le score du chemin 	
		mx = dx
		my = dy
		score = 0
		have_pallet = 0
		mid_point = 0
		csave = 0
		while 1:
			#Pour chaques cases dans le chemin 
			found = 0
			#Pour gerer le passage d'un cote a l'autre de la map
			if self.x + mx == width - 1 and my_map[self.y + my][self.x + mx].char != '#' and dx == 1:
				mx -= width -1
			elif self.x + mx == width:
				mx -= width
			elif self.x + mx == 0 and my_map[self.y + my][self.x + mx].char != '#' and dx == -1:
				mx += width - 1
				csave = mx
				mid_point = 1
			#Pour gerer le type de la case
			ma_case = my_map[self.y + my][self.x + mx]
			if ma_case.ctype == VIDE:
				score -= 1
			elif ma_case.ctype == MUR:
				if have_pallet == 0:
					score = -10
				if mid_point == 1:
					mid_point = 0
					return [(self.x + dx, self.y + dy), (csave, ma_case.y), score]
				else:
					return [(self.x + dx, self.y + dy), (ma_case.x - dx, ma_case.y - dy), score]
			elif ma_case.ctype == PACMAN:
				dist = Distance(ma_case.x, ma_case.y, self.x, self.y)
				if have_pallet == 0 or (dist <= 2 and dist != 0) or ma_case.obj.mine == 0:
					score = -10
				if ma_case.obj.mine == 0:
					print("PAC ENNEMIE DETECTED", ma_case.x, ma_case.y, ma_case.obj.id, ma_case.obj.x, ma_case.obj.y, ma_case.char, ma_case.obj.type_id, file=sys.stderr)
					if self.type - ma_case.obj.type in (1, -2, 0):
					#si je suis moins fort que lui
						# near = self.big_near(big_list)
						print("Loose", file=sys.stderr)
						dist_ennemie = Distance(ma_case.x, ma_case.y, self.x, self.y)
						if self.ability_cooldown <= 1 and dist_ennemie < 6 and dist_ennemie > ability_cooldown :
						# 	#si je peux me transformer
						# 	#je le fais et je lui fonce dessus
							self.needToSwitch = 1
							self.set_my_switch(ma_case.obj.type_id)
							self.have_target = 1
							self.target = ma_case.obj.x, ma_case.obj.y

						else:
							score -= 100
							#le fuire
					# elif Distance(self.x, self.y, ma_case.obj.x, ma_case.obj.y) <= 2 and self.turnturn_count <= 3:
					# # 	#si je suis plus fort que lui je lui fonce mais pas pendant plus de 3 tours
					# 	self.have_target = 1
					# 	self.target = ma_case.obj.x, ma_case.obj.y
					# 	turn_count += 1
					# 	if turn_count == 3:
					# 		turn_count = 0
					score -= 3
				if mid_point == 1:
					mid_point = 0
					print("MID, csave=", csave, file=sys.stderr)
					if csave < 0:
						csave += width
					print("csave=", csave, file=sys.stderr)
					return [(self.x + dx, self.y + dy), (csave, ma_case.y), score]
				else:
					px = ma_case.x -dx
					if px < 0:
						px += width
					return [(self.x + dx, self.y + dy), (px, ma_case.y -dy), score]
			elif ma_case.ctype == PALLET:
				#Si il y a un pellet de meme position que la case
				for pallet in pallet_list:
					if pallet[0] == ma_case.x and pallet[1] == ma_case.y:
						found = 1
						have_pallet = 1
						score += 1
				if found == 0:
					ma_case.ctype = VIDE
					ma_case.obj = None
					ma_case.char = ' '
			# on passe a la case d'apres
			mx += dx
			my += dy
	def checkNESW(self, pallet_list, big_pallet_list, my_map):
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
				dx = -1
			if self.x + dx == width or my_map[self.y+dy][self.x + dx].char != '#':
					ways.append(self.get_path(pallet_list, big_pallet_list, my_map, dx, dy))
		return ways
	def big_near(self, big_list):
	#renvoie le big le plus proche de pac man a - de 5 de dist sinon None 
		shortest = 7
		near = None
		for big in big_list:
			dist = Distance(big[0], big[1], self.x, self.y)
			if dist <= shortest:
				shortest = dist
				near = big
		self.big = near
		return near, shortest
	def set_my_switch(self, enTypeID):
		if enTypeID == "PAPER":
			self.my_switch = "SCISSORS"
		elif enTypeID == "ROCK":
			self.my_switch = "PAPER"
		elif enTypeID == "SCISSORS":
			self.my_switch = "ROCK"
def Sqr(a):
#recupere la carré de la valeur
	return a*a
def Distance(x1,y1,x2,y2):
#recupere la disctance netre deux points
	return math.sqrt(Sqr(y2-y1)+Sqr(x2-x1))	
def get_random_pos():
#renvoi un tuple de positions random dans les limites de la map
	x = random.randint(0, width -1)
	y = random.randint(0, height -1)
	return (x, y)
def get_pallet_map_list(my_map):
#renvoie une liste de cases contenant des pellets
	lst = []
	for ligne in my_map:
		for case in ligne:
			if case.ctype == PALLET and case.obj.targeted == 0:
				lst.append(case)
	return lst			
def create_case(x, y, char):
	if char == '#':
		return case(x, y, char, MUR)
	else:
		return case(x, y, '.', PALLET, pallet(x, y))
def print_map(my_map):
	for row in my_map:
		for case in row:
			print(case.char, end=' ', file=sys.stderr)
		print('', file=sys.stderr)
#affiche la map
def print_path(path):
#affiche un chemin
	print("PATH from: %s to : %s score: %s" % path[0], path[1], path[2], file=sys.stderr)
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

TURN = 0
myPacList = []
# game loop
while True:
	start_time = time.time()
	pallet_list = []
	big_pallet_list = []
	my_action = ""
	my_score, opponent_score = [int(i) for i in input().split()]
	visible_pac_count = int(input())  # all your pacs and enemy pacs in sight

	#RAFRAICHIR LA MAP (VIRER TOUT LES PACMAN)
	for row in my_map:
		for my_case in row:
			if my_case.ctype == PACMAN:
				my_case.ctype = VIDE
				my_case.char = ' '
				my_case.obj = None
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
		if TURN == 0:
			#####CREE UN PAC MAN
			new_pac = pac_man(mine, pac_id, x, y, type_id, speed_turns_left, ability_cooldown)
			#SI IL EST A MOI, L'AJOUTE A MYPACLIST
			if mine == 1:
				myPacList.append(new_pac)
			my_map[y][x].ctype = PACMAN
			my_map[y][x].obj = new_pac
			my_map[y][x].char = 'P'	

		else:
		#MET A JOUR LES INFO DES PACS
			if mine == 1:
				for pac in myPacList:
					if pac.id == pac_id:
						pac.x = x
						pac.y = y
						pac.type_id = type_id
						if pac.type_id == "ROCK":
							pac.type = 1
						elif pac.type_id == "SCISSORS":
							pac.type = 2
						elif pac.type_id == "PAPER":
							pac.type = 3
						pac.speed_turns_left = speed_turns_left
						pac.ability_cooldown = ability_cooldown
						if pac.type_id != "DEAD":
							#L'AJOUTE A LA MAP
							my_map[y][x].ctype = PACMAN
							my_map[y][x].obj = pac
							my_map[y][x].char = 'P'
						else:
							#si le pac est mort
							print("DEBUG remove pacid:", pac.id, file=sys.stderr)
							myPacList.remove(pac)
			else:
				if type_id != "DEAD":
					new_pac = pac_man(mine, pac_id, x, y, type_id, speed_turns_left, ability_cooldown)
					# enPacList.append(new_pac)
					my_map[y][x].ctype = PACMAN
					my_map[y][x].obj = new_pac
					my_map[y][x].char = 'P'
	#CREE LES LISTES DE PELLETS
	visible_pellet_count = int(input())  # all pellets in sight
	for i in range(visible_pellet_count):
		x, y, value = [int(j) for j in input().split()]
		pallet_list.append((x, y))
		if value > 1:
			big_pallet_list.append([x, y])
		

	print_map(my_map)
	#RESOUDRE LES COLLISIONS
	count = 0
	for pac in myPacList:
		print("x= {} y = {} oldx = {} oldy = {}".format(pac.x, pac.y, pac.oldx, pac.oldy), file=sys.stderr)
		if pac.x == pac.oldx and pac.y == pac.oldy and pac.transformed != 1:
			print("pac", pac.id, "bloqué", file=sys.stderr)
			count += 1
		if count >= 2:
			rd = get_random_pos()
			my_action += ("MOVE "+ str(pac.id) + " "+ str(rd[0]) + " " + str(rd[1]) + " | ")
			pac.ignored = 1

	#POUR CHAQUE PACMAN
	for pac in myPacList:
		print("pac ID:", pac.id, file=sys.stderr)
		#SI PACMAN BLOQUE
		if pac.ignored == 1:
			print("IGNORED", file=sys.stderr)
			pac.ignored = 0
			continue
		pac.transformed = 0
		pac.have_target = 0
		pac.target = None
		#MISE A JOUR DE LA MAP ET RECUPERATION NESW
		paths = pac.checkNESW(pallet_list, big_pallet_list, my_map)
		paths.sort(key= lambda x: x[2], reverse=True)
		#SI BESOIN DE SWITCH
		if pac.needToSwitch and pac.ability_cooldown == 0:
			print("SWITCH", file=sys.stderr)
			pac.transformed = 1
			pac.needToSwitch = 0
			my_action +=  ("SWITCH " + str(pac.id) + " " + pac.my_switch + " | ")
		#SINON SI POSSIBILITE DE SPEED
		elif pac.ability_cooldown == 0:
			pac.transformed = 1
			my_action += ("SPEED " + str(pac.id) + " | ")
		elif pac.have_target == 1: #and target plus pres que le plus pres des big:
			print("HUNT", file=sys.stderr)
			my_action += ("MOVE "+ str(pac.id) + " "+ str(pac.target[0]) + " " + str(pac.target[1]) + " | ")
		#SINON SI BIG PROCHE
		elif pac.big_near(big_pallet_list)[0] is not None:
			print("BIG:", pac.big, file=sys.stderr)
			big_pallet_list.remove(pac.big)
			my_action += ("MOVE " + str(pac.id) + " " + str(pac.big[0]) + " " + str(pac.big[1]) + " | ")
		#SINON SI AUCUNE PASTILLE SUR LES CHEMINS
		elif paths[0][2] <= -10: #je regard le score du chemin avec le meilleur score
			# #aller a la pastille la plus proche
			clist = get_pallet_map_list(my_map)
			clist.sort(key = lambda case: Distance(case.x, case.y, pac.x, pac.y))
			clist[0].obj.targeted = 1
			print("NEAR at", clist[0].x, clist[0].y, file=sys.stderr)
			my_action += ("MOVE " + str(pac.id) + " " + str(clist[0].x) + " " + str(clist[0].y) + " | ")
		#SINON ALLER AU BOUT DU MEILLEUR CHEMIN
		else:
			print("PATH:", paths,  file=sys.stderr)
			my_action += ("MOVE "+ str(pac.id) + " "+ str(paths[0][1][0]) + " " + str(paths[0][1][1]) + " | ")
		pac.oldx = pac.x
		pac.oldy = pac.y
	#FIN DU TOUR
	TURN = 1
	print(my_action)
	print("Temps d execution : %s ms" % ((time.time() - start_time) * 1000), file=sys.stderr)

#PATHS = liste de path
# path = tuple + tuple + int
# 1er tuple = 1er case du chemin
# 2eme tuple = derniere case du chemin (si mur renvoie ase d'avant si pacman renvoie la case du pacman)
# int = score