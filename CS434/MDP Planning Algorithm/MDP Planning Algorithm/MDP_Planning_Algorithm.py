import math 

class MDP_Planning_Algorithm:
    def __init__(self, testData, beta):
        self.stateNumber = testData['stateNumber']
        self.actionNumber = testData['actionNumber']
        self.transitionFunctions = testData['transitionFunctions']
        self.rewards = testData['rewards']
        self.beta = beta 
        self.delta = self.calculateDelta(beta)

    def calculateDelta(self, beta):   
        epsilon = math.pow(math.e, -10)
        return (epsilon * ((1 - beta) ** 2))/(2 * (beta **2 ))

    def reward(self, state):   
        return self.rewards[state]

    def transition(self, state, action, nextState):
        return self.transitionFunctions[action][state][nextState]
    
    def maxSumT_U(self, state, iteration):
        value, optimalAction = float('-inf'), 0     
        for action in range(self.actionNumber):
            sum = 0
            for nextState in range(self.stateNumber):
                sum += self.transition(state, action, nextState) * self.utilityValue(nextState, iteration-1)[0]
            if sum > value:
                value, optimalAction = sum, action  
        return (value, optimalAction)

    def utilityValue(self, state, iteration): 
        if iteration <= 1: 
            return (self.reward(state), 0)
        else:
            (value, optimalAction) = self.maxSumT_U(state, iteration)[0]
            return ((self.reward(state) + self.beta * value), optimalAction)

    def optimalUtilityValue(self, state): 
        difference, (iteration, optimalAction) = float('inf'), (1, 0)
        (previousUtility, previousAction) = self.utilityValue(state, iteration)   
        while True:
            iteration += 1
            (utility, action) = self.utilityValue(state, iteration)
            difference = abs(utility - previousUtility)
            if difference < self.delta:
                break
            else:
                (previousUtility, previousAction) = (utility, action)
        return (previousUtility, previousAction)

    def valueIterationAlgorithm(self): 
        optimalUtilityVector, policyVector = [], []
        for state in range(self.stateNumber):
            (optimalUtility, optimalAction) = self.optimalUtilityValue(state)
            optimalUtilityVector.append(optimalUtility)
            policyVector.append(optimalAction)
        return optimalUtilityVector, policyVector