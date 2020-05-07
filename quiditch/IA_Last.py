#IMPORT
import sys
import math
from math import sqrt
from math import cos
from math import sin

#CONSTANTES
MS_X        = 16000
HALF_MS_X   = MS_X / 2
MS_Y        = 7501
HALF_MS_Y   = MS_Y / 2
#CLASSC PART
class rectangle:
    "class rectangle"
    def __init__(self, x, y, L, h):
        self.x = x
        self.y = y
        self.L = L
        self.h = h
    
    def is_in(self, x, y):
        if x > self.x and x < self.x + self.L:
            if y > self.y and y < self.y + self.h:
                return 1
        return 0
class item:
    def __init__(self, id, x, y, vx, vy, state):
        self.id = id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.state = state
        self.dist = 0
        self.dist_goal = 0
        self.target_id = 0
class goal:
    #side:0ou1 si gauche ou droite
    def __init__(self, side):
        self.side = side
        self.y = 3500
        if side == 0:
            self.x = 0
        else:
            self.x = 16000
    def get_target(self, wizard):
        if wizard.y > HALF_MS_Y:
            target = [self.x, self.y + 500]
        else:
            target = [self.x, self.y - 500]
        return target
#INIT PART
my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
if my_team_id == 0:
    ennemy_team_id = 1
else:
    ennemy_team_id = 0
    #definition des rectangles
if my_team_id == 0:
    my_zone = rectangle(0, 0, HALF_MS_X, MS_Y)
    my_close_zone = rectangle(0, 0, 4000, MS_Y)
    my_goal_zone = rectangle(0, 1750, 4000, 4000)
    en_zone = rectangle(MS_X-HALF_MS_X, 0, HALF_MS_X, MS_Y)
    en_goal_zone = rectangle(MS_X-4000, 1750, 4000, 4000)
    en_close_zone = rectangle(MS_X-4500, 0, 4500, MS_Y)
else:
    en_zone = rectangle(0, 0, HALF_MS_X, MS_Y)
    en_close_zone = rectangle(0, 0, 4500, MS_Y)
    en_goal_zone = rectangle(0, 1750, 4000, 4000)
    my_zone = rectangle(MS_X-HALF_MS_X, 0, HALF_MS_X, MS_Y)
    my_goal_zone = rectangle(MS_X-4000, 1750, 4000, 4000)
    my_close_zone = rectangle(MS_X-4000, 0, 4000, MS_Y)

middle_column = rectangle(6000, 0, 4000, MS_Y)
my_goal = goal(my_team_id)
ennemy_goal = goal(ennemy_team_id)

#UTILS PART
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
def Print_snaffle_list_d(snaffle_list):
    print("snaffle_list:", file=sys.stderr)
    for snaffle in snaffle_list:
        print("  id=", snaffle.id, "dist=", snaffle.dist, file=sys.stderr)
def summon(id, gx, gy, magic, my_magic):
    print("WINGARDIUM", id, gx, gy, magic, file=sys.stderr)
    print("WINGARDIUM", id, gx, gy, magic)
    my_magic -= magic
def move_to(gx, gy, thrust):
    print("MOVE", int(gx), int(gy), thrust, file=sys.stderr)
    print("MOVE", int(gx), int(gy), thrust)
def check_in_front(wizard, bx, by, ennemie, rayon):
    m = (by - wizard.x) / (bx - wizard.y)
    b = wizard.x - (m * wizard.y)
    #carre = 1 + m^2
    carre = 1 + Sqr(m)
    #x = (-2*cx) - 2*m*(cy-b)
    x = (-2*ennemie.x) - 2*m*(ennemie.y-b)
    # cst = cx^2 + (cy - b)^2 - rayon^2
    cst = Sqr(ennemie.x) + Sqr(ennemie.y - b) - Sqr(rayon)
    #delta = x^2 - 4*carre*cst
    delta = Sqr(x) - 4*carre*cst
    print("DELTA =", delta, file=sys.stderr)
    if delta >= 0 and in_my_direction(wizard, ennemie, bx, by):
        print("ENNEMI", ennemie.id, "en face", file=sys.stderr)
        return 1
    else:
        print("pas d'ennemie en face", file=sys.stderr)
        return 0
def in_my_direction(wizard, ennemie, cibx, ciby):
    A = 0
    B = 0
    if (ennemie.x - wizard.x < 0 and cibx - wizard.x < 0) or (ennemie.x - wizard.x > 0 and cibx-wizard.x > 0):
        A = 1
    if (ennemie.y - wizard.y < 0 and ciby - wizard.y < 0) or (ennemie.y - wizard.y > 0 and ciby - wizard.y > 0):
        B = 1
    print("A=", A, "B=", B, file=sys.stderr)
    if A == 1 and B == 1:
        return 1
    else:
        return 0
def add_angle(gx, gy):
    new_angle = []
    PHI = math.radians(20)
    new_angle.append(gx*cos(PHI) - gy*sin(PHI))
    new_angle.append(gx*sin(PHI) + gy*cos(PHI))
    return new_angle
def get_other_wizard(wizard, wizard_list):
    wiz = wizard_list[0]
    if wiz.id != wizard.id:
        return wiz
    else:
        return wizard_list[1]
#FONCTIONS
def throw(gx, gy, power):
    print("THROW", int(gx), int(gy), power,file=sys.stderr)     
    print("THROW", int(gx), int(gy), power)
def nearest(wizard_list, snaffle):
    #renvoi l'ID du wizard le plus proche de snaffle 
    dist=[]
    for wizard in wizard_list:
        dist.append(Distance(wizard.x, wizard.y, snaffle.x, snaffle.y))
    if dist[0] < dist[1]:
        return wizard_list[0].id
    else:
        return wizard_list[1].id
def other_nearest_too(wizard, wizard_list, snaffle_list, nearest):
    sorted_list = list(snaffle_list)
    other = get_other_wizard(wizard, wizard_list)
    for snaffle in sorted_list:
        snaffle.dist = Distance(snaffle.x, snaffle.y, other.x, other.y)
    sorted_list.sort(key=lambda snaffle: snaffle.dist)
    print("my list", Print_snaffle_list_d(snaffle_list), file=sys.stderr)
    print("other_list", Print_snaffle_list_d(sorted_list), file=sys.stderr)
    if sorted_list[0].id == nearest.id:
        return 1
    else:
        return 0
def snaffle_left(wizard, snaffle_list):
    for snaffle in snaffle_list:
        if snaffle.x > wizard.x:
            return 1
    return 0
def other_id_is_busy(wizard, wizard_list, sn_id):
    print("A.5", file=sys.stderr)
    other = get_other_wizard(wizard, wizard_list)
    if other.target_id != sn_id:
        return 1
    return 0
def closest_snaffle(snaffle_list, wizard, wizard_list):
    #renvoi le snaffle le plus proche qui n'est pas déja visé
    for snaffle in snaffle_list:
        print(snaffle.id, "=state", snaffle.state, "nearest id =", nearest(wizard_list, snaffle), file=sys.stderr)
        if snaffle.state == 0:
            print("A", file=sys.stderr)
            if other_nearest_too(wizard, wizard_list, snaffle_list, snaffle) and other_id_is_busy(wizard, wizard_list, snaffle.id):
                print("B", file=sys.stderr)
                if wizard.id == nearest(wizard_list, snaffle):
                    print("C", file=sys.stderr)
                    if snaffle_left(wizard, snaffle_list) == 1:
                        print("SPECIAL is", snaffle.id, file=sys.stderr)
                        return snaffle
                    else:
                        wizard.target_id = 0
                else:
                    wizard.target_id = 0
            else:
                return snaffle
    print("closest not found", file=sys.stderr)
def get_near_from_goal(snaffle_list, wizard, goal):
    for snaffle in snaffle_list:
        snaffle.dist_goal = Distance(snaffle.x, snaffle.y, goal.x, goal.y)
    sorted_list = sorted(snaffle_list, key=lambda snaffle: snaffle.dist_goal)
    nearest = closest_snaffle(sorted_list, wizard, wizard_list)
    return nearest
def get_clean_trajectory(wizard, gx, gy, opponent_list):
    angle = [gx, gy]
    modif = 1
    while modif == 1:
        modif = 0
        for opponent in opponent_list:
            if check_in_front(wizard, angle[0], angle[1], opponent, 600):
                modif = 1
                angle = add_angle(angle[0], angle[1])
    return angle

def need_to_incant(snaffle_list, wizard, my_goal, ennemy_goal, my_magic):
    target = []
    closest = get_near_from_goal(snaffle_list, wizard, ennemy_goal)
    if closest is not None and closest.dist_goal < 5000 and my_magic > 20:
        target.append(closest.id)
        xy = ennemy_goal.get_target(closest)
        target.extend(xy)
        target.append(my_magic)
        return target
    elif closest is not None and middle_column.is_in(closest.x, closest.y) and my_magic > 40:
        target.append(closest.id)
        xy = ennemy_goal.get_target(closest)
        target.extend(xy)
        target.append(my_magic)
def need_to_throw(wizard):
    if wizard.state == 1:
        return 1
    else:
        return 0
def sort_liste(wizard, bludger_list, snaffle_list, opponent_list):
    for bludger in bludger_list:
        bludger.dist = Distance(bludger.x, bludger.y, wizard.x, wizard.y)
    for snaffle in snaffle_list:
        snaffle.dist = Distance(snaffle.x, snaffle.y, wizard.x, wizard.y)
    for opponent in opponent_list:
        opponent.dist = Distance(opponent.x, opponent.y, wizard.x, wizard.y)
    bludger_list.sort(key=lambda obj: obj.dist)
    snaffle_list.sort(key=lambda obj: obj.dist)
    opponent_list.sort(key=lambda obj: obj.dist)
def goto_center():
    move_to(HALF_MS_X, HALF_MS_Y, 150)
def goto_closest(snaffle_list, wizard, wizard_list):
    closest = closest_snaffle(snaffle_list, wizard, wizard_list)
    if closest is not None:
        print("goto closest: id=", closest.id, file=sys.stderr)
        print("Debug wizard:", wizard.id, "chasse c:", closest.id, file=sys.stderr)
        move_to(closest.x, closest.y, 150)
        #set target_id
        wizard.target_id= closest.id
        return 1
    else:
        return 0
def move(wizard, snaffle_list, wizard_list):
    if goto_closest(snaffle_list, wizard, wizard_list) == 0:
        goto_center()
def throw_ball(wizard, opponent_list):
    power = 500
    print("my team_id =", my_team_id, "en_close_zone =", en_close_zone, file=sys.stderr)
    if en_close_zone.is_in(wizard.x, wizard.y) or 1:
        print("is in en_close_zone", file=sys.stderr)
        #tirer vers cage
        target = ennemy_goal.get_target(wizard)
        gx = target[0]
        gy = target[1]
    else:
        #tirer vers en_close_zone
        print("not in en_close_zone", file=sys.stderr)
        gx = 16000
        gy = wizard.y
    #ici verifier si trajectoire libre
    print("old traj =", gx, gy, file=sys.stderr)
    trajectory = get_clean_trajectory(wizard, gx, gy, opponent_list)
    print("new traj =", trajectory[0], trajectory[1], file=sys.stderr)
    throw(trajectory[0], trajectory[1], power)
    wizard.target_id = 0
    # d_g = Distance(wizard["x"], wizard["y"], gx, gy)
    # print("Debug distance a la cible = ", d_g, file=sys.stderr)
    # print("Debug cible: x=", gx, "y=", gy, file=sys.stderr)


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
        my_item = item(int(entity_id), int(x), int(y), int(vx), int(vy), int(state))
        if entity_type == "WIZARD":
            wizard_list.append(my_item)
        elif entity_type == "SNAFFLE":
            snaffle_list.append(my_item)    
        elif entity_type == "BLUDGER":
            bludger_list.append(my_item)
        elif entity_type == "OPPONENT_WIZARD":
            opponent_list.append(my_item)
    len(snaffle_list)
#Pour chaque magicien
    for wizard in wizard_list:
        print("WIZ ID=", wizard.id, file=sys.stderr)
        #trie les liste du plus pres au plus loin du magicien
        sort_liste(wizard, bludger_list, snaffle_list, opponent_list)
    #   Print_snaffle_list_d(snaffle_list)
        target = need_to_incant(snaffle_list, wizard, my_goal, ennemy_goal, my_magic)
        # print("HERE, target = ", target, file=sys.stderr)
        if target is not None:
            summon(target[0], target[1], target[2], target[3], my_magic)
        elif need_to_throw(wizard) == 1:
            throw_ball(wizard, opponent_list)
        else:
    #       Print_snaffle_list_d(snaffle_list)
            move(wizard, snaffle_list, wizard_list)