# Contient le niveau et certaines variables

players_name = ("magicienne", "elfe", "nain", "barbare")
players_pos = [(6, 4), (6, 5), (7, 4), (7, 5)]

# Matrice du niveau
level = [
    "ww....wwww...ww",
    "w(.w..w..w...)w",
    "www..ww.w....ww",
    "....ww$€ww...w.",
    ".........w...w.",
    "....w.......w..",
    "....ww£@ww..w.w",
    ".....w.ww.....w",
    "w]...w.......[w",
    "ww...........ww",
]

# Description de tout les symboles du niveau
meanings = {
    ".": "None",
    "w": "wall",
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
