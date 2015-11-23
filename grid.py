from random import randint
import config


class OccupantType:
    EMPTY = 0
    OBSTACLE = 1
    PREDATOR = 2
    PREY_EASY = 3
    PREY_HARD = 4
    COLOUR_MAP = {EMPTY: (240, 240, 240),   #RGB values
                  OBSTACLE: (10, 10, 10),
                  PREDATOR: (255, 0, 0),
                  PREY_EASY: (0, 127, 0),
                  PREY_HARD: (0, 255, 0)}


class GridCell:

    def __init__(self, occupant_type):
        self.colour_map = OccupantType.COLOUR_MAP
        self.occupants = [occupant_type]

    def get_colour(self):
        return self.colour_map[self.occupants[0]]


class Grid:

    def __init__(self):
        self.grid = [[GridCell(OccupantType.EMPTY) for i in range(config.grid_width())] for i in range(config.grid_height())]
        self.single_obstacles()

    def single_obstacles(self):
        for i in range(config.single_obstacle_count()):
            self.grid[randint(0, config.grid_height()-1)][randint(0, config.grid_width()-1)] = GridCell(OccupantType.OBSTACLE)

singleton_grid = Grid().grid
