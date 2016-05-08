from KNN_Algorithm import *
from DecisionTree_Algorithm_Resulting import *

DEFAULT_LABEL_INDEX = 0  

####################################  MAIN  ###################################

def main():
    #getResultsOfAllErrors_KNN_Algorithm(1, 15, plotting = True) # creates a graph and saves as PNG file
    printDecisionStump() # On training Data
    printDecisionTree() # On training Data
    resultsOfDecisionTree_Algorithm() 

################################  RUNNING SCOPE  ##############################

main()