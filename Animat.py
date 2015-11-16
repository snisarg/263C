from random import randint


class Animat:

    def __init__(self):
        # Define grid position (1000x1000)
        self.position_x = randint(0, 1000)
        self.position_y = randint(0, 1000)
        self.age = 0
        # Define direction of the animat as degrees
        self.direction = randint(0, 360)