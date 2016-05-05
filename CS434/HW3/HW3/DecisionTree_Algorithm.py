import math

###################################  READING DATA  ############################

def readDecisionTreeDataForHW3():
    trainingData = readDataset('knn_train.csv')
    testData = readDataset('knn_test.csv')
    return trainingData, testData 

######################################  ENTROPY  ##############################
 
def entropy(*pList):
    result = 0.0
    for p in pList:
        result -= p * math.log(p, 2)
    return result

##############################  ENTROPY FROM VALUES  ##########################
 
def entropyFromValues(*values):
    sum = 0.0
    for v in values:
        sum += v
    pList = [v/sum for v in values]
    return entropy(*pList)

##############################  MAIN FUNCTIONALITIES  #########################
