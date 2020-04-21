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

# Name: Saumya Jain
# CS3600

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
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        #Going through iterations
        for x in range (0, iterations):
            values = self.values.copy()

            #Going through states
            for state in mdp.getStates():

                #Variable established for keeping track of maximum
                maxNum = None
                #Going through all the actions for a state
                for action in mdp.getPossibleActions(state):
                    count = 0
                    for (ns, p) in mdp.getTransitionStatesAndProbs(state, action):
                        #calculate value and increment count
                        r = mdp.getReward(state, action, ns)
                        v = self.values[ns]
                        count += p * (r + v * discount)

                    #Change value of maxNum if needed    
                    maxNum = max(maxNum, count)
                
                if mdp.isTerminal(state):
                    values[state] = 0
                else:
                    values[state] = maxNum
            self.values = values


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
        count = 0

        for (ns, p) in self.mdp.getTransitionStatesAndProbs(state, action):
            #Calculate value and increment count
            r = self.mdp.getReward(state, action, ns)
            v = self.values[ns]
            count += p * (r + v * self.discount)
        return count
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
        bestActionOfState = (None, None)

        #Going through the possible actions of state
        for action in self.mdp.getPossibleActions(state):
            qVal = self.getQValue(state, action)

            #Checking if bestActionOfState needs to be changed according to qVal
            if bestActionOfState[1] == None or qVal > bestActionOfState[1]:
                bestActionOfState = (action, qVal)
                
        return bestActionOfState[0]
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
