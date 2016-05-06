import math 
from CommonTools import *
from Monk import *
from DecisionCondition import *

###################################  READING DATA  ############################

def readDecisionTreeDataForHW3():
    trainingData = readDataset('monks-1-train.csv')
    trainingData = [Monk(row) for row in trainingData]
    testData = readDataset('monks-1-test.csv')
    testData = [Monk(row) for row in testData]
    return trainingData, testData 

#############################  VALUES COUNTS OF FEATURES  #####################
 
def getValueCountsForMonkFeatures(): # Hard coded, values from the assignment description
    return [3, 3, 2, 3, 4, 2]

######################################  ENTROPY  ##############################
 
def entropy(*pList):
    result = 0.0
    for p in pList:
        if p != 0:
            result -= p * math.log(p, 2)
    return result

##############################  ENTROPY FROM VALUES  ##########################
 
def entropyFromValues(*values):
    sum = 0.0
    for v in values:
        sum += v
    pList = [v/sum for v in values]
    return entropy(*pList)

##############################  COUNTING POSITIVES  ###########################
 
def countPositives(monkList):
    count = 0
    for monk in monkList:
        count += monk.classLabel 
    return count

##############################  COUNTING NEGATIVES  ###########################
 
def countNegatives(monkList):
    count = len(monkList)
    for monk in monkList:
        count -= monk.classLabel 
    return count

#################################  ALL CONDITIONS  ############################

def getAllConditions():
    conditions = []
    valueCounts = getValueCountsForMonkFeatures()
    for i in range(len(valueCounts)):
        count = valueCounts[i]
        for value in range(1, count+1):
            condition = DecisionCondition(VALUE_CHECKING, i, value)
            conditions.append(condition)
    for i in range(len(valueCounts)-1):
        for j in range(i+1, len(valueCounts)):
            condition = DecisionCondition(FEATURE_CHECKING, i, j)
            conditions.append(condition)
    return conditions

##############################  MAIN FUNCTIONALITIES  #########################
