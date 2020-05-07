import sys
import math
from math import sqrt

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle to grab it and use your team id to determine towards where you need to throw it.
# Use the Wingardium spell to move things around at your leisure, the more magic you put it, the further they'll move.

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
target_id = {0 : 0, 1 : 0}

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
close_my_zone = rectangle()
ennemy_zone = rectangle()
close_ennemy_zone = rectangle()

if my_team_id == 0:
	my_zone.x = 0
	close_my_zone.x = 0
	ennemy_zone.x = 8000
	close_ennemy_zone.x = 13000
else:
	my_zone.x = 8000
	close_my_zone.x = 13000
	ennemy_zone.x = 0
	close_ennemy_zone.x = 0

my_zone.y = 0
my_zone.h = 7501
my_zone.L = 8000

close_my_zone.y = 1750
close_my_zone.h = 4000
close_my_zone.L = 3000

ennemy_zone.y = 0
ennemy_zone.h = 7501
ennemy_zone.L = 8000
close_ennemy_zone.y = 1750
close_ennemy_zone.h = 4000
close_ennemy_zone.L = 3000

def Sqr(a):
	return a*a

def Distance(x1,y1,x2,y2):
	return sqrt(Sqr(y2-y1)+Sqr(x2-x1))

def Print_wizard(wizard):
	print("Debug wizard id =", wizard["id"], file=sys.stderr)
	print("Debug x = ", wizard["x"], file=sys.stderr)
	print("Debug y = ", wizard["y"], file=sys.stderr)
	print("Debug vx = ",wizard["vx"], file=sys.stderr)
	print("Debug vy =", wizard["vy"], file=sys.stderr)
	print("Debug state =", wizard["state"], file=sys.stderr)

def Print_snaffle(snaffle):
	print("Debug snaffle id =", snaffle["id"], file=sys.stderr)
	print("Debug x = ", snaffle["x"], file=sys.stderr)
	print("Debug y = ", snaffle["y"], file=sys.stderr)
	print("Debug vx = ",snaffle["vx"], file=sys.stderr)
	print("Debug vy =", snaffle["vy"], file=sys.stderr)
	print("Debug state =", snaffle["state"], file=sys.stderr)

#renvoi le snaffle le plus proche qui n'est pas déja visé
def closest_snaffle(snaffle_list, wizard):
	for snaffle in snaffle_list:
		if snaffle["state"] == 0 and target_id[(wizard["id"] + 1)% 2] != snaffle["id"]:
					return snaffle

#renvoi le snaffle le plus proche des goals ennemies
def get_near_from_goal(snaffle_list, wizard, gx, gy):
	for snaffle in snaffle_list:
		snaffle["dist"] = Distance(snaffle["x"], snaffle["y"], gx, gy)
	snaffle_list = sorted(snaffle_list, key=lambda snaffle: snaffle["dist"])
	nearest = closest_snaffle(snaffle_list, wizard)
	return nearest

def get_nb_snuffle_in_danger(snaffle_list):
	cnt = 0
	for snaffle in snaffle_list:
		if close_my_zone.is_in(snaffle["x"], snaffle["y"]) == 1:
			cnt+=1
	return cnt

def throw_ball(wizard, gx, gy, pow):
	print("THROW",	gx, gy, pow)
	d_g = Distance(wizard["x"], wizard["y"], gx, gy)
	print("Debug THROW", file=sys.stderr)
	print("Debug distance GOAL = ", d_g, file=sys.stderr)
	print("Debug goal_ennemy_x=",	gx, file=sys.stderr)
	target_id[wizard["id"] % 2] = 0

def goto_closest(snaffle_list, wizard):
	closest = closest_snaffle(snaffle_list, wizard)
	print("Debug closest= ", closest, file=sys.stderr)
	if closest is not None:
		print("Debug wizard:", wizard["id"], "chasse c:", closest["id"], file=sys.stderr)
		print("MOVE", closest["x"], closest["y"], "120")
		#set target_id
		target_id[wizard["id"] % 2] = snaffle["id"]
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
# game loop

while True:
	my_score, my_magic = [int(i) for i in input().split()]
	opponent_score, opponent_magic = [int(i) for i in input().split()]
	entities = int(input())  # number of entities still in game
	wizard_list = []
	snaffle_list = []
	bludger_list = []
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
#Pour chaque magicien
	print("Debug NB wiz alive = ", len(wizard_list), file=sys.stderr)
	for wizard in wizard_list:
		#mode attack mode defense
		touche = 0
		for bludger in bludger_list:
			if bludger["state"] == wizard["id"]:
				print("TOUCHE BLUGER", file=sys.stderr)
				touch = 1
		if wizard["id"] == nearest_wizard_from(wizard_list, goal_allie_x, goal_allie_y) and get_nb_snuffle_in_danger(snaffle_list) > 0:
			wizard["mode"] = "DEF"
		else:
			wizard["mode"] = "AT"
		#mode DEF si snaffle dans close_zone_allie
		#si ennemi grab ball: wingardium
		print("Debug wizard", wizard["id"], "mode:", wizard["mode"], file=sys.stderr)
		print("Debug wizard", wizard["id"], "state", wizard["state"], file=sys.stderr)
		print("Debug", target_id, file=sys.stderr)
		for snaffle in snaffle_list:
			snaffle["dist"] = Distance(snaffle["x"], snaffle["y"], wizard["x"], wizard["y"])
		snaffle_list = sorted(snaffle_list, key=lambda dist: dist["dist"])
		# Write an action using print
		# To debug: print("Debug messages...", file=sys.stderr)
		# Edit this line to indicate the action for each wizard (0 ≤ thrust ≤ 150, 0 ≤ power ≤ 500, 0 ≤ magic ≤ 1500)
		# i.e.: "MOVE x y thrust" or "THROW x y power" or "WINGARDIUM id x y magic"
		magic = 0
		if my_magic > 75:
			near_al_goal = get_near_from_goal(snaffle_list, wizard, goal_allie_x, goal_allie_y)
			if near_al_goal is not None:
				print("WINGARDIUM", near_al_goal["id"], goal_ennemy_x, goal_ennemy_y, 75)
				print("debug wizard", wizard["id"], "WIND to", near_al_goal["id"], file=sys.stderr)
				magic = 1
		if wizard["mode"] == "AT":
			if wizard["state"] == 1:
				#si mode ATK et porte un snaffle
				throw_ball(wizard, goal_ennemy_x, goal_ennemy_y, 500)
			elif magic == 0:
				find = 0
				#si on est en zone ennemmie
				if ennemy_zone.is_in(wizard["x"], wizard["y"]):
					print("Debug, wizard", wizard["id"], "en zone ENNEMIE", file=sys.stderr)
					snaffle = get_near_from_goal(snaffle_list, wizard, goal_ennemy_x, goal_ennemy_y)
					#Pour le snaffle le plus proche des cages_e
					print("Debug sclosest= ", snaffle, file=sys.stderr)
					if snaffle is not None and close_ennemy_zone.is_in(snaffle["x"], snaffle["y"]) and find == 0:
						#avant verifier si pas de snaffle jste a coté
						print("Debug CLOSE goto", snaffle["id"], file=sys.stderr)
						print("Debug wizard:", wizard["id"], "chasse sf:", snaffle["id"], file=sys.stderr)
						target_id[wizard["id"] % 2] = snaffle["id"]
						print("MOVE", snaffle["x"], snaffle["y"], "150")
						find = 1
				#si on ne vas pas marquer
				if find == 0:
					closest = closest_snaffle(snaffle_list, wizard)
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
			if wizard["state"] == 1:
				throw_ball(wizard, goal_ennemy_x, goal_ennemy_y, 500)
			else:
				if closest is not None and my_zone.is_in(wizard["x"], wizard["y"]) == 1:
					target_id[wizard["id"] % 2] = snaffle["id"]
					print("MOVE", closest["x"], closest["y"], "150")
					print("Debug wizard:", wizard["id"], "DEF", "chasse s:", closest["id"], file=sys.stderr)
				elif closest is not None:
					goto_closest(snaffle_list, wizard)
				else:
					goto_center(150)
