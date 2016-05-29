from MDP_Planning_Algorithm import *
from InputReaderForMDP import *

################################  main  #######################################

def main():
    data = readTestData('test-data-for-MDP.txt')
    betaValues = [0.1, 0.9]
    for b in betaValues:
        algorithm = MDP_Planning_Algorithm(data, b)
        optimalUtilityVector = algorithm.valueIterationAlgorithm()
        policyVector = algorithm.getPolicyVector()
        print '\n', optimalUtilityVector,  '\n', policyVector, '\n', '\n'

################################  running scoce  ##############################

main()
print '\nProgram is terminated successfully.\n'