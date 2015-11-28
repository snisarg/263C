from random import randint
import config
import animat


class OccupantType:
    EMPTY = 0
    OBSTACLE = 1
    PREDATOR = 2
    PREY_EASY = 3
    PREY_HARD = 4
    GRASS = 5
    COLOUR_MAP = {EMPTY: (240, 240, 240),  #RGB values
                  OBSTACLE: (10, 10, 10),
                  animat.Predator: (255, 0, 0),
                  animat.EPrey: (0, 127, 0),
                  animat.HPrey: (0, 255, 0),
                  GRASS: (242, 255, 242)}


class GridCell:

    def __init__(self, occupant_type):
        self.colour_map = OccupantType.COLOUR_MAP
        self.floor = occupant_type                  # Can be grass, obstacle or nothing
        self.occupants = []                         # What animats are in the cell

    def get_colour(self):
        if len(self.occupants) > 0:
            return self.colour_map[self.occupants[0].__class__]
        return self.colour_map[self.floor]


class Grid:

    def __init__(self):
        self.grid = [[GridCell(OccupantType.EMPTY) for i in range(config.grid_width())] for i in range(config.grid_height())]
        # self.set_single_obstacles()
        self.__set_grass()

    def __set_single_obstacles(self):
        for i in range(config.single_obstacle_count()):
            coord = (randint(0, config.grid_height()-1), randint(0, config.grid_width()-1))
            self.__set_floor(coord, OccupantType.OBSTACLE)

    def is_obstacle(self, coord):
        if OccupantType.OBSTACLE == self.grid[coord[0]][coord[1]].floor:
            return True
        return False

    def __set_grass(self):
        for i in range(config.grass_count()):
            coord = (randint(0, config.grid_height()-1), randint(0, config.grid_width()-1))
            if not self.is_obstacle(coord):
                self.__set_floor(coord, OccupantType.GRASS)

    def __set_floor(self, coord, occupant):
        self.grid[coord[0]][coord[1]].floor = occupant

    def remove_from_position(self, occupant):
        coord = occupant.position
        if occupant in self.grid[coord[0]][coord[1]].occupants:
            self.grid[coord[0]][coord[1]].occupants.remove(occupant)
            return True
        return False

    def add_to_position(self, coord, occupant):
        coord[0] %= config.grid_height()
        coord[1] %= config.grid_width()
        self.grid[coord[0]][coord[1]].occupants.append(occupant)
        return coord


class World:

    def __init__(self, position_grid):
        self.grid = position_grid
        self.easy_preys = []
        self.hard_preys = []
        self.predators = []
        self.clock = 0
        self.__init_easy_prey()
        self.__init_hard_prey()
        self.__init_predator()

    def __init_easy_prey(self):
        for i in range(config.animats_easy_prey_count()):
            coord = [randint(0, config.grid_height()-1), randint(0, config.grid_width()-1)]
            if not self.grid.is_obstacle(coord):
                prey = animat.EPrey(coord[0], coord[1])
                self.easy_preys.append(prey)
                self.grid.add_to_position(coord, prey)
            else:
                i -= 1

    def __init_hard_prey(self):
        for i in range(config.animats_easy_prey_count()):
            coord = [randint(0, config.grid_height()-1), randint(0, config.grid_width()-1)]
            if not self.grid.is_obstacle(coord):
                prey = animat.HPrey(coord[0], coord[1])
                self.easy_preys.append(prey)
                self.grid.add_to_position(coord, prey)
            else:
                i -= 1

    def __init_predator(self):
        for i in range(config.animats_easy_prey_count()):
            coord = [randint(0, config.grid_height()-1), randint(0, config.grid_width()-1)]
            if not self.grid.is_obstacle(coord):
                predator = animat.Predator(coord[0], coord[1])
                self.easy_preys.append(predator)
                self.grid.add_to_position(coord, predator)
            else:
                i -= 1

    def move_animat(self, animat, new_coord):
        if self.grid.remove_from_position(animat):
            new_coord[0] += animat.position[0]
            new_coord[1] += animat.position[1]
            new_coord = self.grid.add_to_position(new_coord, animat)
            animat.position = new_coord
        else:
            print "Animat not in position indicated by the animat object."

    def tick(self):
        # Pick the next step
        for easy in self.easy_preys:
            easy.move(self.clock)
        for hard in self.hard_preys:
            hard.move()
        for predator in self.predators:
            predator.move(self.clock)
        # Process the movement and results
        # Right now only Predators can take actions of their movement.
        for predator in self.predators:
            predator.act(self.clock)
        self.clock += 1  # increment timer.


singleton_grid = Grid()
singleton_world = World(singleton_grid)
