from animat import *


class State:
    PreyNotVisible = 0
    PreyEasyClosest = 1
    PreyHardClosest = 2
    Hungry = 3          # If energy below threshold
    NotHungry = 4       # If energy above threshold
    PredatorAskHelp = 5    # If Coordination is needed
    FollowSignal = 6


class Action:
    MoveRandomly = 0        # If chosen, move randomly
    TowardsEasyPrey = 1     # If chosen, then make animat move towards easy prey in the environment.
    TowardsHardPrey = 2     # If chosen, then make animat move towards hard prey in the environment.
    TowardsSignal = 3       # If chosen, move animat towards signal for help
    SignalForHelp = 4       # If chosen, then make animat signal for help


class QLearning:


    def __init__(self, epsilon=0.1, alpha=0.2, gamma=0.9):
        self.table = {}
        # Table is a dictionary with a mapping from states to actions, where one state can map to multiple actions.
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.prev_state = None
        self.prev_max_index = None
        self.current_action = None
        self.chosen_action = None
        self.settable()

# --- Initialise Q-table
    # Key is a list of states
    # Value is a list of actions followed by their q-values
    def settable(self):
        self.table[State.PreyNotVisible] = [Action.MoveRandomly, self.rand()]
        self.table[(State.Hungry, State.PreyEasyClosest)] = [Action.TowardsEasyPrey, self.rand(), Action.MoveRandomly, 0.2]
        self.table[(State.Hungry, State.PreyHardClosest)] = [Action.TowardsHardPrey, self.rand(),
                                                             Action.SignalForHelp, self.rand()]
        self.table[State.NotHungry] = [Action.MoveRandomly, self.rand()]
        self.table[(State.Hungry, State.FollowSignal)] = [Action.TowardsSignal, self.rand()]


# --- Choose Action with max Q value
    def choose_action(self, current_state):

        if len(current_state) == 1:
            self.current_action = self.table.get((current_state[0]))
        else:
            self.current_action = self.table.get(tuple(current_state))

        if self.current_action is None:
            return None

        # Iterating through current action and finding action with max value
        max_qvalue = -1
        max_index = 0
        index = 0
        while index < len(self.current_action)-1:
            if max_qvalue < self.current_action[index+1]:
                max_index = index
                max_qvalue = self.current_action[index+1]
            index += 2
        self.prev_state = current_state
        self.prev_max_index = max_index
        self.chosen_action = self.current_action[max_index]
        # Return best action and it's q weight
        return self.current_action[max_index], self.current_action[max_index+1]


# --- Perform Q Learning
    def doQLearning(self, reward, state):

        # For the first iteration of a generation!
        if self.prev_state is None:
            return

        prev_state = self.prev_state
        prev_action = self.current_action
        prev_max_index = self.prev_max_index

        # Find Qt-1
        oldq = prev_action[prev_max_index+1]

        # Find Qt
        newqtemp = self.choose_action(state)    # Contains best action and it's weight
        newq = newqtemp[1]  # Newq contains best/max weight

        # QLearning
        # Q(t-1) = Q(t-1) + alpha * [ r + (gamma * max(Q(t)) - Q(t-1) ]

        oldq += self.alpha*(reward+(self.gamma * newq)-oldq)  # Calculate newQ

        # print "Updated Q value ", oldq , newq
        # Update QValue and reflect in Table
        # print "Before", prev_state, prev_action
        prev_action[prev_max_index+1] = oldq
        # print "After", prev_action
        self.table[tuple(prev_state)] = prev_action


# --- Return Random weight from 0 to 1
    def rand(self):
        return random.uniform(0.0, 1.0)
