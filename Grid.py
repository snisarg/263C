GRID_WIDTH_MAX = 10
GRID_HEIGHT_MAX = 10


class OccupantType:
    EMPTY = 0
    OBSTACLE = 1
    PREDATOR = 2
    PREY_EASY = 3
    PREY_HARD = 4
    COLOUR_MAP = {EMPTY: (0, 0, 0),
                  OBSTACLE: (255, 255, 255),
                  PREDATOR: (255, 0, 0),
                  PREY_EASY: (0, 127, 0),
                  PREY_HARD: (0, 255, 0)}


class GridCell:

    def __init__(self, colour_map):
        self.colour_map = colour_map
        self.occupants = [OccupantType.EMPTY]

    def get_colour(self):
        return self.colour_map[self.occupants[0]]


class Grid:

    def __init__(self):
        self.grid = [[GridCell(OccupantType.COLOUR_MAP) for i in range(GRID_WIDTH_MAX)] for i in range(GRID_HEIGHT_MAX)]

    def print_grid(self):
        for i in range(0, GRID_HEIGHT_MAX):
            for j in range(0, GRID_WIDTH_MAX):
                print self.grid[i][j].get_colour()
            print '\n'

x = Grid()
x.print_grid()
