from CommonTools import *
import matplotlib.pyplot as plt
from random import randint

################################  Index of the closest Center  ################

def getIndexOfClosestCenter(x, centers):
    closestCenterIndex = float('inf')
    minD = float('inf')
    for j in range(len(centers)):
        d = euclideanDistance(x, centers[j])
        if minD > d:
            minD, closestCenterIndex = d, j
    return closestCenterIndex

################################  Index of the closest Center  ################

def getUpdatedCenter(center, points):
    if points == []: return center 
    sums = [0]*len(center)
    for point in points:
        for i in range(len(sums)):
            sums[i] += point[i]
    return [float(sum)/len(points) for sum in sums]

################################  Standart K Mean Algorithm  ##################

def kMaensAlgorithm(data, k, fixedIterationNumber):
    centers = []
    for i in range(k):
        centers.append(data[randint(0, len(data)-1)])
    for iteration in range(fixedIterationNumber):
        clusters = [[] for i in range(k)]
        for x in data:
            clusters[getIndexOfClosestCenter(x, centers)].append(x)
        for j in range(len(centers)):
            centers[j] = getUpdatedCenter(centers[j], clusters[j])
    return clusters, centers

################################  Plot Clusters  ##############################

def plotClusters(data, title = '', k = 3, fixedIterationNumber = 10):
    clusters, centers = kMaensAlgorithm(data, k, fixedIterationNumber)
    colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']
    for i in range(len(clusters)):
        unzippedCluster = zip(*clusters[i])
        plot = plt.scatter(unzippedCluster[0], unzippedCluster[1], marker = 'o', s = 5, color = colors[i]) 
    for i in range(len(centers)):
        plot = plt.scatter(centers[i][0], centers[i][1], marker = 'o', s = 70, color = colors[i], edgecolor='black', linewidth='3') 
    plt.savefig(title, bbox_inches='tight')
    plt.close()

######  objective of the  algorithm as a function of the iterations  ##########

def calculateSSEOfKMaensAlgorithm(data, k = 3, iterationNumber = 10):
    clusters, centers = kMaensAlgorithm(data, k, iterationNumber)
    sse = 0
    for i in range(len(centers)):
        sse += calculateSSE(clusters[i], centers[i], isYFixed = True)
    return sse 

######  objective of the  algorithm as a function of the iterations  ##########

def getSSEbyIterationNumber(data, k = 3, maximumIterationNumber = 10):
    iterationNumbers, sseList = [], []
    for iterationNumber in range(1, maximumIterationNumber+1):
        iterationNumbers.append(iterationNumber)
        sseList.append(calculateSSEOfKMaensAlgorithm(data, k, iterationNumber))
    return iterationNumbers, sseList

################################  Plot SSE vs IterationNumber  ################

def plotSSEvsIterationNumber(data, title = '', k = 3, maximumIterationNumber = 10):
    iterationNumbers, sseList = getSSEbyIterationNumber(data, k, maximumIterationNumber)
    plot = plt.plot(iterationNumbers, sseList, marker = 'D', linestyle = '-') 
    formatPlot(iterationNumbers, sseList, title)
    plt.savefig(title, bbox_inches='tight')
    plt.close()
    
################################  Getting lowest SSE of K value  ##############

def getLowestSSEfromRepetitions(data, k, repetitionNumber = 10):
    minSSE = float('inf') 
    for repetition in range(repetitionNumber):
        sse = calculateSSEOfKMaensAlgorithm(data, k) 
        if sse < minSSE:
            minSSE = sse
    print 'minSSE =', minSSE, 'for K:', k, '\n' 
    return minSSE

################################  Calculating SSE of K values  ################

def calculateSSEofKValues(data, maximumK = 10, repetitionNumber = 10):
    if maximumK < 2: maximumK = 2
    kList, sseList = [], []
    for k in range(2, maximumK+1):
        kList.append(k)
        sseList.append(getLowestSSEfromRepetitions(data, k, repetitionNumber))
    return kList, sseList

################################  Plot SSE vs K values  #######################

def plotSSEvsKValues(data, title = '', maximumK = 10, repetitionNumber = 10):
    kList, sseList = calculateSSEofKValues(data, maximumK, repetitionNumber)
    plot = plt.plot(kList, sseList, marker = 'D', linestyle = '-') 
    formatPlot(kList, sseList, title)
    #plt.tick_params(axis='y', which='minor', labelsize=5)
    plt.savefig(title, bbox_inches='tight')
    plt.close()