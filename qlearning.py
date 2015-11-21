import random


class state:
    PreyNotVisible = 0
    PreyEasyVisible = 1
    PreyHardVisible = 2
    Hungry = 3          # If energy below threshold
    NotHungry = 4       # If energy above threshold
    PreyEClose = 5       # Prey close enough to be eaten
    PreyHClose = 6
    PredatorHelp = 7    # If Coordination is needed

    # Number of states = 8

class action:
    MoveRandomly = 0        # If chosen, move randomly
    TowardsEasyPrey = 1     # If chosen, then make animat move towards easy prey in the environment.
    TowardsHardPrey = 2     # If chosen, then make animat move towards hard prey in the environment.
    TowardsSignal = 3       # If chosen, move animat towards signal for help
    EatEPrey = 4             # If chosen, eat prey
    EatHPrey = 5
    SignalHelp = 6          # If chosen, then make animat signal for help

    # Number of actions = 7


# --- Future replacement for Table entries
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

# --- Initialise Q-table
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
                                    action.TowardsHardPrey,self.rand()]
        self.table[(state.PreyEasyVisible, state.PreyHardVisible, state.NotHungry)] = [action.MoveRandomly, self.rand()]
        self.table[(state.PreyEClose, state.Hungry)] = [action.EatEPrey, self.rand()]
        self.table[(state.PreyEClose, state.NotHungry)] = [action.MoveRandomly, self.rand()]
        self.table[(state.PreyHClose, state.Hungry)] = [action.EatHPrey, self.rand()]
        self.table[(state.PreyHClose, state.NotHungry)] = [action.MoveRandomly, self.rand()]
        self.table[state.PredatorHelp] = [action.MoveRandomly, self.rand() , action.TowardsSignal, self.rand()]


# --- Choose Action with max Q value
    def chooseaction(self,current_state):

        if len(current_state) == 1:
            current_action = self.table.get((current_state[0]))
        else:
            current_action = self.table.get(tuple(current_state))

        # print "State " , current_state
        # print "Action " , current_action


        if current_action == None:
            # print "Unexpected state! " , current_state
            return
        # Iterating through current action and finding action with max value
        maxqvalue = -1
        maxindex = 0
        index = 0
        while index < len(current_action)-1 :
            if maxqvalue < current_action[index+1] :
                maxindex = index
                maxqvalue = current_action[index+1]
            index += 2
        self.prev_state = current_state
        self.prev_maxindex = maxindex

        # Return best action and it's q weight
        return (current_action[maxindex], current_action[maxindex+1])



# --- Perform Q Learning
    def doQLearning(self,reward,state):

        if len(self.prev_state) == 1:
            prev_action_row = self.table.get((self.prev_state[0]))
        else:
            prev_action_row = self.table.get(tuple(self.prev_state))
        # Retrieve previous row of actions for previous state


        # Find Qt-1
        oldq = prev_action_row[self.prev_maxindex-1]  # prev_maxindex remembers where the previous Q value

        # Find Qt
        newqtemp = self.chooseaction(state)    # Contains best action and it's weight
        newq = newqtemp[1]  # Newq contains best weight

        # Qlearning
        newq = self.alpha*(reward+(self.gamma * newq)-oldq)  # Calculate newQ

        # print "Updated Q value " , oldq , newq
        # Update QValue and reflect in Table
        prev_action_row[self.prev_maxindex-1] = newq
        self.table[tuple(self.prev_state)] = prev_action_row


# --- Return Random weight from 0 to 1
    def rand(self):
        return random.uniform(0.0,1.0)
