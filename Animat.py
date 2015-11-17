from random import randint
from qlearning import QLearning
import math


class Animat:

    def __init__(self):
        self.age = 0
        self.direction = self.getdirection()
        self.qlearn = QLearning()

    # Define direction of the animat as radians
    # To determine which animat is in the line of sight, calculate atan(slope) between animat1 and animat2
    def getdirection(self):
        return (randint(0,360) * math.pi) / 180


class EPrey(Animat):

    def __init__(self,x,y):
        Animat.__init__(self)
        self.position_x = x
        self.position_y = y
        self.energy = 500


class HPrey(Animat):

    def __init__(self,x,y):
        Animat.__init__(self)
        self.position_x = x
        self.position_y = y
        self.energy = 750


class Predator(Animat):

    def __init__(self,x,y):
        Animat.__init__(self)
        self.position_x = x
        self.position_y = y
        self.energy = 1000
