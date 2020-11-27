import random

# Contient le niveau et certaines variables

nbr_of_player = 1
pion_name = ("magicienne", "elfe", "nain", "barbare")
pion_pos = [(13, 9), (13, 11), (15, 9), (15, 11)]
max_time = 180.0
time_left = max_time
actions = ("go_left", "go_right", "go_up", "go_down")#, "vortex", "escalator", "explore") # Toutes les actions disponibles
players_act = [] # Actions partagées entre les joueurs
# Contient la valeur des sélection d'action et de personnages.
selected_pion = [0] 
selected_act = [0] 

# Matrice du niveau
level = [
    "...............................",
    ".#.#. . . . .#.#.#.#. . . .#.#.", 
    ".........§.....................",
    ".#.(. .#. . .#. . .#. . . .).#.", 
    "...............................",
    ".#.#.#. . .#.#. .#. . . . .#.#.", 
    "...............................",
    ". . . . .#.#.$.€.#.#. . . .#. .", 
    "...§.§.§.......................",
    ". § . § . . ._._. .#. . . .#. .", 
    "...............................",
    ". § § § .#. ._._. . . . .#. . .", 
    "...............................",
    ". § § § .#.#.£.@.#.#. . .#. .#.", 
    "...............................",
    ". . § . § .#. .#.#. . . . . .#.", 
    "...§.§.§.......................",
    ".#.]. . . .#. . . . . . . .[.#.", 
    "...............................",
    ".#.#. . . . . . . . . . . .#.#.", 
    "..............................."
]

# Description de tout les symboles du niveau
meanings = {
    ".": "None", # Positions vides entre les cases
    "_": "None", # Juste pour mieux voir les persos sur les cases
    " ": "None",
    "#": "wall",
    "§": "wall", # Murs entre les cases
    "c": "character",
    "$": "to steal magicienne",
    "£": "to steal elfe",
    "€": "to steal nain",
    "@": "to steal barbare",
    "(": "exit magicienne",
    ")": "exit elfe",
    "[": "exit nain",
    "]": "exit barbare",
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
    "semicolon":"do action",
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