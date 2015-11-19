from random import randint
import random
from qlearning import QLearning
import math
import config
from grid import OccupantType


class Animat:

    def __init__(self):
        self.age = 0
        self.direction = self.getdirection()
        self.qlearn = QLearning()

    # Define direction of the animat as radians
    # To determine which animat is in the line of sight, calculate atan(slope) between animat1 and animat2
    def getdirection(self):
        return (randint(0,360) * math.pi) / 180

    def randomjump(self, list):
            return random.choice(list)

    def modulus_movement(self):
        self.position_x %= config.grid_width()
        self.position_y %= config.grid_height()


# --- Easy Prey class def
class EPrey(Animat):

    def __init__(self,x,y):
        Animat.__init__(self)
        self.position_x = x
        self.position_y = y
        self.energy = 500

        # Set to true prey dies
        self.killed = False
        # Coordinates of the predator are set
        self.being_chased_x = -1
        self.being_chased_y = -1

    def update_position(self):
        if self.being_chased_x == -1:
            self.position_x += self.randomjump([1,-1])
            self.position_y += self.randomjump([1,-1])
        else:
            # Using Manhattan distance, make prey move further away from the predator
            self.position_x = max([self.position_x + 1 - self.being_chased_x , self.position_x -1 - self.being_chased_x])
            self.position_y = max([self.position_y + 1 - self.being_chased_y , self.position_y -1 - self.being_chased_y])
        self.modulus_movement()


# --- This class can be modified to make sure that the harder prey is tougher to catch. (Change speed)
class HPrey(Animat):

    def __init__(self,x,y):
        Animat.__init__(self)
        self.position_x = x
        self.position_y = y
        self.energy = 750
        # Set to true prey dies
        self.killed = False
        # Coordinates of the predator are set
        self.being_chased_x = -1
        self.being_chased_y = -1

    def update_position(self):
        if self.being_chased_x == -1:
            self.position_x += self.randomjump([1,-1])
            self.position_y += self.randomjump([1,-1])
        else:
            # Using Manhattan distance, make prey move further away from the predator
            self.position_x = max([self.position_x + 1 - self.being_chased_x , self.position_x -1 - self.being_chased_x])
            self.position_y = max([self.position_y + 1 - self.being_chased_y , self.position_y -1 - self.being_chased_y])
        self.modulus_movement()


class Predator(Animat):

    def __init__(self, x, y):
        Animat.__init__(self)
        self.position_x = x
        self.position_y = y
        self.energy = 1000
        self.hunger_threshold = 200
        self.eprey_x = -1
        self.eprey_y = -1
        self.hprey_x = -1
        self.hprey_y = -1
        self.killed = False

    def prey_in_sight(self, occupant, mark_position):
        width = config.grid_width()
        height = config.grid_height()
        prey_x = -1
        prey_y = -1
        min_distance = width * height # Large value as min_distance
        for i in range((self.position_y - 10) % height , (self.position_y + 10) % height, 1):
            for j in range((self.position_x - 10) % width, (self.position_x + 10) % width, 1):
                if mark_position[i][j] == occupant:
                    min_distance = min(min_distance , self.manhattan_dist(i,j))
                    prey_y = i
                    prey_x = j
        if min_distance < width*height:
            if occupant == OccupantType.PREY_EASY and prey_x != -1:
                self.eprey_x = prey_x
                self.eprey_y = prey_y

            elif occupant == OccupantType.PREY_HARD and prey_x != -1:
                self.hprey_x = prey_x
                self.hprey_y = prey_y
            return True
        else:
            if occupant == OccupantType.PREY_EASY:
                self.eprey_x = -1
                self.eprey_y = -1

            elif occupant == OccupantType.PREY_HARD:
                self.hprey_x = -1
                self.hprey_y = -1
            return False

    def prey_close(self, occupant, mark_position):
        width = config.grid_width()
        height = config.grid_height()
        for i in range((self.position_y - 1) % height , (self.position_y + 10) % height, 1):
            for j in range((self.position_x - 1) % width, (self.position_x + 10) % width, 1):
                if mark_position[i][j] == occupant:
                    return True
        return False

    def manhattan_dist(self, i ,j):
        return (self.position_x % config.grid_width()) - i + (self.position_y % config.grid_height()) - j

    def update_position(self):
            self.position_x += self.randomjump([1,-1])
            self.position_y += self.randomjump([1,-1])
            self.modulus_movement()

    def chase_e_prey(self, eprey):
        # Using Manhattan distance, make predator move towards prey
            self.position_x = min([self.position_x + 1 - self.eprey_x, self.position_x -1 - self.eprey_x])
            self.position_y = min([self.position_y + 1 - self.eprey_y, self.position_y -1 - self.eprey_y])
            self.modulus_movement()
            for x in eprey:
                if x.position_x == self.eprey_x and x.position_y == self.eprey_y:
                    x.being_chased_x = self.position_x
                    x.being_chased_y = self.position_y

    def chase_h_prey(self, hprey):
        # Using Manhattan distance, make predator move towards prey
            self.position_x = min([self.position_x + 1 - self.hprey_x, self.position_x -1 - self.hprey_x])
            self.position_y = min([self.position_y + 1 - self.hprey_y, self.position_y -1 - self.hprey_y])
            self.modulus_movement()
            for x in hprey:
                if x.position_x == self.eprey_x and x.position_y == self.eprey_y:
                    x.being_chased_x = self.position_x
                    x.being_chased_y = self.position_y

    def eat_e_prey(self,eprey):
            for x in eprey:
                if x.position_x == self.eprey_x and x.position_y == self.eprey_y:
                    x.killed = True
                    self.energy += x.energy

    def eat_h_prey(self,hprey):
            for x in hprey:
                if x.position_x == self.eprey_x and x.position_y == self.eprey_y:
                    x.killed = True
                    self.energy += x.energy

