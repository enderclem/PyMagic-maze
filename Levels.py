# Contient le niveau et certaines variables

players_name = ("magicienne", "elfe", "nain", "barbare")
players_pos = [(6, 4), (6, 5), (7, 4), (7, 5)]
max_time = 180.0
time_left = max_time

# Matrice du niveau
level = [
    "##....####...##",
    "#(.#..#..#...)#",
    "###..##.#....##",
    "....##$€##...#.",
    ".........#...#.",
    "....#.......#..",
    "....##£@##..#.#",
    ".....#.##.....#",
    "#]...#.......[#",
    "##...........##",
]

# Description de tout les symboles du niveau
meanings = {
    ".": "None",
    "#": "wall",
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
