from random import randint
import random
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
                  animat.EPrey: (0, 255, 0),
                  animat.HPrey: (0, 127, 0),
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

    def get_occupants_in(self, coord):
        coord[0] %= config.grid_height()
        coord[1] %= config.grid_width()
        return self.grid[coord[0]][coord[1]].occupants

class World:

    def __init__(self, position_grid):
        self.grid = position_grid
        self.easy_preys = []
        self.hard_preys = []
        self.predators = []
        self.clock = 0
        self.__init_easy_prey(config.easy_prey_count())
        self.__init_hard_prey(config.hard_prey_count())
        self.__init_predator(config.predator_count())

    def __init_easy_prey(self,count):
        for i in range(count):
            coord = [randint(0, config.grid_height()-1), randint(0, config.grid_width()-1)]
            if not self.grid.is_obstacle(coord):
                prey = animat.EPrey(coord[0], coord[1])
                self.easy_preys.append(prey)
                self.grid.add_to_position(coord, prey)
            else:
                i -= 1

    def __init_hard_prey(self,count):
        for i in range(count):
            coord = [randint(0, config.grid_height()-1), randint(0, config.grid_width()-1)]
            if not self.grid.is_obstacle(coord):
                prey = animat.HPrey(coord[0], coord[1])
                self.hard_preys.append(prey)
                self.grid.add_to_position(coord, prey)
            else:
                i -= 1

    def __new_generation(self):

        easy_prey_count = len(self.easy_preys)
        self.easy_preys = []
        self.__init_easy_prey(easy_prey_count)

        hard_prey_count = len(self.hard_preys)
        self.hard_preys = []
        self.__init_hard_prey(hard_prey_count)

        self.clock = 0

        best_predators = []
        count = min(len(self.predators),config.best_predator_count())

        # Find best predators based on energy and store in best_predators[]
        for j in range(count):
            max_predator = self.predators[0]
            rem_i = 0
            for i in range(len(self.predators)):
                if self.predators[i].energy > max_predator.energy:
                    max_predator = self.predators[i]
                    rem_i = i
            best_predators.append(max_predator)
            self.predators.pop(rem_i)

        predator_count = len(self.predators)
        self.predators = []
        self.__init_predator(predator_count)

        # Potential memory leak
        # Children have same Q tables as that of a random parent
        for i in range(predator_count):
            self.predators[i].qlearn = random.choice(best_predators).qlearn


    def __init_predator(self,count):
        for i in range(count):
            coord = [randint(0, config.grid_height()-1), randint(0, config.grid_width()-1)]
            if not self.grid.is_obstacle(coord):
                predator = animat.Predator(coord[0], coord[1])
                self.predators.append(predator)
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

    def around_point(self, coord, view_range):
        ranged_animats = []     # Will contain animats in order of ranges.
        for r in range(view_range):     # Range 0, or adjacent cells, up to vision.
            single_range = []
            # Look in the cells at this level
            # Height constant iterations
            for i in range(-1-r, 2+r):
                occ = self.grid.get_occupants_in([coord[0]-r-1, coord[1]+i])
                if occ:
                    single_range.append(occ)
                occ = self.grid.get_occupants_in([coord[0]+r+1, coord[1]+i])
                if occ:
                    single_range.append(occ)
            # Width constant iterations
            for i in range(-1-r, 2+r):
                occ = self.grid.get_occupants_in([coord[0]+i, coord[1]-r-1])
                if occ:
                    single_range.append(occ)
                occ = self.grid.get_occupants_in([coord[0]+i, coord[1]+r+1])
                if occ:
                    single_range.append(occ)
            ranged_animats.append(single_range)
        return ranged_animats

    def kill(self, animat):
        self.grid.remove_from_position(animat)
        if animat in self.easy_preys:
            self.easy_preys.remove(animat)
            print "Easy killed at " + str(animat.position)
        if animat in self.hard_preys:
            self.hard_preys.remove(animat)
            print "Hard killed at " + str(animat.position)
        if animat in self.predators:
            self.predators.remove(animat)
            print "Predator died at " + str(animat.position)

    def tick(self):
        # Pick the next step
        for easy in self.easy_preys:
            easy.move(self.clock)
        for hard in self.hard_preys:
            hard.move(self.clock)
        for predator in self.predators:
            predator.move(self.clock)
        # Process the movement and results
        # Right now only Predators can take actions of their movement.
        for predator in self.predators:
            # Reduce wait time
            predator.reduce_wait()
            predator.act()
            predator.update_energy(-1)
        self.clock += 1  # increment timer.


singleton_grid = Grid()
singleton_world = World(singleton_grid)
