from DecisionTree_Algorithm import *

class DecisionTreeNode(object):
    def __init__(self, positives, negatives):
        self.positives = positives
        self.negatives = negatives
        self.entropyValue = entropyFromValues(self.positives, self.negatives)
        self.children = []

        
    def addChild(self, child, p):
        child = [p, child]
        self.children.append(child)
        
    def getInformationGain(self):
        result = self.entropyValue
        for child in self.children:
            p, child = child
            result -= p * child.entropyValue
        return result

    def __str__(self):
     return str(self.positives) + ' | ' + str(self.negatives) + ' | Entropy = ' + str(self.entropyValue)
    def __repr__(self):
        return str(self.positives) + ' | ' + str(self.negatives) + ' | Entropy = ' + str(self.entropyValue)