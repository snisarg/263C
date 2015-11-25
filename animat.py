import random
from qlearning import QLearning
import config
import grid


def random_walk():
    return [random.randint(-1, 1), random.randint(-1, 1)]


class Animat:

    def __init__(self):
        self.age = 0
        self.qlearn = QLearning()

    def randomjump(self, list):
            return random.choice(list)

    def modulus_movement(self):
        self.position_x %= config.grid_width()
        self.position_y %= config.grid_height()


# --- Easy Prey class def
class EPrey(Animat):

    def __init__(self, x, y):
        Animat.__init__(self)
        self.position_x = x
        self.position_y = y
        self.position = [x, y]
        self.energy = 400

        # Set to true prey dies
        self.killed = False
        # Coordinates of the predator are set
        self.being_chased_x = -1
        self.being_chased_y = -1

    def move(self, game_clock):
        if game_clock % config.easy_prey_range() + 1 == 0:
            return
        # Check where the predators are, run in the opposite direction

        # Nothing in site, random walk.
        coord = random_walk()
        while grid.singleton_grid.is_obstacle(coord):
            coord = random_walk()
        grid.singleton_world.move_animat(self, coord)

    def update_position(self,predators,markposition):
        oldx = self.position_x
        oldy = self.position_y
        # Mark your old spot as empty
        markposition[oldx][oldy]=grid.OccupantType.EMPTY

        # If not being chased, find new spot randomly
        if self.being_chased_x == -1:
            flag = True
            while flag:
                self.position_x += self.randomjump([1,0,-1])
                self.position_y += self.randomjump([1,0,-1])
                self.modulus_movement()
                # To ensure you choose only empty spot (No collision)
                if markposition[self.position_x][self.position_y] == grid.OccupantType.EMPTY:
                    flag = False

        # You are being chased, evade!
        else:

            # Using Manhattan distance, make prey move further away from the predator
            if abs((self.position_x + 1) % config.grid_width() - self.being_chased_x) > abs((self.position_x - 1) % config.grid_width() - self.being_chased_x):
                self.position_x = (self.position_x + 1) % config.grid_width()
            else:
                self.position_x = (self.position_x - 1) % config.grid_width()
            if abs((self.position_y + 1) % config.grid_height() - self.being_chased_y) > abs((self.position_y - 1) % config.grid_height() - self.being_chased_y):
                self.position_y = (self.position_y + 1) % config.grid_height()
            else:
                self.position_y = (self.position_y - 1) % config.grid_height()

            # Let the predator chasing you, know your new position (?? If no predator chasing you, remove being_chased ??)
            for x in predators:
                if x.eprey_x == oldx and x.eprey_y == oldy:
                    x.eprey_x = self.position_x
                    x.eprey_y = self.position_y

        # Mark your new position
        markposition[self.position_x][self.position_y]=grid.OccupantType.PREY_EASY

        # If the predator is far behind, forget him
        if abs(self.position_x - self.being_chased_x) > 8 and abs(self.position_y - self.being_chased_y) > 8:
            self.being_chased_x = -1
            self.being_chased_y = -1


# --- This class can be modified to make sure that the harder prey is tougher to catch. (Change speed)
class HPrey(Animat):

    def __init__(self,x,y):
        Animat.__init__(self)
        self.position_x = x
        self.position_y = y
        self.position = [x, y]
        self.energy = 400
        # Set to true prey dies
        self.killed = False
        # Coordinates of the predator are set
        self.being_chased_x = -1
        self.being_chased_y = -1

    def move(self, game_clock):
        if game_clock % config.easy_prey_range() + 1 == 0:
            return
        coord = random_walk()
        while grid.singleton_grid.is_obstacle(coord):
            coord = random_walk()
        grid.singleton_world.move_animat(self, coord)

    def update_position(self, predators,markposition):
        oldx = self.position_x
        oldy = self.position_y
        # Mark your old spot as empty
        markposition[oldx][oldy]=grid.OccupantType.EMPTY

        # If not being chased, find new spot randomly
        if self.being_chased_x == -1:
            flag = True
            while flag:
                self.position_x += self.randomjump([1,0,-1])
                self.position_y += self.randomjump([1,0,-1])
                self.modulus_movement()
                if markposition[self.position_x][self.position_y] == grid.OccupantType.EMPTY:
                    flag = False

        # You are being chased, evade!
        else:

            # Using Manhattan distance, make prey move further away from the predator
            if (self.position_x + 2) % config.grid_width() - self.being_chased_x > (self.position_x - 1) % config.grid_width() - self.being_chased_x:
                self.position_x = (self.position_x + 2) % config.grid_width()
            else:
                self.position_x = (self.position_x - 2) % config.grid_width()
            if abs((self.position_y + 2) % config.grid_height() - self.being_chased_y) > (self.position_y - 1) % config.grid_height() - self.being_chased_y:
                self.position_y = (self.position_y + 2) % config.grid_height()
            else:
                self.position_y = (self.position_y - 2) % config.grid_height()

            # Let the predator chasing you, know your new position (?? If no predator chasing you, remove being_chased ??)
            for x in predators:
                if x.hprey_x == oldx and x.hprey_y == oldy:
                    x.hprey_x = self.position_x % config.grid_width()
                    x.hprey_y = self.position_y % config.grid_height()
        markposition[self.position_x][self.position_y]=grid.OccupantType.PREY_HARD

        # If the predator is far behind, forget him
        if abs(self.position_x - self.being_chased_x) > 8 and abs(self.position_y - self.being_chased_y) > 8:
            self.being_chased_x = -1
            self.being_chased_y = -1


class Predator(Animat):

    def __init__(self, x, y):
        Animat.__init__(self)
        self.position_x = x
        self.position_y = y
        self.position = [x, y]
        self.energy = 1000
        self.hunger_threshold = 900
        self.eprey_x = -1
        self.eprey_y = -1
        self.hprey_x = -1
        self.hprey_y = -1
        self.killed = False
        self.length = 0

    def move(self, game_clock):
        if game_clock % config.easy_prey_range() + 1 == 0:
            return
        coord = random_walk()
        while grid.singleton_grid.is_obstacle(coord):
            coord = random_walk()
        grid.singleton_world.move_animat(self, coord)

    def act(self):
        pass

# -- Sets to true when easy or hard prey is in sight (occupant = hard/easy)
    def prey_in_sight(self, occupant, mark_position):
        width = config.grid_width()
        height = config.grid_height()
        prey_x = -1
        prey_y = -1

        # Find closest Animat in vision
        min_distance = width * height
        for i in range((self.position_x - 10), (self.position_x + 10)):
            for j in range((self.position_y - 10), (self.position_y + 10)):
                if mark_position[i % width][j % height] == occupant:
                    if min_distance > self.manhattan_dist(i,j):
                        min_distance = self.manhattan_dist(i,j)
                        prey_x = i % width
                        prey_y = j % height

        # Something is in sight
        if min_distance < width*height:
            if occupant == grid.OccupantType.PREY_EASY and prey_x != -1:
                self.eprey_x = prey_x
                self.eprey_y = prey_y
            elif occupant == grid.OccupantType.PREY_HARD and prey_x != -1:
                self.hprey_x = prey_x
                self.hprey_y = prey_y
            return True

        # No Animat in sight
        else:
            if occupant == grid.OccupantType.PREY_EASY:
                self.eprey_x = -1
                self.eprey_y = -1
            elif occupant == grid.OccupantType.PREY_HARD:
                self.hprey_x = -1
                self.hprey_y = -1
            return False

# -- Sets to true when prey being chased is close enough for a kill
    def prey_close(self, occupant, mark_position):
        width = config.grid_width()
        height = config.grid_height()
        if occupant == grid.OccupantType.PREY_EASY:
            for i in range((self.position_x - 1) , (self.position_x + 1)):
                 for j in range((self.position_y - 1), (self.position_y + 1)):
                     if i % width == self.eprey_x and j % height == self.eprey_y:
                         return True
        else:
            for i in range((self.position_x - 1) , (self.position_x + 1)):
                 for j in range((self.position_y - 1), (self.position_y + 1)):
                     if i % width == self.hprey_x and j % height == self.hprey_y:
                         return True
        return False

# -- Returning Manhattan distance between i and j
    def manhattan_dist(self, i ,j):
        return abs(self.position_x - i % config.grid_width()) + abs(self.position_y - j % config.grid_height())

# -- Walk randomly
    def update_position(self,markposition):
            markposition[self.position_x][self.position_y]=grid.OccupantType.EMPTY
            self.position_x += self.randomjump([1, -1])
            self.position_y += self.randomjump([1, -1])
            self.modulus_movement()
            markposition[self.position_x][self.position_y]=grid.OccupantType.PREDATOR


# -- Go towards easy prey
    def chase_e_prey(self, eprey,markposition):
            # Using Manhattan distance, make predator move towards prey
            width = config.grid_width()
            height = config.grid_height()

            # Mark Previous position as empty
            markposition[self.position_x][self.position_y] = grid.OccupantType.EMPTY

            # Find Best step to take
            step = 1
            if (self.position_x + step) % width - self.eprey_x < (self.position_x - step) % width - self.eprey_x:
                self.position_x = (self.position_x + step) % width
            else:
                self.position_x = (self.position_x - step) % width
            if (self.position_y + step) % height - self.eprey_y < (self.position_y - step) % height - self.eprey_y:
                self.position_y = (self.position_y + step) % height
            else:
                self.position_y = (self.position_y - step) % height

            # Update prey so that it knows your new position
            flag = False
            for x in eprey:
                if x.position_x == self.eprey_x and x.position_y == self.eprey_y:
                    x.being_chased_x = self.position_x
                    x.being_chased_y = self.position_y
                    flag = True
            # The prey you are chasing has been killed
            if not flag:
                self.eprey_x = -1
                self.eprey_y = -1

            # Mark your new spot as occupied
            markposition[self.position_x][self.position_y] = grid.OccupantType.PREDATOR

            # If you need to know how long the chase has gone on
            self.length += 1

# -- Go towards hard prey
    def chase_h_prey(self, hprey, markposition):
            # Using Manhattan distance, make predator move towards prey
            width = config.grid_width()
            height = config.grid_height()

            # Mark Previous position as empty
            markposition[self.position_x][self.position_y]=grid.OccupantType.EMPTY

            # Find Best step to take
            step = 1
            if (self.position_x + step) % width - self.hprey_x < (self.position_x - step) % width - self.hprey_x:
                self.position_x = (self.position_x + step) % width
            else:
                self.position_x = (self.position_x - step) % width
            if (self.position_y + step) % height - self.hprey_y < (self.position_y - step) % height - self.hprey_y:
                self.position_y = (self.position_y + step) % height
            else:
                self.position_y = (self.position_y - step) % height

            # Update prey so that it knows your new position
            flag = False
            for x in hprey:
                if x.position_x == self.hprey_x and x.position_y == self.hprey_y:
                    x.being_chased_x = self.position_x
                    x.being_chased_y = self.position_y
                    flag = True
            # The prey you are chasing has been killed
            if not flag:
                self.hprey_x = -1
                self.hprey_y = -1

            # Mark your new spot as occupied
            markposition[self.position_x][self.position_y] = grid.OccupantType.PREDATOR

            # If you need to know how long the chase has gone on
            self.length += 1


# -- Eat easy prey, update your location to easy prey. Remove easy prey's coordinates
    def eat_e_prey(self,eprey,markposition):

            for x in eprey:
                if x.position_x == self.eprey_x and x.position_y == self.eprey_y:
                    # Mark prey as killed
                    x.killed = True

                    # Energy reward
                    self.energy += 200

                    print "Chase lasted ", self.length
                    self.length = 0

                    # Make position of predator as that of killed prey
                    markposition[self.position_x][self.position_y] = grid.OccupantType.EMPTY
                    self.position_x = self.eprey_x
                    self.position_y = self.eprey_y

                    # Update mark position to predator
                    markposition[self.eprey_x][self.eprey_y] = grid.OccupantType.PREDATOR

                    # Remove coordinates of prey that predator was chasing
                    self.eprey_x = -1
                    self.eprey_y = -1

# -- Eat hard prey, update your location to hard prey. Remove Hard prey's coordinates
    def eat_h_prey(self,hprey,markposition):

            for x in hprey:
                if x.position_x == self.hprey_x and x.position_y == self.hprey_y:
                    # Mark prey as killed
                    x.killed = True

                    # Energy reward
                    self.energy += 600

                    print "Chase lasted ", self.length
                    self.length = 0


                    # Make position of predator as that of killed prey
                    markposition[self.position_x][self.position_y] = grid.OccupantType.EMPTY
                    self.position_x = self.hprey_x
                    self.position_y = self.hprey_y

                    # Update mark position to predator
                    markposition[self.hprey_x][self.hprey_y] = grid.OccupantType.PREDATOR

                    # Remove coordinates of prey that predator was chasing
                    self.hprey_x = -1
                    self.hprey_y = -1


# -- Problems to Address
# 1. Sometimes two or more predators can lock on to a single target. They both update the prey's position x and position y information.
# That makes no sense.
# 2. What if you give same speed to both easy and hard prey. But energy of hard prey is much higher.
# If energy(hard) > energy(predator) make hard animat survive.
# 3. Why do they run to the corner so often?
# 4. Let each prey store a list of predators chasing it. Rather than it's x and y coordinates.
