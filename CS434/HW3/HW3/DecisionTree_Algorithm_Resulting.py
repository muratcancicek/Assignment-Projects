
from CommonTools import *
from KNN_Algorithm import *
from DecisionTreeNode import * 
from DecisionTree_Algorithm import * 
#execfile('HW3.py')

########################  GETTING RESULTS OF DECISION TREE  ###################

def getResultsOfDecisionTree(trainingData, testData, buildAllTree):
    root = DecisionTreeNode(trainingData)
    if buildAllTree:
        root.buildAllTree()
    else:
        root.buildDecisionStump()
    return countErrorsOfDecisionTree(root, testData)

##############################  MAIN FUNCTIONALITIES  #########################

def resultsOfDecisionTree_Algorithm():
    trainingData, testData = readDecisionTreeDataForHW3()
    errorsOfDecisionStump = getResultsOfDecisionTree(trainingData, trainingData, False)
    print '\nIn', len(trainingData), 'instances, Error Count of Decision Stump on Training Data =', errorsOfDecisionStump

    errorsOfDecisionStump = getResultsOfDecisionTree(trainingData, testData, False)
    print '\nIn', len(testData), 'instances, Error Count of Decision Stump on Test Data =', errorsOfDecisionStump

    errorsOfDecisionStump = getResultsOfDecisionTree(trainingData, trainingData, True)
    print '\nIn', len(trainingData), 'instances, Error Count of Decision Tree on Training Data =', errorsOfDecisionStump

    errorsOfDecisionStump = getResultsOfDecisionTree(trainingData, testData, True)
    print '\nIn', len(testData), 'instances, Error Count of Decision Tree on Test Data =', errorsOfDecisionStump
    
#########################  PRINTING DECISION TREE  ####################### 

def printDecisionTree():
    trainingData, testData = readDecisionTreeDataForHW3()
    root = DecisionTreeNode(trainingData)
    root.buildAllTree()
    print '\nDecision Tree:\n'
    root.printTree()

#########################  PRINTING DECISION STUMP  ####################### 

def printDecisionStump():
    trainingData, testData = readDecisionTreeDataForHW3()
    root = DecisionTreeNode(trainingData)
    root.buildDecisionStump()
    print '\nDecision Stump:\n'
    root.printTree()
