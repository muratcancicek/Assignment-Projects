from CommonTools import *
from Kmeans_Algorithm import *
#    execfile('Main.py') 

################################  main  #######################################

def main():
    data = readDataset('sampledTrian.csv')
    kMaensAlgorithm(data, 100, 10)

################################  running scoce  ##############################

main()
print '\nProgram is terminated successfully.\n' 