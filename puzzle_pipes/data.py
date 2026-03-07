from game_env import Tile, PipesGameState

MY_LEVELS = {
    'level1': [
        [Tile(4, 90), Tile(0, 90), Tile(2, 0), Tile(0, 0), Tile(4, 90)],
        [Tile(4, 270), Tile(1, 180), Tile(2, 180), Tile(0, 0), Tile(4, 0)],
        [Tile(1, 90), Tile(2, 0), Tile(2, 0), Tile(2, 0), Tile(4, 180)],
        [Tile(2, 90), Tile(0, 90), Tile(4, 180), Tile(2, 180), Tile(1, 90)],
        [Tile(1, 180), Tile(4, 180), Tile(4, 0), Tile(1, 180), Tile(4, 270)],
    ],
    'level2': [
        [Tile(4, 180), Tile(1, 0), Tile(0, 90), Tile(4, 0), Tile(4, 0)],
        [Tile(0, 0), Tile(2, 0), Tile(0, 90), Tile(4, 0), Tile(0, 90)],
        [Tile(1, 180), Tile(2, 0), Tile(2, 270), Tile(2, 180), Tile(2, 180)],
        [Tile(1, 180), Tile(1, 0), Tile(0, 0), Tile(4, 90), Tile(0, 90)],
        [Tile(4, 270), Tile(1, 180), Tile(2, 180), Tile(4, 90), Tile(4, 90)],
    ],
    'level3': [
        [Tile(1, 0), Tile(1, 0), Tile(4, 180), Tile(1, 0), Tile(4, 0)],
        [Tile(4, 90), Tile(1, 270), Tile(0, 0), Tile(2, 270), Tile(0, 0)],
        [Tile(4, 90), Tile(0, 90), Tile(2, 0), Tile(2, 0), Tile(2, 90)],
        [Tile(4, 180), Tile(4, 0), Tile(2, 180), Tile(1, 180), Tile(4, 90)],
        [Tile(1, 270), Tile(2, 180), Tile(1, 270), Tile(1, 270), Tile(4, 180)],
    ],
    'level4': [
        [Tile(4, 180), Tile(2, 270), Tile(4, 0), Tile(1, 270), Tile(4, 180)],
        [Tile(4, 270), Tile(2, 90), Tile(1, 180), Tile(2, 270), Tile(1, 180)],
        [Tile(4, 180), Tile(2, 180), Tile(2, 270), Tile(4, 90), Tile(1, 0)],
        [Tile(4, 270), Tile(1, 90), Tile(2, 90), Tile(0, 0), Tile(4, 90)],
        [Tile(4, 90), Tile(2, 0), Tile(2, 270), Tile(0, 0), Tile(4, 180)],
    ],
    'level5': [
        [Tile(4, 270), Tile(4, 0), Tile(1, 0), Tile(4, 90), Tile(4, 180)],
        [Tile(1, 180), Tile(2, 90), Tile(2, 0), Tile(4, 0), Tile(2, 90)],
        [Tile(4, 90), Tile(4, 0), Tile(2, 90), Tile(2, 0), Tile(1, 270)],
        [Tile(0, 90), Tile(2, 180), Tile(2, 90), Tile(2, 0), Tile(1, 270)],
        [Tile(1, 0), Tile(1, 90), Tile(4, 90), Tile(4, 90), Tile(4, 90)],
    ],
    'level6': [
        [Tile(4, 90), Tile(0, 90), Tile(2, 90), Tile(0, 0), Tile(4, 0)],
        [Tile(4, 180), Tile(2, 270), Tile(2, 0), Tile(1, 90), Tile(4, 0)],
        [Tile(1, 270), Tile(2, 180), Tile(1, 180), Tile(2, 0), Tile(4, 90)],
        [Tile(4, 180), Tile(2, 90), Tile(0, 0), Tile(0, 90), Tile(1, 180)],
        [Tile(4, 180), Tile(2, 270), Tile(0, 0), Tile(4, 90), Tile(4, 270)],
    ],
    'level7': [
        [Tile(4, 270), Tile(4, 270), Tile(1, 180), Tile(0, 90), Tile(4, 0)],
        [Tile(2, 270), Tile(2, 0), Tile(2, 270), Tile(2, 0), Tile(4, 270)],
        [Tile(4, 90), Tile(1, 180), Tile(1, 90), Tile(2, 180), Tile(4, 180)],
        [Tile(4, 180), Tile(2, 0), Tile(1, 90), Tile(0, 0), Tile(4, 0)],
        [Tile(4, 270), Tile(1, 0), Tile(1, 180), Tile(2, 180), Tile(1, 0)],
    ],
}

def get_level(name):
    return PipesGameState(MY_LEVELS[name])