from CommonTools import *
from MDP_Planning_Algorithm import *
from InputReaderForMDP import *
#    execfile('Main.py') 

################################  main  #######################################

def main():
    data = readTestData('test-data-for-MDP.txt')
    betaValues = [0.9, 01]
    for b in betaValues:
        algorithm = MDP_Planning_Algorithm(data, b)
        optimalUtilityVector, policyVector = algorithm.valueIterationAlgorithm()
        print optimalUtilityVector, '\n'
        print policyVector, '\n'
        print '\n'

################################  running scoce  ##############################

main()
print '\nProgram is terminated successfully.\n'