from Animat import *
from grid import *
from qlearning import *

class Environment:
    def __init__(self,width,height,num_eprey, num_hprey, num_predators):
        self.width = width
        self.height = height
        self.num_eprey = num_eprey
        self.num_hprey = num_hprey
        self.num_predators = num_predators

        # List to contain all animats
        self.eprey = []
        self.hprey = []
        self.predators = []

        # To Remember where animats are - Mark all empty
        self.markposition = [[0]*self.width]*self.height

        # To Remember where the grass is - Mark all empty
        self.markgrass = [[0]*self.width]*self.height

        # Add all animats to the environment
        self.add_animats()

        # Mark Grass
        self.mark_grassy()

        # We need to simulate the environment here.


# --- Sense state of the Animat
    def sense_state(self,x):    #x could be EPrey/HPrey/Predator
        if isinstance(x,EPrey) or isinstance(x,HPrey):
            i = 10 # Random statement to remove indent error
            # Check if on grass
            # Check energy levels
            # Check if being chased (auditory sensor)
            # Check energy level
        else :
            i = 10  # Random statement to remove indent error
            # Check if easy or hard prey in sight
            # Check if hungry
            # Check if cooperation is needed
        # Return a list of states that match
        return []



# --- Update Animat
    def update_animat(self,x):
        reward = -1
        xstate = []
        if isinstance(x,Predator):
            xstate = self.sense_state(x)
            lis = x.qlearn.chooseaction(xstate) # lis contains best action and it's qvalue
            # Update environment as well
            reward = self.energy_reward(lis[0])
            x.energy += reward
            x.age +=1
        else:
            #Make prey perform some action based on it's state
            x.age +=1
            x.energy -= 1
        x.qlearn.doQLearning(reward,xstate)



# --- Define reward for an action
    def energy_reward(self,a):
        if a == action.EatEPrey:
            return 200
        elif a == action.EatHPrey:
            return 500
        elif a == action.SignalHelp:
            return -10
        elif a == action.MoveRandomly:
            return -1
        elif a == action.TowardsSignal:
            return -1
        elif a == action.TowardsEasyPrey:
            return -1
        else:
            return -1



# --- Adds Animats to the Environment
    def add_animats(self):
         while self.num_eprey < len(self.eprey):
            self.pos = self.getposition()
            # Replace next line with either prey or predator
            self.eprey.append(EPrey(self.pos[0],self.pos[1]))
            self.markposition[self.pos[0]][self.pos[1]] = OccupantType.PREY_EASY

         # Add Hard Prey
         while self.num_hprey < len(self.hprey):
            self.pos = self.getposition()
            # Replace next line with either prey or predator
            self.hprey.append(HPrey(self.pos[0],self.pos[1]))
            self.markposition[self.pos[0]][self.pos[1]] = OccupantType.PREY_HARD

         # Add Predators
         while self.num_predators < len(self.predators):
            self.pos = self.getposition()
            # Replace next line with either prey or predator
            self.predators.append(Predator(self.pos[0],self.pos[1]))
            self.markposition[self.pos[0]][self.pos[1]] = OccupantType.PREDATOR


# --- Marks elements on the grid as grass
    def mark_grassy(self):

        # Let grasscount represent amount of grass needed
        grasscount = (self.width * self.height) / 2

        while True:
            temp = randint(0,self.width*self.height)
            column = temp % self.width
            row = temp / self.width
            if self.markgrass[row][column] == 0:    # Only set to grass if empty
                self.markgrass[row][column] = 1
                grasscount -=1
                if grasscount == 0:
                    return



# --- Returns grid position which is free
    def getposition(self):
        while True:
            temp = randint(0,self.width*self.height)
            column = temp % self.width
            row = temp / self.width
            if self.markposition[row][column] == 0: # Only return position if empty
                return row, column