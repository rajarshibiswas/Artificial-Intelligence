# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        for iter in xrange(self.iterations): # Run the specifed number of iterations
            temp_state = util.Counter() # A temp dict
            for state in self.mdp.getStates(): # Get the mdp states
                if not self.mdp.isTerminal(state): # Compute only for non-terminal states
                    q_vals = util.Counter()
                    # iterate over the possible actions
                    for action in self.mdp.getPossibleActions(state):
                        q_vals[action] = self.getQValue(state, action)
                    temp_state[state] = max(q_vals.values()) # Choose the best one
            self.values = temp_state.copy()




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        Q_value = 0 # will store the computed q value here
        transition_states_probs =  self.mdp.getTransitionStatesAndProbs(state, action)
        # iterate over all the trastition states
        for state_prob in transition_states_probs:
            next_state = state_prob[0] # next state
            prob = state_prob[1] # probability
            reward = self.mdp.getReward(state, action, next_state) # Get the reward
            # compute the Q value
            Q_value += prob * (reward + self.discount * self.values[next_state])
        return Q_value # return the computed q value
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        if self.mdp.isTerminal(state): # if state is terminal return NONE
            return None
        # get the action
        possible_action = self.mdp.getPossibleActions(state)
        if (len(possible_action) == 0):
            return None
        act_val = util.Counter() # temp dict to compute
        for action in possible_action:
            # get the q values
            act_val[action] = self.computeQValueFromValues(state, action)
        return act_val.argMax() # return the best
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
