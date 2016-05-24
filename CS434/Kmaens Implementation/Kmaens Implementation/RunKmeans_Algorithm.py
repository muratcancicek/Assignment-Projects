from CommonTools import *
from Kmeans_Algorithm import *
#    execfile('Main.py') 

################################  main  #######################################

def main():
    data = readDataset('cluster-data-for-k-means.csv')
    #plotSSEvsKValues(data, 'SSE_vs_KValues', maximumK = 10, repetitionNumber = 10) 
    #plotSSEvsIterationNumber(data, 'SSE_vs_IterationNumber', maximumIterationNumber = 20) 
    plotClusters(data, '4_Clusters', k = 4, fixedIterationNumber = 20) 

################################  running scoce  ##############################

main()
print '\nProgram is terminated successfully.\n' 