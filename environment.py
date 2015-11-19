from Animat import *
from grid import *
from qlearning import *
import numpy



class Environment:
    def __init__(self, num_eprey, num_hprey, num_predators):
        self.width = config.grid_width()
        self.height = config.grid_height()
        self.num_eprey = num_eprey
        self.num_hprey = num_hprey
        self.num_predators = num_predators

        # List to contain all animats
        self.eprey = []
        self.hprey = []
        self.predators = []

        # To Remember where animats are - Mark all empty
        # How do you know which one was killed? Position or id?
        # self.markposition = [[0 for x in range(self.width)] for x in range(self.height)]
        self.markposition = numpy.zeros(shape=(self.height,self.width))

        # To Remember where the grass is - Mark all empty
        # self.markgrass = [[0 for x in range(self.width)] for x in range(self.height)]
        self.markgrass = numpy.zeros(shape=(self.height,self.width))

        # Mark Grass
        self.mark_grassy()
        print "Grass has been laid out!"

        # Add all animats to the environment
        self.add_animats()
        print "Animats added!"

        self.main_run()

    # Simulate enivronment
    def main_run(self):
        # Should take clock from the config file
        clock = 100000
        while clock > 0:
            for x in self.eprey:
                self.update_animat(x)
                if x.killed:
                    print "Easy prey killed!"
                    self.eprey.remove(x)

            for x in self.hprey:
                self.update_animat(x)
                if x.killed:
                    print "Hard prey killed!"
                    self.hprey.remove(x)

            for x in self.predators:
                self.update_animat(x)
                if x.killed:
                    print "Predator killed!"
                    self.predators.remove(x)
            clock -= 1
            # TODO - new generation to be created here
            # call self.initialise()



# -- Initialise the environment again
    def initialise(self):
        self.eprey = []
        self.hprey = []
        self.predators = []

        # To Remember where animats are - Mark all empty
        # How do you know which one was killed? Position or id?
        self.markposition = [[0]*self.width]*self.height

        # To Remember where the grass is - Mark all empty
        self.markgrass = [[0]*self.width]*self.height

        # Add all animats to the environment
        self.add_animats()

        # Mark Grass
        self.mark_grassy()





# --- Sense state of the Animat
    def sense_state(self,animat):
        if isinstance(animat,EPrey) or isinstance(animat,HPrey):
            animat.update_position()
            # If on grass and not being chased , update energy
            if self.markgrass[animat.position_x][animat.position_y] == 1 and animat.being_chased_x == -1:
                animat.energy +=2
            # Kill if low
            if animat.energy <= 0:
                animat.killed = True
        else :
            list_state = []

            # Check if predator has energy
            if animat.energy <= 0:
                    return list_state

            # Check if a prey is close
            if animat.prey_close(OccupantType.PREY_EASY,self.markposition):
                list_state.append(state.PreyEClose)
                return list_state
            if animat.prey_close(OccupantType.PREY_HARD,self.markposition):
                list_state.append(state.PreyHClose)
                return list_state

            # Check if easy or hard prey in sight
            if animat.prey_in_sight(OccupantType.PREY_EASY, self.markposition):
                list_state.append(state.PreyEasyVisible)
            if animat.prey_in_sight(OccupantType.PREY_HARD, self.markposition):
                list_state.append(state.PreyHardVisible)
            if OccupantType.PREY_EASY not in list_state and OccupantType.PREY_HARD not in list_state:
                list_state.append(state.PreyNotVisible)
                return list_state

            # Check Hunger
            if animat.energy < animat.hunger_threshold:
                list_state.append(state.Hungry)
            else:
                list_state.append(state.NotHungry)

            # TODO - check if cooperation is needed

            # Return a list of states that match
            return list_state


# --- Update Animat
    def update_animat(self,x):
        if isinstance(x,Predator):
            pred_state = self.sense_state(x)
            if pred_state == []:    # Predator has died
                x.killed = True
            lis = x.qlearn.chooseaction(pred_state) # lis contains best action and it's qvalue
            if lis == None:
                # print "No Action for undefined state!"
                return

            # Update environment as well
            if lis[0] == action.MoveRandomly:
                x.update_position()
            elif lis[0] == action.TowardsEasyPrey:
                x.chase_e_prey(self.eprey)
            elif lis[0] == action.TowardsHardPrey:
                x.chase_h_prey(self.hprey)
            elif lis[0] == action.EatEPrey:
                x.eat_e_prey(self.eprey)
            elif lis[0] == action.EatHPrey:
                x.eat_h_prey(self.hprey)
            elif lis[0] == action.SignalHelp:   # Signal for help
                pass
            else:   # Go towards signal
                pass
            reward = self.energy_reward(lis[0])
            x.energy += reward
            x.age +=1
            x.qlearn.doQLearning(reward,pred_state)
        else:
            x.age +=1
            x.energy -= 1
            self.sense_state(x)




# --- Define reward for an action
    def energy_reward(self,a):
        if a == action.MoveRandomly:
            return -20
        elif a == action.TowardsSignal:
            return -1
        elif a == action.TowardsEasyPrey:
            return -1
        else:
            return -1



# --- Adds Animats to the Environment
    def add_animats(self):
        while self.num_eprey > len(self.eprey):
            pos = self.getposition()
            # Replace next line with either prey or predator
            self.eprey.append(EPrey(pos[0],pos[1]))
            self.markposition[pos[0]][pos[1]] = OccupantType.PREY_EASY

        # Add Hard Prey
        while self.num_hprey > len(self.hprey):
            pos = self.getposition()
            # Replace next line with either prey or predator
            self.hprey.append(HPrey(pos[0],pos[1]))
            self.markposition[pos[0]][pos[1]] = OccupantType.PREY_HARD

        # Add Predators
        while self.num_predators > len(self.predators):
            pos = self.getposition()
            # Replace next line with either prey or predator
            self.predators.append(Predator(pos[0],pos[1]))
            self.markposition[pos[0]][pos[1]] = OccupantType.PREDATOR


# --- Marks elements on the grid as grass
    def mark_grassy(self):

        # Let grasscount represent amount of grass needed
        grasscount = (self.width * self.height) / 2

        while grasscount > 0:
            temp = randint(0,self.width*self.height-1)
            column = temp % self.width
            row = temp / self.width
            if self.markgrass[row][column] == 0:    # Only set to grass if empty
                self.markgrass[row][column] = 1
                #print row , column , self.markgrass[row][column]
                grasscount -=1
                if grasscount == 0:
                    break



# --- Returns grid position which is free
    def getposition(self):
        flag = False
        while not flag:
            temp = randint(0,self.width*self.height-1)
            column = temp % self.width
            row = temp / self.width
            if self.markposition[row][column] == 0: # Only return position if empty
                return row, column