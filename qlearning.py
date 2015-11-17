import random

class state:
    PreyNotVisible = 0
    PreyEasyVisible = 1
    PreyHardVisible = 2
    PreyBothVisible = 3
    Hungry = 4          #If energy below threshold
    NotHungry = 5       #If energy above threshold
    PreyEClose = 6       #Prey close enough to be eaten
    PreyHClose = 7
    PredatorHelp = 8    #If Coordination is needed

    #Number of states = 9

class action:
    MoveRandomly = 0        #If chosen, move randomly
    TowardsEasyPrey = 1     #If chosen, then make animat move towards easy prey in the environment.

    TowardsHardPrey = 2     #If chosen, then make animat move towards hard prey in the environment.
    TowardsSignal = 3       #If chosen, move animat towards signal for help
    EatEPrey = 4             #If chosen, eat prey
    EatHPrey = 5
    SignalHelp = 6          #If chosen, then make animat signal for help

    #Number of actions = 7


#--- Future replacement for Table entries
class actionValue:

    def __init__(self,x,y):
        self.action = action()
        self.value = y


class QLearning:

    prev_state = None
    prev_maxindex = None


    def __init__(self, epsilon=0.1, alpha=0.2, gamma=0.9):
        self.table = {}
        # Table is a dictionary with a mapping from states to actions, where one state can map to multiple actions.
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.settable()

#--- Initialise Q-table
    # Key is a list of states
    # Value is a list of actions followed by their q-values
    def settable(self):
        self.table[state.PreyNotVisible] = [action.MoveRandomly, self.rand()]
        self.table[(state.PreyEasyVisible, state.Hungry)] = [action.MoveRandomly, self.rand(), action.TowardsEasyPrey,
                                                             self.rand(), action.SignalHelp, self.rand()]
        self.table[(state.PreyHardVisible, state.Hungry)] = [action.MoveRandomly, self.rand(),action.TowardsHardPrey,
                                                              self.rand(), action.SignalHelp ,self.rand()]
        self.table[(state.PreyHardVisible, state.NotHungry)] = [action.MoveRandomly, self.rand()]
        self.table[(state.PreyEasyVisible, state.NotHungry)] = [action.MoveRandomly, self.rand()]
        self.table[(state.PreyEasyVisible, state.PreyHardVisible, state.Hungry)] = [action.TowardsEasyPrey,self.rand(),
                                    action.TowardsHardPrey,self.rand(),action.SignalHelp,self.rand()]
        self.table[state.PreyEClose] = [action.EatEPrey, self.rand()]
        self.table[state.PreyHClose] = [action.EatHPrey, self.rand()]
        self.table[state.PredatorHelp] = [action.MoveRandomly, self.rand() , action.TowardsSignal, self.rand()]



#--- Choose Action with max Q value
    def chooseaction(self,current_state):
        if self.table.has_key(current_state):
            current_action = self.table.get(current_state,default=None)
        else:
            print "Unrecognised state!"
            return None

        #Iterating through current action and finding action with max value
        maxqvalue = -1
        maxindex = 0
        for index in range(len(current_action)-1) :
            if maxqvalue < current_action[index+1] :
                maxindex = index
                maxqvalue = current_action[index+1]
            index += 2
        self.prev_state = current_state
        self.prev_maxindex = maxindex

        #Return best action and it's q weight
        return current_action[maxindex - 1], current_action[maxindex]



#--- Perform Q Learning
    def doQLearning(self,reward,state):

        # Retrieve previous row of actions for previous state
        prev_action_row = self.table.get(self.prev_state,default = None)

        # Find Qt-1
        oldq = prev_action_row[self.prev_maxindex]  # prev_maxindex remembers where the previous Q value

        # Find Qt
        newqtemp = self.chooseaction(state)    # Contains best action and it's weight
        newq = newqtemp[1]  # Newq contains best weight

        # Qlearning
        newq = self.alpha*(reward+(self.gamma * newq)-oldq)  #Calculate newQ

        #Update QValue and reflect in Table
        prev_action_row[self.prev_maxindex] = newq
        self.table[self.prev_state] = prev_action_row


#--- Return Random weight from 0 to 1
    def rand(self):
        return random.uniform(0.0,1.0)
