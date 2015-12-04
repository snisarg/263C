import random
from qlearning import *
import config
import grid
import math


def random_walk():
    return [random.randint(-1, 1), random.randint(-1, 1)]


# TODO Toroidal differences not accurate.
def distance_diff(reference, target, vision_range):
    # print (reference, target)
    height = -reference[0]+target[0]
    width = -reference[1]+target[1]
    if abs(height) > vision_range:
        height += 2 * reference[0]
    if abs(width) > vision_range:
        width += 2 * reference[1]
    height_multiplier = 1
    width_multiplier = 1
    if height < 0:
        height_multiplier = -1
    if width < 0:
        width_multiplier = -1
    height %= (vision_range + 1) % config.grid_height()
    width %= (vision_range + 1) % config.grid_width()
    return [height * height_multiplier, width * width_multiplier]


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


# --- Easy Prey class def
class EPrey(Animat):

    def __init__(self, x, y):
        Animat.__init__(self)
        self.position = [x, y]
        self.energy = random.randint(400, 500)

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
                        if not (diff[0] == 0 and diff[1] == 0):
                            step_calc.add(diff)

        if not step_calc.get_count() == 0:
            coord = step_calc.get_decision()
        else:
            # Nothing in site, random walk.
            coord = random_walk()
            while grid.singleton_grid.is_obstacle(coord):
                coord = random_walk()

        grid.singleton_world.move_animat(self, coord)


class HPrey(Animat):

    def __init__(self, x, y):
        Animat.__init__(self)
        self.position = [x, y]
        self.energy = random.randint(1000, 1200)

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
                        if not (diff[0] == 0 and diff[1] == 0):
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

    def __init__(self, x, y):
        Animat.__init__(self)
        self.position = [x, y]
        self.energy = random.randint(600, 1000)
        self.hunger_threshold = 1000
        self.wait_time = 0
        self.making_signal = False  # Internal neuron

    # Returns prey closest to predator's positions OR closest predator making signal for help!
    def __closest_animat(self):
        closest_animats = grid.singleton_world.around_point(self.position, config.predator_range())
        for level in closest_animats:
            for block in level:
                for anim in block:
                    if isinstance(anim, EPrey) or isinstance(anim, HPrey):
                        return anim  # Return the anim object which is closest
                    elif isinstance(anim, Predator) and anim.making_signal is True:
                        return anim
        return None

    def move(self, game_clock):
        if game_clock % (config.predator_speed() + 1) == 0:
            return

        # If predator has lost to the hard prey, make him move randomly until wait_time = 0
        if self.wait_time > 0:
            self.making_signal = False
            return

        anim = self.__closest_animat()
        if anim is None:
            coord = None
        else:
            coord = anim.position

        current_state = self.sense_state(anim)
        current_action = self.qlearn.choose_action(current_state)

        if current_action[0] == Action.MoveRandomly:
            # print "Move randomly!"
            coord = random_walk()
            while grid.singleton_grid.is_obstacle(coord):
                coord = random_walk()
                self.making_signal = False

        elif current_action[0] == Action.TowardsEasyPrey or current_action[0] == Action.TowardsHardPrey:
            # print "Chased prey!"
            coord = normalise_distance(
                distance_diff(self.position, coord, config.predator_range()), config.predator_range())
            self.making_signal = False

        elif current_action[0] == Action.SignalForHelp:
            print "Need help at ", self.position, "chasing ", coord
            coord = normalise_distance(
                distance_diff(self.position, coord, config.predator_range()), config.predator_range())
            # Signal for help!
            self.making_signal = True

        elif current_action[0] == Action.TowardsSignal:
            print "HELPING ", coord , self.position
            coord = normalise_distance(
                distance_diff(self.position, coord, config.predator_range()), config.predator_range())
            self.making_signal = False

        grid.singleton_world.move_animat(self, coord)

# -- Battle between two animats is done here!
    def act(self):
        occupants = grid.singleton_grid.get_occupants_in(self.position)
        for animat in occupants:
            if isinstance(animat, EPrey):
                reward = self.reward(animat)
                self.update_energy(200)
                grid.singleton_world.kill(animat)
                # self.qlearn.doQLearning(reward, self.sense_state(self.__closest_animat()))
                self.making_signal = False

            elif isinstance(animat, HPrey):
                if self.energy > animat.energy:
                    reward = self.reward(animat)
                    self.update_energy(400)
                    grid.singleton_world.kill(animat)
                    # self.qlearn.doQLearning(reward, self.sense_state(self.__closest_animat()))
                    self.making_signal = False

                elif self.energy <= animat.energy and self.wait_time == 0:
                    print "Hard fights back at ", animat.position
                    # Both predator and prey lose energy
                    self.update_energy(-100)
                    animat.energy -= 300

                    # Must wait before chasing again
                    self.wait_time = 10
                    reward = 0
                    # self.qlearn.doQLearning(reward, self.sense_state(self.__closest_animat()))
                    self.making_signal = False


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

                if isinstance(closest_animat, Predator):
                    list_state.append(State.FollowSignal)
                elif isinstance(closest_animat, EPrey):
                    list_state.append(State.PreyEasyClosest)
                elif isinstance(closest_animat, HPrey) and self.making_signal is False:
                    list_state.append(State.PreyHardClosest)
                elif isinstance(closest_animat, HPrey) and self.making_signal is True:
                    list_state.append(State.PredatorAskHelp)
            return list_state

    def update_energy(self, amount):
        self.energy += amount

    def reduce_wait(self):
        if self.wait_time > 0:
            self.wait_time -= 1

    def reward(self, animat):
        if isinstance(animat, EPrey):
            return 0.5
        else:
            return 1
