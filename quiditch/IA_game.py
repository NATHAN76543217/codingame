import sys
import math
from math import sqrt
from math import cos
from math import sin
# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle to grab it and use your team id to determine towards where you need to throw it.
# Use the Wingardium spell to move things around at your leisure, the more magic you put it, the further they'll move.

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
target_id = {0 : 0, 1 : 0
			,"dist0" : 0, "dist1": 0}

if my_team_id == 0:
	goal_ennemy_x = 16000
	goal_ennemy_y = 3750
else:
	goal_ennemy_x = 0
	goal_ennemy_y = 3750

if my_team_id == 0:
	goal_allie_x = 0
	goal_allie_y = 3750
else:
	goal_allie_x = 16000
	goal_allie_y = 3750

class rectangle:
	"class rectangle"
	def __init__(self):
		self.x = 0
		self.y = 0
		self.L = 0
		self.h = 0
	
	def is_in(self, x, y):
		if x > self.x and x < self.x + self.L:
			if y > self.y and y < self.y + self.h:
				return 1
		return 0
#defini 4 rectangles

my_zone = rectangle()
my_close_zone = rectangle()
my_goal_zone = rectangle()

en_zone = rectangle()
en_goal_zone = rectangle()
en_close_zone = rectangle()

if my_team_id == 0:
	my_zone.x = 0
	my_goal_zone.x = 0
	my_close_zone.x = 0
	en_zone.x = 8000
	en_goal_zone.x = 13000
	en_close_zone.x = 16000 - 3000
else:
	my_zone.x = 8000
	my_goal_zone.x = 13000
	my_close_zone.x = 13000
	en_zone.x = 0
	en_goal_zone.x = 0
	en_close_zone.x = 0

my_zone.y = 0
my_zone.h = 7501
my_zone.L = 8000

my_goal_zone.y = 1750
my_goal_zone.h = 4000
my_goal_zone.L = 3000

en_zone.y = 0
en_zone.h = 7501
en_zone.L = 8000

en_goal_zone.y = 1750
en_goal_zone.h = 4000
en_goal_zone.L = 3000

en_close_zone.y = 0
en_close_zone.h = 7500
en_close_zone.L = 3000

MANA_USE = 40

def Sqr(a):
	return a*a

def Distance(x1,y1,x2,y2):
	return sqrt(Sqr(y2-y1)+Sqr(x2-x1))

def Print_wizard(wizard):
	print("wizard id =", wizard["id"], file=sys.stderr)
	print(" x = ", wizard["x"], file=sys.stderr)
	print(" y = ", wizard["y"], file=sys.stderr)
	print(" vx = ",wizard["vx"], file=sys.stderr)
	print(" vy =", wizard["vy"], file=sys.stderr)
	print(" state =", wizard["state"], file=sys.stderr)
def Print_snaffle(snaffle):
	print("snaffle id =", snaffle["id"], file=sys.stderr)
	print(" x = ", snaffle["x"], file=sys.stderr)
	print(" y = ", snaffle["y"], file=sys.stderr)
	print(" vx = ",snaffle["vx"], file=sys.stderr)
	print(" vy =", snaffle["vy"], file=sys.stderr)
	print(" state =", snaffle["state"], file=sys.stderr)

#renvoi le binaire du wizard le plus proche de snaffle 
def nearest(wizard_list, snaffle):
	i = 0
	dist=[0, 0]
	for wizard in wizard_list:
		dist[i] = Distance(wizard["x"], wizard["y"], snaffle["x"], snaffle["y"])
		i+=1
	if dist[0] < dist[1]:
		return 0
	else:
		return 1

#renvoi le snaffle le plus proche qui n'est pas déja visé
def closest_snaffle(snaffle_list, wizard, wizard_list):
	for snaffle in snaffle_list:
		if snaffle["state"] == 0 and ((target_id[(wizard["id"] + 1)% 2] != snaffle["id"] or wizard["id"] == nearest(wizard_list, snaffle) ) or len(snaffle_list) == 1):
					return snaffle

#renvoi le snaffle le plus proche des goals ennemies
def	get_near_from_goal(snaffle_list, wizard, gx, gy):
	for snaffle in snaffle_list:
		snaffle["dist"] = Distance(snaffle["x"], snaffle["y"], gx, gy)
	snaffle_list = sorted(snaffle_list, key=lambda snaffle: snaffle["dist"])
	nearest = closest_snaffle(snaffle_list, wizard, wizard_list)
	return nearest

def get_nb_snuffle_in_danger(snaffle_list):
	cnt = 0
	for snaffle in snaffle_list:
		if my_goal_zone.is_in(snaffle["x"], snaffle["y"]) == 1:
			cnt+=1
	return cnt

def in_my_direction(wizard, ennemie):
	A = 0
	B = 0
	if (ennemie["x"] - wizard["x"] < 0 and wizard["vx"] < 0) or (ennemie["x"] - wizard["x"] > 0 and wizard["vx"] > 0):
		A = 1
	if (ennemie["y"] - wizard["y"] < 0 and wizard["vy"] < 0) or (ennemie["y"] - wizard["y"] > 0 and wizard["vy"] > 0):
		B = 1
	print("A=", A, "B=", B, file=sys.stderr)
	if A == 1 and B == 1:
		return 1
	else:
		return 0

def check_in_front(wizard, bx, by, ennemie, rayon):
	m = (by - wizard["x"]) / (bx - wizard["y"])
	b = wizard["x"] - (m * wizard["y"])
	#carre = 1 + m^2
	carre = 1 + Sqr(m)
	#x = (-2*cx) - 2*m*(cy-b)
	x = (-2*ennemie["x"]) - 2*m*(ennemie["y"]-b)
	# cst = cx^2 + (cy - b)^2 - rayon^2
	cst = Sqr(ennemie["x"]) + Sqr(ennemie["y"] - b) - Sqr(rayon)
	#delta = c^2 - 4*carre*cst
	delta = Sqr(x) - 4*carre*cst
	print("DELTA =", delta, file=sys.stderr)
	if delta >= 0 and in_my_direction(wizard, ennemie):
		print("ENNEMI en face", file=sys.stderr)
		return 1
	else:
		print("pas d'ennemie en face", file=sys.stderr)
		return 0

def add_angle(gx, gy):
	new_angle = []
	PHI = math.radians(20)
	new_angle.append(gx*cos(PHI) - gy*sin(PHI))
	new_angle.append(gx*sin(PHI) + gy*cos(PHI))
	return new_angle

def throw_ball(wizard, gx, gy, power, opponent_list):
	ennemi_bludger = opponent_list + bludger_list
	for opponent in ennemi_bludger:
		print("for id =", opponent["id"], file=sys.stderr)
		print("gx = ", gx, "gy=", gy, file=sys.stderr)
		if en_close_zone.is_in(wizard["x"], wizard["y"]) == 0:
			# if check_in_front(wizard["x"], wizard["y"], gx, gy, opponent["x"], opponent["y"], 600) == 1:
			# 	power == 100
			while check_in_front(wizard, gx, gy, opponent, 600) == 1 and opponent["dist"] < 3000:
				new_angle = add_angle(gx, gy)
				gx = new_angle[0]
				gy = new_angle[1]
				power = 100
		
	print("THROW", int(gx), int(gy), power)
	d_g = Distance(wizard["x"], wizard["y"], gx, gy)
	print("Debug THROW", int(gx), int(gy), power,file=sys.stderr)
	print("Debug distance GOAL = ", d_g, file=sys.stderr)
	print("Debug goal_ennemy_x=",	gx, file=sys.stderr)
	target_id[wizard["id"] % 2] = 0

def goto_closest(snaffle_list, wizard):
	closest = closest_snaffle(snaffle_list, wizard, wizard_list)
	print("goto closest= ", closest, file=sys.stderr)
	if closest is not None:
		print("Debug wizard:", wizard["id"], "chasse c:", closest["id"], file=sys.stderr)
		print("MOVE", closest["x"], closest["y"], "150")
		#set target_id
		target_id[wizard["id"] % 2] = closest["id"]
	else:
		goto_center(150)
def goto_center(power):
	print("MOVE", 8000, 3750, power)

def nearest_wizard_from(wizard_list, gx, gy):
	distT = 0
	for wizard in wizard_list:
		distW = Distance(wizard["x"], wizard["y"], gx, gy)
		if distW < distT or distT == 0:
			distT = distW 
			near = wizard
	return near["id"]
def bludger_is_targeting_me(bludger_list, wizard):
	for bludger in bludger_list:
		if bludger["state"] != wizard["id"] and bludger["dist"] < 3000:
			#vy*Wx - vy*Bx - vx*Wy + vx*By == 0 eq droite
			print("EQU ==", (bludger["vy"] * wizard["x"]) - (bludger["vy"] * bludger["x"]) - (bludger["vx"] * wizard["y"]) + (bludger["vx"]*bludger["y"]), file=sys.stderr)
			Mx = 1
			tmp = (bludger["vy"] * Mx) - (bludger["vy"] * bludger["x"]) + (bludger["vx"]*bludger["y"])
			# tmp == bludger["vx"] * My:
			if bludger["vx"] != 0:
				My = tmp / bludger["vx"]
				if check_in_front(bludger, Mx, My, wizard, 600) == 1:
					print("BLUDGER is targeting ", wizard["id"], file=sys.stderr)
					return 1
	return 0
# game loop
while True:
	my_score, my_magic = [int(i) for i in input().split()]
	opponent_score, opponent_magic = [int(i) for i in input().split()]
	entities = int(input())  # number of entities still in game
	wizard_list = []
	snaffle_list = []
	bludger_list = []
	opponent_list = []
	#fill list
	for i in range(entities):
		# entity_id: entity identifier
		# entity_type: "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" or "BLUDGER"
		# x: position
		# y: position
		# vx: velocity
		# vy: velocity
		# state: 1 if the wizard is holding a Snaffle, 0 otherwise. 1 if the Snaffle is being held, 0 otherwise. id of the last victim of the bludger.
		entity_id, entity_type, x, y, vx, vy, state = input().split()
		my_dict = {
		"id" : int(entity_id),
		"x" : int(x),
		"y" : int(y),
		"vx" : int(vx),
		"vy" : int(vy),
		"state" : int(state) }

		if entity_type == "WIZARD":
			wizard_list.append(my_dict)
		elif entity_type == "SNAFFLE":
			snaffle_list.append(my_dict)	
		elif entity_type == "BLUDGER":
			bludger_list.append(my_dict)
		elif entity_type == "OPPONENT_WIZARD":
			opponent_list.append(my_dict)
#Pour chaque magicien
	for wizard in wizard_list:
	#trie les liste	du plus pres au plus loin du magicien
		for bludger in bludger_list:
			bludger["dist"] = Distance(bludger["x"], bludger["y"], wizard["x"], wizard["y"])
		bludger_list = sorted(bludger_list, key=lambda dist: dist["dist"])
		#snaffle list trié du plus pres du magcien au plus loin
		for snaffle in snaffle_list:
			snaffle["dist"] = Distance(snaffle["x"], snaffle["y"], wizard["x"], wizard["y"])
		snaffle_list = sorted(snaffle_list, key=lambda dist: dist["dist"])
		bad_bludger = bludger_is_targeting_me(bludger_list, wizard)
		# if bad_bludger is not None:
			# dodge_bludger(bad_bludger, wizard)
		if wizard["id"] == nearest_wizard_from(wizard_list, goal_allie_x, goal_allie_y) and get_nb_snuffle_in_danger(snaffle_list) > 0 and my_zone.is_in(wizard["x"], wizard["y"]) == 1:
			wizard["mode"] = "AT"
		else:
			wizard["mode"] = "AT"
		#mode DEF si snaffle dans close_zone_allie
		#si ennemi grab ball: wingardium
		#!Eviter les grosse baballe
		#! en defence si ennemie dans trajectoire, changer de trajectoires
		#! tester en boucle pour chaque trajectoire si ennemie et prendre en compte la distance
		# tester si bludger dans trajectoire ET ennemie
		#  Diviser les cages en deux
		#faire trois wrapper pour chaque commande et se baser dessus
		print("Debug wizard", wizard["id"], "mode:", wizard["mode"], file=sys.stderr)
		print("Debug wizard", wizard["id"], "state", wizard["state"], file=sys.stderr)
		print("Debug", target_id, file=sys.stderr)
		#esquive seulement quand tire snaffle ou quand bludger nous fonce dessus sinon aller en  directe
		# Write an action using print
		# To debug: print("Debug messages...", file=sys.stderr)
		# Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500, 0 ≤ magic ≤ 1500)
		# i.e.: "MOVE x y thrust" or "THROW x y power" or "WINGARDIUM id x y magic"
		
		# V1
		#if my_magic > 75:
		#near_al_goal = get_near_from_goal(snaffle_list, wizard, goal_allie_x, goal_allie_y)
		#print("WINGARDIUM", near_al_goal["id"], goal_ennemy_x, goal_ennemy_y, 75)
		
		#V2
		magic = 0
		if my_magic > 60:
			near_al_goal = get_near_from_goal(snaffle_list, wizard, goal_allie_x, goal_allie_y)
			near_en_goal = get_near_from_goal(snaffle_list, wizard, goal_ennemy_x, goal_ennemy_y)
			if near_en_goal is not None and near_en_goal["dist"] < 5000:
				print("WINGARDIUM", near_en_goal["id"], goal_ennemy_x, goal_ennemy_y, 35)
			elif near_al_goal is not None:
				vx = goal_ennemy_x
				vy = goal_ennemy_y
				for opponent in opponent_list:
					if check_in_front(near_al_goal, vx, vy, opponent, 400) == 1:
						vx = 8000
						vy = 0
				print("WINGARDIUM", near_al_goal["id"], vx, vy, 60)
				my_magic -= 60
				print("debug wizard", wizard["id"], "WIND to", near_al_goal["id"], file=sys.stderr)
				magic = 1
			else:
				goto_closest(snaffle_list, wizard)
		elif wizard["state"] == 1:
			throw_ball(wizard, goal_ennemy_x, goal_ennemy_y, 500, opponent_list)
		elif wizard["mode"] == "AT":
			if magic == 0:
				find = 0
				#si on est en zone ennemmie
				if en_zone.is_in(wizard["x"], wizard["y"]):
					print("Debug, wizard", wizard["id"], "en zone ENNEMIE", file=sys.stderr)
					snaffle = get_near_from_goal(snaffle_list, wizard, goal_ennemy_x, goal_ennemy_y)
					#Pour le snaffle le plus proche des cages_e
					print("Debug sclosest= ", snaffle, file=sys.stderr)
					if snaffle is not None and en_goal_zone.is_in(snaffle["x"], snaffle["y"]) and find == 0:
						#avant verifier si pas de snaffle jste a coté
						print("Debug CLOSE goto", snaffle["id"], file=sys.stderr)
						print("Debug wizard:", wizard["id"], "chasse sf:", snaffle["id"], file=sys.stderr)
						target_id[wizard["id"] % 2] = snaffle["id"]
						print("MOVE", snaffle["x"], snaffle["y"], "150")
						find = 1
				#si on ne vas pas marquer
				if find == 0:
					closest = closest_snaffle(snaffle_list, wizard, wizard_list)
					print("Debug closest= ", closest, file=sys.stderr)
					if closest is not None:
						print("Debug wizard:", wizard["id"], "chasse f0:", closest["id"], file=sys.stderr)
						print("MOVE", closest["x"], closest["y"], "150")
						#set target_id
						target_id[wizard["id"] % 2] = closest["id"]
					else:
						goto_center(150)
		else:
			#si mode DEF
			#si snaffle proche allie_goal AND me near allie_goal
			closest = get_near_from_goal(snaffle_list, wizard, goal_allie_x, goal_allie_y)
			if closest is not None and my_zone.is_in(wizard["x"], wizard["y"]) == 1:
				target_id[wizard["id"] % 2] = snaffle["id"]
				print("MOVE", closest["x"], closest["y"], "150")
				print("Debug wizard:", wizard["id"], "DEF", "chasse s:", closest["id"], file=sys.stderr)
			elif closest is not None:
				goto_closest(snaffle_list, wizard)
			else:
				goto_center(150)
