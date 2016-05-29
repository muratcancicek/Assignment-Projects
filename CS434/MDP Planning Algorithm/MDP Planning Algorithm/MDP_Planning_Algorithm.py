import math 

class MDP_Planning_Algorithm:
    def __init__(self, testData, beta):
        self.stateNumber = testData['stateNumber']
        self.actionNumber = testData['actionNumber']
        self.transitionFunctions = list(testData['transitionFunctions'])
        self.rewards = list(testData['rewards'])
        self.utilityVector = None
        self.beta = beta 
        self.delta = self.calculateDelta(beta)

    def calculateDelta(self, beta):   
        epsilon = math.pow(math.e, -10)
        return (epsilon * ((1 - beta) ** 2))/(2 * (beta **2 ))

    def reward(self, state):   
        return self.rewards[state]

    def transition(self, state, action, nextState):
        return self.transitionFunctions[action][state][nextState]
    
    def utilityValue(self, state): 
        return self.utilityVector[state]
    
    def sumT_U(self, state, action):
        sum = 0
        for nextState in range(self.stateNumber):
            sum += self.transition(state, action, nextState) * self.utilityValue(nextState)
        return sum

    def maxSumT_U(self, state):
        return max([self.sumT_U(state, action) for action in range(self.actionNumber)])

    def valueIterationAlgorithm(self): 
        self.utilityVector, utilityVectorPrime = list(self.rewards), list(self.rewards)
        while True:
            self.utilityVector = list(utilityVectorPrime)
            for state in range(self.stateNumber):
                utilityVectorPrime[state] = self.reward(state) + self.beta * self.maxSumT_U(state)
            maxD = max([abs(U - Up) for (U, Up) in zip(self.utilityVector, utilityVectorPrime)])
            if maxD < self.delta:
                break
        return self.utilityVector
    
    def argmaxSumT_U(self, state):
        maximumSum, optimalAction = float('-inf'), 0 
        for action in range(self.actionNumber):
            sum = self.sumT_U(state, action)
            if sum > maximumSum:
                maximumSum, optimalAction = sum, action
        return optimalAction

    def getPolicyVector(self): 
        if self.utilityValue == None:
            self.valueIterationAlgorithm()
        return [self.argmaxSumT_U(state)+1 for state in range(self.stateNumber)]