import inspect
from CommonTools import *
from KNN_Algorithm import *
from DecisionTree_Algorithm import *
from DecisionTreeNode import *
#execfile('HW3.py')

DEFAULT_LABEL_INDEX = 0  

####################################  MAIN  ###################################

def main():
    #getResultsOfAllErrors_KNN_Algorithm(1, 15, plotting = True)
    #s, s1, s2 = DecisionTreeNode(26, 7), DecisionTreeNode(21, 3), DecisionTreeNode(5, 4)
    #s.addChild(s1, 24.0/33)
    #s.addChild(s2, 9.0/33)  b  
    trainingData, testData = readDecisionTreeDataForHW3()

    conditions = getAllConditions()
    s = DecisionTreeNode(trainingData)
    bestCondition = s.findBestCondition(conditions)
    print '\n', bestCondition
    print '\n', s.getInformationGain()

    #monk = Monk([0,1,2,2,2,3,2])
    #for condition in conditions:
    #    print condition
    #    print condition(monk)

################################  RUNNING SCOPE  ##############################

main()