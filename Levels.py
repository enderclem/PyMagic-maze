import random
import os

# Contient le niveau et certaines variables

# Variable pour les boucles
menu_loop=True
playing_loop=False

# Variables des pions
pion_name = ("magicienne", "elfe", "nain", "barbare")
pion_pos = [(13, 9), (13, 11), (15, 9), (15, 11)]
# pion_pos = [(5, 3), (27, 3), (27, 17), (3, 17)]

# Variables des joueurs
nbr_of_player = 1
players_act = [] # Actions partagées entre les joueurs
# Contient la valeur des sélection d'action et de personnages.
selected_pion = [0] 
selected_act = [0] 

# Autres
actions = ("go_left", "go_right", "go_up", "go_down", "vortex", "escalator", "explore") # Toutes les actions disponibles
has_stolen=False
deactive_hourglass=[]
discussing=False
player_using_vortex=-1
selected_vortex=(1, 1)
escalator={}

# Matrice du niveau
level = [
    "...............................",
    ".#.#. . . . .#.#.#.#. . .H.#.#.",
    ".........§.....................",
    ".#.(.0.#. . .#.e. .#. . . .).#.",
    "...............................",
    ".#.#.#. . .#.#. .#.e. . . .#.#.",
    "...............................",
    ". . . . .#.#.$.€.#.#. . . .#.°.",
    "...§.§.§.......................",
    ". § . § . .0._._.°.#. . . .#. .",
    "...............................",
    ". § § § .#.o._._.O.e. . .#. . .",
    "...............................",
    ". § § § .#.#.£.@.#.#. . .#. .#.",
    "...............................",
    ". . § . § .#. .#.#. . . . . .#.",
    "...§.§.§.......................",
    ".#.]. . . .#. . . . . . . .[.#.",
    "...............................",
    ".#.#.H. . . . . . . . . . .#.#.",
    "..............................."
]
tiles_left = []

# Description de tout les symboles du niveau
meanings = {
    ".": "None", # Positions vides entre les cases
    "_": "None", # Juste pour mieux voir les persos sur les cases
    " ": "None",
    "#": "wall",
    "§": "wall", # Murs entre les cases
    "?": "unexplored",
    "c": "character",
    "$": "to steal magicienne",
    "£": "to steal elfe",
    "€": "to steal nain",
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
}

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


def share_actions(nbr_of_player):
    """
    Créer une liste contenant une liste d'actions disponible pour chaque joueur.
    En gros, partage les actions entre les joueurs.
    """
    global actions
    global players_act
    global selected_pion
    global selected_act

    to_distribute=list(actions)
    players_act=[[] for i in range(nbr_of_player)]

    while len(to_distribute)>=nbr_of_player:
        for i in range(nbr_of_player):
            random_act = to_distribute.pop(random.randint(0, len(to_distribute)-1))
            players_act[i].append(random_act)

    bonus=[i for i in range(nbr_of_player)] # Numéro des joueurs pouvant avoir une des actions restantes
    
    for act in to_distribute:
        p_gain=bonus.pop(random.randint(0, len(bonus)-1))
        players_act[p_gain].append(act)

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
                        if meanings[level[y+i][x+j]]=="escalator":
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
    for i in range(4):
        text+=pion_name[i]+" position="+str(pion_pos[i][0])+","+str(pion_pos[i][1])+"\n"
    # Sauvegarde du nombre de joueurs
    text+="nbr of player="+str(nbr_of_player)+"\n"
    # Sauvegarde des actions des joueurs
    for i in range(nbr_of_player):
        text+="J"+str(i)+" actions="
        for j in range(len(players_act[i])):
            text+=","*(j!=0)+players_act[i][j]
        text+="\n"
    # Sauvegarde de la variable has_stolen
    text+="has stolen="+str(int(has_stolen))+"\n"
    # Sauvegarde du niveau
    text+="\nlevel=\n"
    for line in level:
        text+=line+"\n"

    save=open("save.save", "w")
    save.write(text)
    save.close()


def load_game():
    """
    Charge le jeu et retourne le timer.
    """
    global pion_pos, nbr_of_player, players_act, has_stolen

    save=open("save.save", 'r')
    # Chargement du timer
    timer=float(save.readline().split('=')[1])
    # Chargement des positions des pions
    pos=[]
    for i in range(4):
        value=save.readline().split('=')[1].split(',')
        pos.append((int(value[0]), int(value[1])))
    pion_pos=pos
    # Chargement du nbr de joueur
    nbr_of_player=int(save.readline().split('=')[1])
    # Chargement des actions des joueurs
    players_act=[]
    for i in range(nbr_of_player):
        values=save.readline().split('=')[1].split(',')
        players_act.append([val.replace("\n", "") for val in values])
    # Chargement du booleen has_stolen
    has_stolen=bool(int(save.readline().split('=')[1]))

    level_add_escalators()
    return timer


def load_new_level(width, height):
    """
    Charge le niveau à partir des fichier
    """
    global level
    global tiles_left
    global pion_pos

    level=[]
    for y in range(height):
        level.append(["?" for i in range(width*2+1)])
        level.append(["?" for i in range(width*2+1)])
    level.append(["?" for i in range(width*2+1)])

    pos_tile=((width-1)//2*2-2, (height-1)//2*2-2)
    print("pos_tile", pos_tile)

    # Positionement des pions
    pion_pos=[(pos_tile[0]+x*2+3, pos_tile[1]+y*2+3) for x in range(2) for y in range(2)]

    # Chargement de la tuile de départ
    start_tile=load_tiles("tiles/start.tile")[0]
    print("start_tile", start_tile)
    for y in range(9):
        for x in range(9):
            level[pos_tile[1]+y][pos_tile[0]+x]=start_tile[y][x]

    # Chargement des tuiles piochables
    tiles_left=load_tiles("tiles/classic.tile")

    level_add_escalators()
    share_actions(nbr_of_player)

    print("DEBUT DE LA GAME")


def add_tile(pos_x, pos_y):
    global tiles_left
    global level
    global meanings
    
    if len(tiles_left)>0:
        tile=tiles_left.pop(random.randrange(0, len(tiles_left)))
    else:
        print("Erreur : Il n'y a plus de tuile restantes !")
        return None
        
    for y in range(9):
        for x in range(9):
            if not (meanings[level[pos_y+y][pos_x+x]]=="wall" and tile[y][x]=="None"):
                level[pos_y+y][pos_x+x]=tile[y][x]

    for y in range(9):
        for x in range(9):
            if "explore " in meanings[level[pos_y+y][pos_x+x]]:
                can_explore=False
                for d in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                    if 0<=pos_y+y+d[1]<len(level) and 0<=pos_x+x+d[0]<len(level[0]):
                        if "explore " in meanings[level[pos_y+y+d[1]][pos_x+x+d[0]]]:
                            level[pos_y+y+d[1]][pos_x+x+d[0]]=" "
                        if meanings[level[pos_y+y+d[1]][pos_x+x+d[0]]]=="unexplored":
                            can_explore=True
                            break
                if not can_explore:
                    level[pos_y+y][pos_x+x]=" "



    level_add_escalators()


def load_tiles(path):
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
