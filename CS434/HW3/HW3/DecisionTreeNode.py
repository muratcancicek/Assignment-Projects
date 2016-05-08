from DecisionTree_Algorithm import *

TRUE_CHILD = 'TRUE-CHILD'
FALSE_CHILD = 'FALSE-CHILD'


class DecisionTreeNode(object):
    def __init__(self, *args):
        if len(args) == 1: # monkList 
            self.set = args[0]
            self.positives = countPositives(args[0])
            self.negatives = countNegatives(args[0])
            self.probability = 1
            self.depth = 0
        #if len(args) == 2: # monkList, probability 
        #    self.set = args[0]
        #    self.positives = countPositives(args[0])
        #    self.negatives = countNegatives(args[0])
        #    self.probability = args[1]
        elif len(args) == 3: # monkList, probability, depth 
            self.set = args[0]
            self.positives = countPositives(args[0])
            self.negatives = countNegatives(args[0])
            self.probability = args[1]
            self.depth = args[2]+1
        self.entropyValue = entropyFromValues(self.positives, self.negatives)
        self.leftChild = None
        self.rightChild = None
        self.maxGain = None
        self.condition = None

    def predict(self, monk):
        if self.getChildren() != []:
            if self.condition(monk):
                return self.leftChild.predict(monk)
            else:
                return self.rightChild.predict(monk)
        else:
           return 1 if self.positives > self.negatives else 0

    def buildAllTree(self):
        if self.positives > 0 and self.negatives > 0:
        #if self.maxGain < 0.9:
            self.buildDecisionStump()
            if self.leftChild != None:
                self.leftChild.buildAllTree()
            if self.rightChild != None:
                self.rightChild.buildAllTree()

    def splitBy(self, condition):
        trueSet, falseSet = [], []
        for monk in self.set:
            if condition(monk):
                trueSet.append(monk)
            else:
                falseSet.append(monk)
        if trueSet != []:
            self.leftChild = DecisionTreeNode(trueSet, float(len(trueSet))/len(self.set), self.depth)
        if falseSet != []:
            self.rightChild = DecisionTreeNode(falseSet, float(len(falseSet))/len(self.set), self.depth)
        
    def buildDecisionStump(self):
        self.findBestCondition()
        self.splitBy(self.condition)

    def findBestCondition(self): 
        conditions = getAllConditions()
        self.condition, self.maxGain = conditions[0], 0
        for condition in conditions:
            self.leftChild, self.rightChild = None, None
            self.splitBy(condition)
            gain = self.getInformationGain()            
            if gain > self.maxGain:
                self.condition, self.maxGain = condition, gain
        self.leftChild, self.rightChild = None, None
        return self.condition

    def getChildren(self):
        children = []
        if self.leftChild != None:
            children.append(self.leftChild)
        if self.rightChild != None:
            children.append(self.rightChild)
        return children
        
    def getInformationGain(self):
        result = self.entropyValue
        for child in self.getChildren():
            result -= child.probability * child.entropyValue
        return result

    def printTree(self, childTag = 'ROOT:'):
        print self.depth * '\t' + childTag, self.NodeLike()
        if self.rightChild != None:
            self.rightChild.printTree('RIGHT CHILD:')
        if self.leftChild != None:
            self.leftChild.printTree('LEFT CHILD:')

    def NodeLike(self):
         return "[" + str(self.positives) + ', ' + str(self.negatives) + ']' + \
            (' TEST: '+ str(self.condition) if self.condition != None else '') + \
            ' | G = ' + ("{0:.2f}".format(self.maxGain) if self.maxGain != None else '1')

    def __my_str__(self):
     return "+:" + str(self.positives) + ' -:' + str(self.negatives) + ' | ' + str(self.condition) + \
         ' | Ent. = ' + "{0:.2f}".format(self.entropyValue) + ' | P = ' + \
         "{0:.2f}".format(self.probability) + \
         (' | G = ' + ("{0:.2f}".format(self.maxGain)) if self.maxGain != None else '')
    def __str__(self):
        return self.__my_str__()
    def __repr__(self):
        return self.__my_str__()