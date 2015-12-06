import random
from qlearning import *
import config
import grid
import math


def random_walk():
    return [random.randint(-1, 1), random.randint(-1, 1)]


def distance_diff(reference, target, vision_range):
    # print (reference, target, vision_range)
    ref_h = reference[0]
    ref_w = reference[1]
    tar_h = target[0]
    tar_w = target[1]

    height = tar_h - ref_h
    width = tar_w - ref_w

    if abs(height) > (vision_range + 1):
        if ref_h > tar_h:
            tar_h += config.grid_height()
        else:
            ref_h += config.grid_height()
        height = tar_h - ref_h
        height_sign = 1
        if height < 0:
            height_sign = -1
        height %= vision_range + 1
        height *= height_sign

    if abs(width) > (vision_range + 1):
        if ref_w > tar_w:
            tar_w += config.grid_width()
        else:
            ref_w += config.grid_width()
        width = tar_w - ref_w
        width_sign = 1
        if width < 0:
            width_sign = -1
        width %= vision_range + 1
        width *= width_sign

    return [height, width]


def normalise_distance(coord, level):
    # Normalise huge differences to one step for calculations.
    difference = coord[:]
    # TODO can be done better.
    for i in range(level):
        if difference[0] > 1:
            difference[0] -= 1
        elif difference[0] < -1:
            difference[0] += 1
        if difference[1] > 1:
            difference[1] -= 1
        elif difference[1] < -1:
            difference[1] += 1
    return difference

class StepCalculator:

    def __init__(self, step_weight):
        self.weight = step_weight
        self.decision_memo = [0, 0, 0, 0, 0, 0, 0, 0]
        self.map = {-1: {-1: 0, 0: 1, 1: 2}, 0: {-1: 7, 1: 3}, 1: {1: 4, 0: 5, -1: 6}}
        self.reverse_map = ([-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1])
        self.count = 0

    def __set_index_weight(self, index, weight):
        index %= 8    # 8 because there are 8 possible blocks
        self.decision_memo[index] += weight

    def add(self, difference):
        self.count += 1
        # Find row number for weight selection
        h = math.fabs(difference[0])
        w = math.fabs(difference[1])
        level = int(max(h, w) - 1)
        current_weight = self.weight[int(level)]

        difference = normalise_distance(difference, level)

        # Here, 'difference' represents which direction is the predator coming from
        # Negative weights for origin of predator
        index = self.map[difference[0]][difference[1]]
        self.__set_index_weight(index, -current_weight)
        self.__set_index_weight(index-1, -round(current_weight/2))
        self.__set_index_weight(index+1, -round(current_weight/2))
        # Opposite side of the predator
        index = self.map[-difference[0]][-difference[1]]
        self.__set_index_weight(index, current_weight)
        self.__set_index_weight(index-1, round(current_weight/2))
        self.__set_index_weight(index+1, round(current_weight/2))

    def get_decision(self):
        max = self.decision_memo[0]
        result = 0
        for i in range(1, 8):
            if self.decision_memo[i] > max:
                max = self.decision_memo[i]
                result = i
        return self.reverse_map[result]

    def get_count(self):
        return self.count


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
        self.position = [x, y]
        self.energy = 400

        # Set to true prey dies
        self.killed = False

    def move(self, game_clock):
        if game_clock % (config.easy_prey_speed() + 1) == 0:
            return
        # Check where the predators are, run in the opposite direction
        closest_animats = grid.singleton_world.around_point(self.position, config.easy_prey_range())
        step_calc = StepCalculator((10, 6, 4, 2, 1))
        for level in closest_animats:
            for block in level:
                for anim in block:
                    if isinstance(anim, Predator):
                        # Escaping 0 differences for now because of toroidal diff bug
                        diff = distance_diff(self.position, anim.position, config.easy_prey_range())
                        # print diff
                        #if not (diff[0] == 0 and diff[1] == 0):
                        step_calc.add(diff)

        if not step_calc.get_count() == 0:
            coord = step_calc.get_decision()
        else:
            # Nothing in site, random walk.
            coord = random_walk()
            while grid.singleton_grid.is_obstacle(coord):
                coord = random_walk()

        grid.singleton_world.move_animat(self, coord)



# --- This class can be modified to make sure that the harder prey is tougher to catch. (Change speed)
class HPrey(Animat):

    def __init__(self,x,y):
        Animat.__init__(self)
        self.position = [x, y]
        self.energy = random.randint(1200,1400)
        # Set to true prey dies
        self.killed = False

    def move(self, game_clock):
        if game_clock % (config.hard_prey_speed() + 1) == 0:
            return
        closest_animats = grid.singleton_world.around_point(self.position, config.hard_prey_range())
        step_calc = StepCalculator((10, 6, 4, 2, 1))
        for level in closest_animats:
            for block in level:
                for anim in block:
                    if isinstance(anim, Predator):
                        # Escaping 0 differences for now because of toroidal diff bug
                        diff = distance_diff(self.position, anim.position, config.hard_prey_range())
                        # if not (diff[0] == 0 and diff[1] == 0):
                        step_calc.add(diff)

        if not step_calc.get_count() == 0:
            coord = step_calc.get_decision()
        else:
            # Nothing in site, random walk.
            coord = random_walk()
            while grid.singleton_grid.is_obstacle(coord):
                coord = random_walk()
        grid.singleton_world.move_animat(self, coord)


class Predator(Animat):

    def __init__(self, x, y, z):
        Animat.__init__(self)
        self.position = [x, y]
        self.energy = 1000
        self.hunger_threshold = 1500
        self.killed = False
        self.wait_time = 5
        self.id = z

    # Returns animat closest to predator's positions
    def __closest_animat(self):
        closest_animats = grid.singleton_world.around_point(self.position, config.predator_range())
        for level in closest_animats:
            for block in level:
                for anim in block:
                    if isinstance(anim, EPrey) or isinstance(anim, HPrey):
                        return anim # Return the anim object which is closest
        return None

    def move(self, game_clock):
        if game_clock % (config.predator_speed() + 1) == 0:
            return

        if self.wait_time > 0:
            self.wait_time -= 1
            return

        anim = self.__closest_animat()
        if anim is None:
            coord = None    # No prey in sight
        else:
            coord = anim.position   # anim is in sight

        current_state = self.sense_state(anim)
        current_action = self.qlearn.choose_action(current_state)

        if current_action[0] == Action.TowardsEasyPrey or current_action[0] == Action.TowardsHardPrey:
            coord = normalise_distance(
                distance_diff(self.position, coord, config.predator_range()), config.predator_range())
        else:
            coord = random_walk()
            while grid.singleton_grid.is_obstacle(coord):
                coord = random_walk()
        grid.singleton_world.move_animat(self, coord)

    def act(self):
        if self.qlearn.prev_state is None or self.wait_time > 0:
            return
        if self.qlearn.prev_state[0] == State.NotHungry or self.qlearn.prev_state == State.PreyNotVisible:
            return
        occupants = grid.singleton_grid.get_occupants_in(self.position)
        for animat in occupants:
            if isinstance(animat, EPrey) and self.qlearn.chosen_action == State.PreyEasyClosest:
                print "Predator ID ", self.id
                grid.singleton_world.kill(animat)
                self.energy += 200
                # self.qlearn.doQLearning(self.get_reward(1), self.sense_state(self.__closest_animat()))
                break
            elif isinstance(animat, HPrey) and animat.energy <= self.energy and self.qlearn.chosen_action == State.PreyHardClosest:
                print "Predator ID ", self.id
                grid.singleton_world.kill(animat)
                self.energy += 400
                # self.qlearn.doQLearning(self.get_reward(2), self.sense_state(self.__closest_animat()))
                break
            elif isinstance(animat, HPrey) and animat.energy > self.energy and self.qlearn.chosen_action == State.PreyHardClosest:
                print "Predator ID ", self.id
                print "Hard prey fought back at ", animat.position
                # Both Predator and prey lose energy
                animat.energy -= 100
                self.energy -= 100
                # Predator waits for 10 seconds
                self.wait_time = 10
                # self.qlearn.doQLearning(self.get_reward(3), self.sense_state(self.__closest_animat()))
                break

    def get_reward(self,x):
        if x == 1:
            return 0.5
        elif x == 2:
            return 1
        else:
            return -1



# --- Return the state of the Animat
    def sense_state(self, closest_animat):

            list_state = []

            if closest_animat is None:
                list_state.append(State.PreyNotVisible)
            else:

                # Check Hunger
                if self.energy < self.hunger_threshold:
                    list_state.append(State.Hungry)
                else:
                    list_state.append(State.NotHungry)
                    return list_state

                if isinstance(closest_animat, EPrey):
                    list_state.append(State.PreyEasyClosest)
                else:
                    list_state.append(State.PreyHardClosest)
            return list_state

    def printqtable(self):
        print self.qlearn.table
# So Easy prey are killed. Hard Prey fight back.
# Predators on losing, must wait on spot, else they keep chasing hard prey continuously.