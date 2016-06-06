from KaggleTutorial import * 
from CommonTools import *
from Algorithms import *
from myScript import *
import pandas as pd

#    execfile('main.py')

################################  main  #######################################

def main():
    #writeNewTrain('train.csv', 'sampledTrain7.csv', 'sampledTest7.csv') if i != 2
    indices = [i for i in range(9)]
    #runAlgorithm(logisticRegressionMethod, 'sampledTrain7.csv', 'sampledTest7.csv', 'sampledSubmissionBinary.csv', indices, indices, False)
    #runAlgorithm(linearRegressionMethod, 'sampledTrain7.csv', 'sampledTest7.csv', 'sampledSubmissionBinary.csv', indices, indices, False)
    runAlgorithm(logisticRegressionMethod, 'sampledTrain7.csv', 'sampledTest7.csv', 'sampledSubmissionBinary.csv', indices, indices, True)
    runAlgorithm(linearRegressionMethod, 'sampledTrain7.csv', 'sampledTest7.csv', 'sampledSubmissionBinary.csv', indices, indices, True)
    #runAlgorithm(randomForestMethod, 'sampledTrain7.csv', 'sampledTest7.csv', 'sampledSubmissionBinary.csv', indices, indices, True)
    #runAlgorithm(logisticRegressionMethod, 'sampledTrain7.csv', 'sampledTest7.csv', 'sampledSubmissionBinary.csv', indices, indices, True)
    #runAlgorithm(randomForestMethod, 'sampledTrain6.csv', 'sampledTest6.csv', 'sampledSubmissionBinary.csv', indices, indices, True)
    #runAlgorithm(linearRegressionMethod, 'sampledTrain6.csv', 'sampledTest6.csv', 'sampledSubmissionBinary.csv', indices, indices, True)
    
################################  running scope  ##############################


printSave('\n###############################################################################\n')
printSave('\nProgram starts...\n')
main()
printSave('\nProgram is terminated successfully.\n')
printSave('\n###############################################################################\n')