import sys
import math
from operator import itemgetter
from copy import deepcopy

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories


#retourner id plutot que dico
def get_near_link(base_id, mineList, excludeMe=0):
    print("gnl base_id", base_id, file=sys.stderr)
    available = []
    for link in link_list:
        link["case"] = 0
        if link["fact1"] == base_id:
            link["case"] = 1
        elif link["fact2"] == base_id:
            link["case"] = 2
        #si j'apparait dans un des deux
        if link["case"] > 0:
            available.append(link)
    #trie les liens ou ma base apparait du plus proche au plus loin
    available.sort(key=itemgetter("distance")) # a optimiser
    i = 0    
    if excludeMe == 0:
        #renvoi le premier
        print("gnl return", available[i], file=sys.stderr)
        return (available[i])
    else:
        #exclue les base m'appartenant des link renvoyé
        tmp = i
        while tmp == i and i < len(available) - 1:
            #tant qu'il y a deux bases a moi et que ce n'est pas le dernier lien
            tmp +=1
            if link["case"] == 1:
                if mineList.count(available[i]["fact1"]) == 1:
                    i+=1
            else:
                if mineList.count(available[i]["fact2"]) == 1:
                    i+=1
            if i == len(available):

        print("gnl return", available[0], file=sys.stderr)
        return (available[i])




#init_link_list
my_dict = {}
link_list = []
for i in range(link_count):
    my_dict = {}
    my_dict["fact1"], my_dict["fact2"], my_dict["distance"] = [int(j) for j in input().split()]
    link_list.append(my_dict)
    print("link:", my_dict, file=sys.stderr)

# game loop
while True:
    print("WAIT")
    my_bases = []
    entity_count = int(input())  # the number of entities (e.g. factories and troops)
    print("entity_count", entity_count, file=sys.stderr)
    
    for i in range(entity_count):
        my_dict = {}
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
        my_dict["id"] = int(entity_id)
        my_dict["arg1"] = int(arg_1)
        my_dict["arg2"] = int(arg_2)
        my_dict["arg3"] = int(arg_3)
        my_dict["arg4"] = int(arg_4)
        my_dict["arg5"] = int(arg_5)
        if entity_type == "FACTORY":
            if my_dict["arg1"] == 1:
                my_bases.append(my_dict)


    print("MY_FACTORYES", file=sys.stderr)
    mineList = []
    for base in my_bases:
        mineList.append(base["id"])
    for base in my_bases:
        print(base , file=sys.stderr)
        near_link = get_near_link(base["id"], 1)
        print(near_link, file=sys.stderr)
        if near_link["fact1"] == base["id"]:
            print("MOVE", base["id"], near_link["fact2"], 10)
        else:
            print("MOVE", base["id"], near_link["fact1"], 10)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    
    # Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
    # print("WAIT")

# print("", file=sys.stderr)
#idees
# 1- parcourir les bases m'appartenant : DONE
# 2- Si ma base a plus de (? nb_total)
# 3- une base doit attendre d'avoir >x cyborg avant de jouer sauf si elle n'en produit pas
# 4- soit une base est inferieur a 5 et on l'alimente soit on n'envoie pas de bonhomme sur une de nos propres bases