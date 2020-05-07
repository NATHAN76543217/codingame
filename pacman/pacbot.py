import sys
import math

# Grab the pellets as fast as you can!
class case():
	def __init__(self, x, y, char, pellet = 0, value = 0):
		self.x = x
		self.y = y
		self.char = char
		self.pellet = pellet
		self.value = value

class pac_man():
	def __init__(self, x, y, ID):
		self.x = x
		self.y = y
		self.pos = (x, y)
		self.id = ID
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
		score = 0
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
		while 1:
			if self.x + mx == width:
				mx -= width
			elif self.x +mx == 0:
				mx += width -1
			ma_case = my_map[self.y + my][self.x + mx]
			if ma_case.pellet == 1:
				score += 1
			if ma_case.char == '#':
				return score, ma_case.x, ma_case.y
			my += dy
			mx += dx
def Sqr(a):
	return a*a
def Distance(x1,y1,x2,y2):
	return math.sqrt(Sqr(y2-y1)+Sqr(x2-x1))
	
def print_map(my_map):
	for cle, ligne in enumerate(my_map):
		for case in ligne:
			print(case.char, file=sys.stderr)
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

# print_map(my_map)
# game loop
while True:
	myPacList = [] #liste de tous mes pac_man
	my_score, opponent_score = [int(i) for i in input().split()]
	visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
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
			myPacList.append(pac_man(x, y, pac_id))
	visible_pellet_count = int(input())  # all pellets in sight
	#init my_map.pellet a 0
	for ligne in my_map:
		for case in ligne:
			case.pellet = 0
			case.value = 0
	pallet_list = []
	big_pallet_list = []
	for i in range(visible_pellet_count):
		# value: amount of points this pellet is worth
		x, y, value = [int(j) for j in input().split()]
		pallet_list.append((x, y, value))
		if value > 1:
			big_pallet_list.append((x, y, value))
		my_map[y][x].pellet = 1
		my_map[y][x].value = value

		#print("pellet_list", x, y, value, file=sys.stderr)
	for pac in myPacList:
		#Pour chacun de mes pac
		poss = pac.get_way(my_map)
		#recuperer les possibilités NESW
		ways = []
		for i in range(4):
			if poss[i] == 1:
				#si le chemin est degagé
				way = pac.get_pellets(my_map, i)
				print("on way:", i, "pallet:", way, file=sys.stderr)
				ways.append(way)
		print("ways not sorted", ways, file=sys.stderr)
		ways.sort(reverse = True, key= lambda way: way[0])
		print("ways sorted", ways, file=sys.stderr)
		interupt = 0
		#####


		#ajouter condition pour empecher de changer tout le temp de cible
		#voir partie actuelle
		####
		longest = 5
		for big in big_pallet_list:
			dist = Distance(big[0], big[1], pac.x, pac.y)
			if dist <= longest:
				longest = dist
				near = big
				interupt = 1

		if interupt == 1:	
				print("MOVE 0", near[0], near[1])
		# if toute les voies contiennent 0 pastille
		elif ways[0][0] == 0:
			#recuperer la pastille la plus proche
			longest = 10000  
			for pallet in pallet_list:
				dist = Distance(pallet[0], pallet[1], pac.x, pac.y)
				if dist < longest:
					longest = dist
					near = pallet
			# y aller
			print("MOVE 0", near[0], near[1])
		else:
			print("MOVE 0", ways[0][1], ways[0][2])

	# Write an action using print
	# To debug: print("Debug messages...", file=sys.stderr)

	# MOVE <pacId> <x> <y>

