import sys
import math
import time
import random
# Grab the pellets as fast as you can!
class case():
	def __init__(self, x, y, char, pellet = 0, value = 0):
		self.x = x
		self.y = y
		self.char = char
		self.pellet = pellet
		self.value = value

class pac_man():
	def __init__(self, ID, x, y, type_id, speed_turns_lest, ability_cooldown, big_target = None):
		self.x = x
		self.y = y
		self.oldx = 0
		self.oldy = 0
		self.id = ID
		self.type_id = type_id
		self.speed_turns_left = speed_turns_left
		self.ability_cooldown = ability_cooldown
		self.big_target = big_target
		self.target = []

	def get_way(self, my_map):
		#renvoie 1 si libre sinon 0, pour les 4 directions
		#gere la sortie droite
		ways = []
		for i in range(4):
			if i == 0:
				if my_map[self.y - 1][self.x].char == ' ':
					ways.append(1)
				else:
					ways.append(0)
			elif i == 1:
				if self.x == width - 1:
					ways.append(1)
				elif my_map[self.y][self.x + 1].char == ' ':
					ways.append(1)
				else:
					ways.append(0)
			elif i == 2:
				if my_map[self.y + 1][self.x].char == ' ':
					ways.append(1)
				else:
					ways.append(0)
			elif i == 3:
				if self.x == 0:
					ways.append(1)
				elif my_map[self.y][self.x - 1].char == ' ':
					ways.append(1)
				else:
					ways.append(0)
		print("ways:", ways, file=sys.stderr)
		return ways
	def get_pellets(self, my_map, i):
	#recupere la valeur d'un chemin
		#initialise dx et dy en fonction de l'orientation du chemin
		dx = 0
		dy = 0
		if i == 0:
			dy = -1
		elif i == 1:
			dx = 1
		elif i == 2:
			dy = 1
		else:
			dx = -1
		my = dy
		mx = dx
		score = 0
		while 1:
		#Pour chaque cases
		#gere le passage d'un cote de la map a l'autre
			if self.x + mx == width - 1 and my_map[self.y + my][self.x + mx].char != '#':
				mx -= width -1
			elif self.x + mx == width:
				mx -= width
			elif self.x + mx == 0 and my_map[self.y + my][self.x + mx].char != '#' and i == 3:
				mx += width - 1
		#recupere la case actuelle
			ma_case = my_map[self.y + my][self.x + mx]
		#si il y a un pellet sur la case augmente le score	
			if ma_case.pellet == 1:
				score += 1
		#si la case est vide diminuer le score
			elif ma_case.char == ' ':
				score -= 1
		#si c'est un mur arreter de chercher et renvoyer la position de la case avant le mur et le score 
			elif ma_case.char == '#':
				return ma_case.x -dx, ma_case.y-dy, score
		#sinon passer a la case d'apres
			my += dy
			mx += dx



def Sqr(a):
#recupere la carré de la valeur
	return a*a
def Distance(x1,y1,x2,y2):
#recupere la disctance netre deux points
	return math.sqrt(Sqr(y2-y1)+Sqr(x2-x1))	
def print_map(my_map):
#affiche la map
	for cle, ligne in enumerate(my_map):
		for case in ligne:
			print(case.char, file=sys.stderr)
def get_random_pos():
#renvoi une position random dans les limites de la map
	w = random.randint(0, width -1)
	h = random.randint(0, height -1)
	return w, h

# width: size of the grid
# height: top left corner is (x=0, y=0)
width, height = [int(i) for i in input().split()]
print("Width =", width, "heigh=", height, file=sys.stderr)
#map = list de listes
my_map = []
for i in range(height):
	my_line = []
	P = 0
	for char in input():  # one line of the grid: space " " is floor, pound "#" is wall
		my_line.append(case(P, i, char, 0, 0))
		P+=1
	my_map.append(my_line)

TURN = 0
myPacList = [] #liste de tous mes pac_man
enPacList = [] #liste de tous les pac-man ennemies

old_visible_pac_count = 100

# print_map(my_map)
# game loop
while True:
	# Debut du decompte du temps
	start_time = time.time()
	my_action = ""
	my_score, opponent_score = [int(i) for i in input().split()]
	visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
	if visible_pac_count < old_visible_pac_count:
		TURN = 0

	if TURN == 0:
	#Si c'est le premier tour, initialiser les listes des pac-man
		print("TURN 0", file=sys.stderr)
		TURN = 1
		myPacList = []
		enPacList = []
		for i in range(visible_pac_count):
			# pac_id: pac number (unique within a team)
			# mine: true if this pac is yours
			# x: position in the grid
			# y: position in the grid
			# type_id: unused in wood leagues
			# speed_turns_left: unused in wood leagues
			# ability_cooldown: unused in wood leagues	
			pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
			pac_id = int(pac_id)
			mine = mine != "0"
			x = int(x)
			y = int(y)
			speed_turns_left = int(speed_turns_left)
			ability_cooldown = int(ability_cooldown)
			if mine == 1:
				myPacList.append(pac_man(pac_id, x, y, type_id, speed_turns_left, ability_cooldown))
			else:
				enPacList.append(pac_man(pac_id, x, y, type_id, speed_turns_left, ability_cooldown))
	else:
	# chaque tour mettre a jour les information de mes pac-mans
		for i in range(visible_pac_count):
			pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
			pac_id = int(pac_id)
			mine = mine != "0"
			x = int(x)
			y = int(y)
			speed_turns_left = int(speed_turns_left)
			ability_cooldown = int(ability_cooldown)
			#Pour moi
			if mine == 1:
				for pac in myPacList:
					if pac_id == pac.id:
						pac.x = x
						pac.y = y
						pac.type_id = type_id
						pac.speed_turns_left = speed_turns_left
						pac.ability_cooldown = ability_cooldown
			#pour les ennemies
			else:
				for pac in enPacList:
					if pac_id == pac.id:
						pac.x = x
						pac.y = y
						pac.type_id = type_id
						pac.speed_turns_left = speed_turns_left
						pac.ability_cooldown = ability_cooldown

	#init my_map.pellet a 0
	for ligne in my_map:
		for case in ligne:
			case.pellet = 0
			case.value = 0

	#recupere liste pellet
	pallet_list = []
	big_pallet_list = []
	visible_pellet_count = int(input())  # all pellets in sight
	for i in range(visible_pellet_count):
		x, y, value = [int(j) for j in input().split()]
		pallet_list.append((x, y, value))
		if value > 1:
			big_pallet_list.append([x, y, value, 0])
		my_map[y][x].pellet = 1
		my_map[y][x].value = value




	for pac in myPacList:
		print("for pac:", pac.id, file=sys.stderr)
	#si pac-man bloqué
		if pac.oldx == pac.x and pac.oldy == pac.y:
			print("pac blocked, x=", x, "y=", y, file=sys.stderr)
			pac.target = get_random_pos()
			my_action = my_action + ("MOVE "+ str(pac.id) + " "+ str(pac.target[0]) + " "+ str(pac.target[1]) + " | ")
			continue
	#Pour chacun de mes pac
		poss = pac.get_way(my_map)
	#recuperer les possibilités NESW
		ways = []
		for i in range(4):
			if poss[i] == 1:
				ways.append(pac.get_pellets(my_map, i))
		ways.sort(reverse = True, key= lambda way: way[2])
	#les trier par ordre de preference
		print("ways sorted", ways, file=sys.stderr)
	
	#recherche des big proches
		longest = 5
		near = []
		interupt = 0
		for big in big_pallet_list:
			if big[3] == 0:
				dist = Distance(big[0], big[1], pac.x, pac.y)
				if dist <= longest:
					longest = dist
					near = big
					interupt = 1
	#si un big est plus proche que 5 cases
		print("pac.big:", pac.big_target, file=sys.stderr)
		if interupt == 1 or pac.big_target is not None:	
			if pac.big_target is None:
				near[3] = 1
				pac.big_target = near
				pac.target = near
				# my_action = my_action + ("MOVE " + str(pac.id) + " "+ str(near[0]) + " "+ str(near[1]) + " | ")
				print("after:", pac.big_target, file=sys.stderr)
			else:
				pac.target = pac.big_target
				# my_action = my_action + ("MOVE " + str(pac.id) + " "+ str(pac.big_target[0]) + " "+ str(pac.big_target[1]) + " | ")
				pac.big_target = None

		# si toute les voies contiennent 0 pastille
		elif ways[0][2] <= 0:
			#recuperer la pastille la plus proche
			longest = 10000  
			near = None
			for pallet in pallet_list:
				dist = Distance(pallet[0], pallet[1], pac.x, pac.y)
				print("palletDist =", dist, file=sys.stderr)
				if dist < longest:
					longest = dist
					near = pallet
			#rejoindre la plus proche	
			if near != None:
				pac.target = near
				# my_action = my_action + ("MOVE "+ str(pac.id)+ " " + str(near[0]) + " " + str(near[1]) + " | ")
			# si il n'y a aucune pastille visible
			else:
				#aller au big le plus proche

				#sinon aller a une position random
				rand_pos = get_random_pos()
				pac.target = rand_pos
				# my_action = my_action + ("MOVE "+ str(pac.id)+ " " + str(rand_pos[0]) + " " + str(rand_pos[1]) + " | ")
		else:
			#aller au bout du chemin
			pac.target = ways[0]
			# my_action = my_action + ("MOVE "+ str(pac.id) + " "+ str(ways[0][1]) + " "+ str(ways[0][2]) + " | ")
		my_action = my_action + ("MOVE "+ str(pac.id) + " "+ str(pac.target[0]) + " "+ str(pac.target[1]) + " | ")
		pac.oldx = pac.x
		pac.oldy = pac.y
	
	print(my_action)
	old_visible_pac_count = visible_pac_count
	print("Temps d execution : %s ms ---" % ((time.time() - start_time) * 1000), file=sys.stderr)
	# MOVE <pacId> <x> <y>

