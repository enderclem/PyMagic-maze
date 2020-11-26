# Contient le niveau et certaines variables

nbr_of_player = 1
players_name = ("magicienne", "elfe", "nain", "barbare")
players_pos = [(13, 9), (13, 11), (15, 9), (15, 11)]
max_time = 180.0
time_left = max_time
actions = ("left", "right", "up", "down")#, "vortex", "escalator", "explore") # Toutes les actions disponibles
players_act = [] # Actions partagées entre les joueurs

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


def share_actions(nbr_of_player):
    global actions
    to_distribute=tuple(actions)
    players_actions=[[] for i in range(nbr_of_player)]

    while len(actions)>=nbr_of_player:
        for i in range(nbr_of_player):
            random_act = to_distribute.pop(random.randint(0, len(to_distribute)-1))
            players_actions[i].append(random_act)

    bonus=[i for i in range(len(to_distribute))] # Numéro des joueurs pouvant avoir une des actions restantes
    for act in to_distribute:
        p_gain=bonus.pop(random.randint(0, len(bonus)-1))
        players_actions[p_gain].append(act)

    return players_actions