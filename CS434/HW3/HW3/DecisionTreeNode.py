from DecisionTree_Algorithm import *

class DecisionTreeNode(object):
    def __init__(self, *args):
        if len(args) == 1: # monkList 
            self.set = args[0]
            self.positives = countPositives(args[0])
            self.negatives = countNegatives(args[0])
            self.probability = 1
        if len(args) == 2: # monkList, probability 
            self.set = args[0]
            self.positives = countPositives(args[0])
            self.negatives = countNegatives(args[0])
            self.probability = args[1]
        elif len(args) == 3: # positives, negatives, probability
            self.positives = args[0]
            self.negatives = args[1]
            self.probability = args[2]
        self.entropyValue = entropyFromValues(self.positives, self.negatives)
        self.children = []

    def makeChildren(self, condition):
        trueSet, falseSet = [], []
        for monk in self.set:
            if condition(monk):
                trueSet.append(monk)
            else:
                falseSet.append(monk)
        trueChild = DecisionTreeNode(trueSet, float(len(trueSet))/len(self.set))
        falseChild = DecisionTreeNode(falseSet, float(len(falseSet))/len(self.set))
        self.children.extend([trueChild, falseChild])
        
    def findBestCondition(self, conditions): 
        bestCondition, maxGain = conditions[0], 0
        for condition in conditions:
            self.children = []
            self.makeChildren(condition)
            gain = self.getInformationGain()
            print gain, maxGain
            if gain >= maxGain:
                bestCondition, maxGain = condition, gain
        self.children = []
        self.makeChildren(bestCondition)
        return bestCondition

    def addChild(self, child):
        self.children.append(child)
        
    def getInformationGain(self):
        result = self.entropyValue
        for child in self.children:
            result -= child.probability * child.entropyValue
        return result

    def __str__(self):
     return str(self.positives) + ' | ' + str(self.negatives) + ' | Entropy = ' + str(self.entropyValue) + ' | Probability = ' + str(self.probability)
    def __repr__(self):
        return str(self.positives) + ' | ' + str(self.negatives) + ' | Entropy = ' + str(self.entropyValue) + ' | Probability = ' + str(self.probability)