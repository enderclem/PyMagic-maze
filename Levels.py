import random
import os

# Contient le niveau et certaines variables

# Variable pour les boucles
menu_loop=True
playing_loop=False

# Variables des pions
pion_name = ["magicienne", "elfe", "nain", "barbare"]
pion_pos = [(13, 9), (13, 11), (15, 9), (15, 11)]
# pion_pos = [(5, 3), (27, 3), (27, 17), (3, 17)]

# Variables des joueurs
nbr_of_player = 1
players_act = [] # Actions partagées entre les joueurs
# Contient la valeur des sélection d'action et de personnages.
selected_pion = [0] 
selected_act = [0] 

# Gardes
nbr_guards=0

# Vortex
player_using_vortex=-1
selected_vortex=(1, 1)

# Sorts magiques
spells_all=("spell_balai", "spell_echange", "spell_teleportation", "spell_fantome", "spell_grenouille", "spell_invisibilite", "spell_appat")
nbr_spells=2
player_using_spell=-1
spell_being_used=None
selected_spell_target=None
move_pion=[]
eating=None
invisible=False
ghost_mod=False

# Autres
actions = ("go_left", "go_right", "go_up", "go_down", "vortex", "escalator", "explore") # Toutes les actions disponibles
has_stolen=False
deactive_hourglass=[]
discussing=False
escalator={}
reason_stop="quit"

# Matrice du niveau
level = []
tiles_left = []
tiles_pos = dict()
tiles_nbr = 0

# Description de tout les symboles du niveau
meanings = {
    ".": "None",
    "_": "None",
    " ": "None",
    "#": "wall",
    "§": "wall",
    "?": "unexplored",
    "c": "character",
    "$": "to steal magicienne",
    "£": "to steal elfe",
    "M": "to steal nain",
    "@": "to steal barbare",
    "(": "exit magicienne",
    ")": "exit elfe",
    "[": "exit nain",
    "]": "exit barbare",
    "H": "flip hourglass",
    "0": "vortex magicienne",
    "o": "vortex elfe",
    "°": "vortex nain",
    "O": "vortex barbare",
    "e": "escalator",
    "E": "explore magicienne",
    "S": "explore elfe",
    "s": "explore nain",
    "&": "explore barbare",
    "G": "guard",
    "R": "reinforcement unactivated",
    "r": "reinforcement activated",
    "T": "McTrollald",
}

meanings_reverse={meanings[m]: m for m in meanings.keys()}

# Les touches pour les différents controles en jeu, par joueur
controller = [{
    "w":"do action",
    "a":"select player -1",
    "q":"select player +1",
    "z":"select action -1",
    "s":"select action +1"
},{
    "b":"do action",
    "t":"select player -1",
    "g":"select player +1",
    "y":"select action -1",
    "h":"select action +1"
},{
    "colon":"do action",
    "o":"select player -1",
    "l":"select player +1",
    "p":"select action -1",
    "m":"select action +1"
},{
    "2":"do action",
    "8":"select player -1",
    "5":"select player +1",
    "9":"select action -1",
    "6":"select action +1"
}]


def add_guards():
    global level, nbr_guards, pion_pos, pion_name, meanings
    for y in range(len(level)):
        for x in range(len(level[y])):
            if meanings[level[y][x]]=="guard" \
            or (meanings[level[y][x]]=="reinforcement unactivated" and has_stolen):
                pion_pos.append((x, y))
                pion_name.append("garde_"+str(nbr_guards))
                level[y][x]=meanings_reverse["reinforcement activated"]
                nbr_guards+=1


def add_tile(pos_x, pos_y, rotate=0):
    global tiles_left,  tiles_pos, tiles_nbr
    global level, meanings
    
    tile=None
    if len(tiles_left)>0:
        tile=tiles_left.pop(random.randrange(0, len(tiles_left)))
        for line in tile:
            print(line)
    else:
        print("Erreur : Il n'y a plus de tuile restantes !")
        return None
        
    for i in range(rotate):
        rotated=[]
        for y in range(9):
            rotated.append([])
            for x in range(9):

                """print("\nrotated :")
                for l in rotated:
                    print(l)
                print("\ntile :")
                for l in tile:
                    print(l)"""
                
                rotated[-1].append(tile[8-x][y])
        tile=rotated

    for y in range(9):
        for x in range(9):
            if not (meanings[level[pos_y+y][pos_x+x]]=="wall" and tile[y][x]=="None"):
                # Ajout de la case
                level[pos_y+y][pos_x+x]=tile[y][x]
                tiles_pos[(pos_x+x, pos_y+y)]=tiles_nbr

                # Ajout des gardes
                add_guards()
    tiles_nbr+=1

    # Suppression des cases explorer inutiles
    for y in range(9):
        for x in range(9):
            # Si la case est une case explorer
            if "explore " in meanings[level[pos_y+y][pos_x+x]] and explore_info((pos_x+x, pos_y+y)) is None:
                level[pos_y+y][pos_x+x]=" "

    level_add_escalators()


def explore_info(case_pos):
    """
    Retourne la position et la rotation, ou None si le case n'est pas explorable.
    """
    global level, meanings

    case=level[case_pos[1]][case_pos[0]]
    case_mean=meanings[case]

    if "explore " in case_mean:
        can_explore=False
        # vérification que on peut explorer une tuile non exploré
        for d in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            if 0<=case_pos[1]+d[1]<len(level) and case_pos[0]+d[0]<len(level[0]):
                if "explore " in meanings[level[case_pos[1]+d[1]][case_pos[0]+d[0]]]:
                    level[case_pos[1]+d[1]][case_pos[0]+d[0]]=" "
                if meanings[level[case_pos[1]+d[1]][case_pos[0]+d[0]]]=="unexplored":
                    can_explore=True
                    break

        if can_explore:
            case_around={"x": {-1: meanings[level[case_pos[1]][case_pos[0]-2]],
                               1: meanings[level[case_pos[1]][case_pos[0]+2]]}, 
                        "y": {-1: meanings[level[case_pos[1]-2][case_pos[0]]],
                               1: meanings[level[case_pos[1]+2][case_pos[0]]]}}

            # Calcul de la position de la tuile à poser
            tile_pos_x=case_pos[0] \
                      +(case_around["x"][-1]=="unexplored")*-9 \
                      +(case_around["x"][1] =="unexplored")*1 \
                      +(case_around["y"][-1]=="unexplored")*-3 \
                      +(case_around["y"][1] =="unexplored")*-5
            tile_pos_y=case_pos[1] \
                      +(case_around["x"][-1]=="unexplored")*-5 \
                      +(case_around["x"][1] =="unexplored")*-3 \
                      +(case_around["y"][-1]=="unexplored")*-9 \
                      +(case_around["y"][1] =="unexplored")*1
            # verifier si la tuile sort du terrain
            if 0<=tile_pos_x<=len(level[0])-9 and 0<=tile_pos_y<=len(level)-9:
                rotation=(case_around["x"][-1]=="unexplored")*3 \
                        +(case_around["x"][1] =="unexplored") \
                        +(case_around["y"][1] =="unexplored")*2
                return ((tile_pos_x, tile_pos_y), rotation)

    return None


def get_index_pion_pos(pos):
    global pion_pos, pion_name
    for i in range(len(pion_pos)):
        if pion_pos[i]==pos and "grenouille" not in pion_name[i]:
            return i


def share_actions(nbr_of_player):
    """
    Créer une liste contenant une liste d'actions disponible pour chaque joueur.
    En gros, partage les actions entre les joueurs.
    """
    global actions
    global players_act
    global selected_pion
    global selected_act
    global spells_all, nbr_spells

    # distribution des actions pour chaque joueur
    to_distribute=list(actions)
    players_act=[[] for i in range(nbr_of_player)]

    while len(to_distribute)>=nbr_of_player:
        for i in range(nbr_of_player):
            random_act = to_distribute.pop(random.randint(0, len(to_distribute)-1))
            players_act[i].append(random_act)
    
    bonus=[i for i in range(nbr_of_player)] # Numéro des joueurs pouvant avoir une des actions restantes
    
    # distribution des actions en trop
    for act in to_distribute:
        p_gain=bonus.pop(random.randint(0, len(bonus)-1))
        players_act[p_gain].append(act)

    # Distribution des sorts
    to_distribute=list(spells_all)
    for i in range(nbr_spells):
        random_spell = to_distribute.pop(random.randint(0, len(to_distribute)-1))
        for j in range(len(players_act)):
            players_act[j].append(random_spell)
    """for random_spell in ("spell_fantome", "spell_invisibilite"):
        for j in range(len(players_act)):
            players_act[j].append(random_spell)"""

    # Initialisation des sélecteurs d'actions/pions
    selected_pion=[0 for i in range(nbr_of_player)]
    selected_act=[0 for i in range(nbr_of_player)]


def level_add_escalators():
    """
    Ajoute les positions des escalator par pair pour les calculs.
    """
    global escalator, level, meanings

    for y in range(len(level)):
        for x in range(len(level[y])):
            if meanings[level[y][x]]=="escalator" and (x,y) not in escalator.keys():
                for i in range(0, 5, 2):
                    for j in range(-4*(i!=0) + 2*(i==0), 5, 2):
                        if 0<=y+i<len(level) and 0<=x+j<len(level[0]) \
                        and meanings[level[y+i][x+j]]=="escalator" and tiles_pos[(x+j, y+i)]==tiles_pos[(x, y)]:
                            escalator[(x, y)]=(x+j, y+i)
                            escalator[(x+j, y+i)]=(x, y)


def save_game(timer):
    """
    Sauvegarde le jeu.
    """
    text=""
    # Sauvegarde du timer
    text+="timer="+str(timer)+"\n"
    # Sauvegarde des positions des pions
    text+="nbr of pion="+str(len(pion_pos))+"\n"
    for i in range(len(pion_pos)):
        text+=pion_name[i]+" position="+str(pion_pos[i][0])+","+str(pion_pos[i][1])+"\n"
    # Sauvegarde du nombre de joueurs
    text+="nbr of player="+str(nbr_of_player)+"\n"
    # Sauvegarde du nombre de gardes
    text+="nbr of guards="+str(nbr_guards)+"\n"
    # Sauvegarde des actions des joueurs
    for i in range(nbr_of_player):
        text+="J"+str(i)+" actions="
        for j in range(len(players_act[i])):
            text+=","*(j!=0)+players_act[i][j]
        text+="\n"
    # Sauvegarde de la variable has_stolen
    text+="has stolen="+str(int(has_stolen))+"\n"
    # Sauvegarde les cases sabliers déjà utilisées
    line="deactivated hourglass="
    if deactive_hourglass==[]:
        line+="None\n"
    else:
        for elem in deactive_hourglass:
            line+=str(elem[0])+","+str(elem[1])+"|"
        line=line[:-1]+"\n"
    text+=line

    with open("save/save.save", "w") as save:
        save.write(text)

    # Sauvegarde du niveau
    save_tiles("save/level.tile", [level])

    # Sauvegarde des tuiles piochables
    save_tiles("save/tiles.tile", tiles_left)

    # Sauvegarde des position des tuiles
    text="tiles nbr="+str(tiles_nbr)+"\n"
    for pos in tiles_pos.keys():
        print(str(pos[0])+","+str(pos[1])+":"+str(tiles_pos[pos])+"\n")
        text += str(pos[0])+","+str(pos[1])+":"+str(tiles_pos[pos])+"\n"
    with open("save/tiles_pos.save", "w") as file:
        file.write(text)


def load_game():
    """
    Charge la sauvegarde du jeu et retourne le timer.
    """
    global pion_pos, nbr_of_player, players_act, has_stolen, pion_name, level, tiles_pos, tiles_nbr, nbr_guards, deactive_hourglass

    with open("save/save.save", 'r') as save:
        # Chargement du timer
        timer=float(save.readline().split('=')[1])
        # Chargement des positions des pions et de leurs nom
        pion_pos=[]
        pion_name=[]
        nbr_pion=int(save.readline().split('=')[1])
        for i in range(nbr_pion):
            line=save.readline().split('=')
            pion_name.append(line[0].replace(" position", ""))
            value=line[1].split(',')
            pion_pos.append((int(value[0]), int(value[1])))
        # Chargement du nbr de joueur
        nbr_of_player=int(save.readline().split('=')[1])
        # Sauvegarde du nombre de gardes
        nbr_guards=int(save.readline().split('=')[1])
        # Chargement des actions des joueurs
        players_act=[]
        for i in range(nbr_of_player):
            values=save.readline().split('=')[1].split(',')
            players_act.append([val.replace("\n", "") for val in values])
        # Chargement du booleen has_stolen
        has_stolen=bool(int(save.readline().split('=')[1]))
        # Chargement de deactive_hourglass
        line=save.readline().replace("deactivated hourglass=", "").strip().split('|')
        if line[0]!="None":
            for elem in line:
                elem=elem.split(",")
                deactive_hourglass.append((int(elem[0]), int(elem[1])))


    # Chargement du niveau
    lvl_tile=load_tiles("save/level.tile")[0]
    level=[]
    for line in lvl_tile:
        level.append([c for c in line])

    # Chargement des positions des tuiles
    with open("save/tiles_pos.save", "r") as save:
        tiles_nbr=int(save.readline().strip().split("=")[1])
        for line in save.readlines():
            line=line.split(":")
            line[0]=line[0].split(",")
            tiles_pos[(int(line[0][0]), int(line[0][1]))]=int(line[1])

    # Chargement des escalators
    level_add_escalators()
    # Chargement des tuiles piochables
    tiles_left=load_tiles("save/tiles.tile")

    return timer


def load_new_level(width, height):
    """
    Charge le niveau à partir des fichier
    """
    global level
    global tiles_left
    global pion_pos
    global tiles_pos, tiles_nbr

    level=[]
    for y in range(height):
        level.append(["?" for i in range(width*2+1)])
        level.append(["?" for i in range(width*2+1)])
    level.append(["?" for i in range(width*2+1)])

    pos_tile=((width-1)//2*2-2, (height-1)//2*2-2)

    # Positionement des pions
    pion_pos=[(pos_tile[0]+x*2+3, pos_tile[1]+y*2+3) for x in range(2) for y in range(2)]

    # Chargement de la tuile de départ
    start_tile=load_tiles("tiles/start.tile")[0]
    for y in range(9):
        for x in range(9):
            level[pos_tile[1]+y][pos_tile[0]+x]=start_tile[y][x]
            tiles_pos[(pos_tile[0]+x, pos_tile[1]+y)]=0
    tiles_nbr=1

    # Chargement des tuiles piochables
    tiles_left=load_tiles("tiles/classic.tile")

    level_add_escalators()
    share_actions(nbr_of_player)

    print("DEBUT DE LA PARTIE")


def load_tiles(path):
    """
    Retourne les tuiles du fichier indiqué.
    """
    with open(path, "r") as file:
        tiles=[[]]
        for line in file.readlines():
            if (line=="\n" or "/" in line) and tiles[-1]!=[]:
                tiles.append([])
            elif not (line=="\n" or "/" in line):
                tiles[-1].append(line.strip().replace("Â", ""))

        if [] in tiles:
            tiles.remove([])
        return tiles


def save_tiles(path, tiles):
    """
    Sauvegarde les tuiles dans le fichier indiqué.
    """
    text=""
    for tile in tiles:
        for line in tile:
            text += "".join(line)+"\n"
        text+="\n"

    with open(path, "w") as file:
        file.write(text)

