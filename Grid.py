from random import randint

GRID_WIDTH_MAX = 10
GRID_HEIGHT_MAX = 10


class OccupantType:
    EMPTY = 0
    OBSTACLE = 1
    PREDATOR = 2
    PREY_EASY = 3
    PREY_HARD = 4
    COLOUR_MAP = {EMPTY: (240, 240, 240),
                  OBSTACLE: (10, 10, 10),
                  PREDATOR: (255, 0, 0),
                  PREY_EASY: (0, 127, 0),
                  PREY_HARD: (0, 255, 0)}


class GridCell:

    def __init__(self, type):
        self.colour_map = OccupantType.COLOUR_MAP
        self.occupants = [type]

    def get_colour(self):
        return self.colour_map[self.occupants[0]]


class Grid:

    def __init__(self):
        self.grid = [[GridCell(OccupantType.EMPTY) for i in range(GRID_WIDTH_MAX)] for i in range(GRID_HEIGHT_MAX)]
        self.single_obstacles()

    def single_obstacles(self):
        for i in range(11):
            self.grid[randint(0, GRID_HEIGHT_MAX-1)][randint(0, GRID_WIDTH_MAX-1)] = GridCell(OccupantType.OBSTACLE)