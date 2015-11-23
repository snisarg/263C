from random import randint
import config


class OccupantType:
    EMPTY = 0
    OBSTACLE = 1
    PREDATOR = 2
    PREY_EASY = 3
    PREY_HARD = 4
    GRASS = 5
    COLOUR_MAP = {EMPTY: (240, 240, 240),   #RGB values
                  OBSTACLE: (10, 10, 10),
                  PREDATOR: (255, 0, 0),
                  PREY_EASY: (0, 127, 0),
                  PREY_HARD: (0, 255, 0),
                  GRASS: (150, 250, 150)}


class GridCell:

    def __init__(self, occupant_type):
        self.colour_map = OccupantType.COLOUR_MAP
        self.occupants = [occupant_type]

    def get_colour(self):
        return self.colour_map[self.occupants[0]]


class Grid:

    def __init__(self):
        self.grid = [[GridCell(OccupantType.EMPTY) for i in range(config.grid_width())] for i in range(config.grid_height())]
        self.set_single_obstacles()
        self.set_grass()

    def set_single_obstacles(self):
        for i in range(config.single_obstacle_count()):
            coord = (randint(0, config.grid_height()-1), randint(0, config.grid_width()-1))
            self.set_at_position(coord, OccupantType.OBSTACLE)

    def is_obstacle(self, coord):
        if OccupantType.OBSTACLE in self.grid[coord[0]][coord[1]].occupants:
            return True;
        return False

    def set_grass(self):
        for i in range(config.grass_count()):
            coord = (randint(0, config.grid_height()-1), randint(0, config.grid_width()-1))
            if not self.is_obstacle(coord):
                self.set_at_position(coord, OccupantType.GRASS)

    def set_at_position(self, coord, occupant):
        self.grid[coord[0]][coord[1]].occupants.append(occupant)
        self.remove_from_position(coord, OccupantType.EMPTY)

    def remove_from_position(self, coord, occupant):
        if occupant in self.grid[coord[0]][coord[1]].occupants:
            self.grid[coord[0]][coord[1]].occupants.remove(occupant)

singleton_grid = Grid().grid
