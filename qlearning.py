from animat import *


class State:
    PreyNotVisible = 0
    PreyEasyClosest = 1
    PreyHardClosest = 2
    Hungry = 3          # If energy below threshold
    NotHungry = 4       # If energy above threshold
    PredatorHelp = 5    # If Coordination is needed


class Action:
    MoveRandomly = 0        # If chosen, move randomly
    TowardsEasyPrey = 1     # If chosen, then make animat move towards easy prey in the environment.
    TowardsHardPrey = 2     # If chosen, then make animat move towards hard prey in the environment.
    TowardsSignal = 3       # If chosen, move animat towards signal for help
    SignalHelp = 4          # If chosen, then make animat signal for help


class QLearning:

    prev_state = None
    prev_max_index = None

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
        self.table[State.PreyNotVisible] = [Action.MoveRandomly, self.rand()]
        self.table[(State.Hungry,State.PreyEasyClosest)] = [Action.MoveRandomly, self.rand(), Action.TowardsEasyPrey,
                                                             self.rand()]
        self.table[(State.Hungry,State.PreyHardClosest)] = [Action.MoveRandomly, self.rand(),Action.TowardsHardPrey,
                                                              self.rand(), Action.SignalHelp ,self.rand()]
        self.table[State.NotHungry] = [Action.MoveRandomly, self.rand()]
        # self.table[State.PredatorHelp] = [Action.MoveRandomly, self.rand() , Action.TowardsSignal, self.rand()]


# --- Choose Action with max Q value
    def choose_action(self, current_state):

        if len(current_state) == 1:
            current_action = self.table.get((current_state[0]))
        else:
            current_action = self.table.get(tuple(current_state))

        if current_action is None:
            return None

        # Iterating through current action and finding action with max value
        max_qvalue = -1
        max_index = 0
        index = 0
        while index < len(current_action)-1:
            if max_qvalue < current_action[index+1]:
                max_index = index
                max_qvalue = current_action[index+1]
            index += 2
        self.prev_state = current_state
        self.prev_max_index = max_index

        # Return best action and it's q weight
        return current_action[max_index], current_action[max_index+1]


# --- Perform Q Learning
    def doQLearning(self,reward,state):

        if len(self.prev_state) == 1:
            prev_action_row = self.table.get((self.prev_state[0]))
        else:
            prev_action_row = self.table.get(tuple(self.prev_state))
        # Retrieve previous row of actions for previous state

        # Find Qt-1
        oldq = prev_action_row[self.prev_max_index-1]  # prev_maxindex remembers where the previous Q value

        # Find Qt
        newqtemp = self.choose_action(state)    # Contains best action and it's weight
        newq = newqtemp[1]  # Newq contains best weight

        # QLdeearning
        newq = self.alpha*(reward+(self.gamma * newq)-oldq)  # Calculate newQ

        # print "Updated Q value " , oldq , newq
        # Update QValue and reflect in Table
        prev_action_row[self.prev_max_index-1] = newq
        self.table[tuple(self.prev_state)] = prev_action_row


# --- Return Random weight from 0 to 1
    def rand(self):
        return random.uniform(0.0, 1.0)
