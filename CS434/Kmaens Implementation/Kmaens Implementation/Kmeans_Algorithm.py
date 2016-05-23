from CommonTools import *
import matplotlib.pyplot as plt
from random import randint

################################  Index of the closest Center  ################

def getIndexOfClosestCenter(x, centers):
    closestCenterIndex = float('inf')
    for j in range(len(centers)):
        minD = float('inf')
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
    clusters = [[] for i in range(k)]
    for iteration in range(fixedIterationNumber):
        for x in data:
            clusters[getIndexOfClosestCenter(x, centers)].append(x)
        for j in range(len(centers)):
            centers[j] = getUpdatedCenter(centers[j], clusters[j])
    return clusters, centers

######  objective of the  algorithm as a function of the iterations  ##########

def calculateSSEOfAlgorithm(data, k = 3, iterationNumber = 10):
    clusters, centers = kMaensAlgorithm(data, k, iterationNumber)
    sse = 0
    for i in range(len(centers)):
        sse += calculateSSE(clusters[i], centers[i], isYFixed = True)
    return sse 

######  objective of the  algorithm as a function of the iterations  ##########

def getObjectivesOfAlgorithm(data, k = 3, maximumIterationNumber = 10):
    sseList = []
    for iterationNumber in range(1, maximumIterationNumber+1):
        sseList.append(calculateSSEOfAlgorithm(data, k, iterationNumber))
    return sseList

################################  Standart K Mean Algorithm  ##################

def plotObjectiveOfAlgorithm(data, title = '', k = 3, maximumIterationNumber = 10):
    sseList = getObjectivesOfAlgorithm(data, k, maximumIterationNumber)
    plot = plt.plot(sseList) 
    formatPlot(sseList, [], title)
    plt.savefig(title, bbox_inches='tight')
    plt.close()