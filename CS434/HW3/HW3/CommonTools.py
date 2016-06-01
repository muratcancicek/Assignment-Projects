import math
import matplotlib.pyplot as plt 

DEFAULT_LABEL_INDEX = 0
##########################  READING FILE X AND Y ##############################

def readXYFromFile(fileName, labelIndex = DEFAULT_LABEL_INDEX, splitChar = ','):  
    file = open(fileName, 'rb') 
    featuresMatrix, labels = [], [] 
    for rawLine in file: 
        row = str.split(rawLine, splitChar) 
        features = []
        for i in range(len(row)):
            if i == labelIndex:
                labels.append(float(row[-1])) 
            else:
                features.append(float(row[i]))
        featuresMatrix.append(features)
    return [featuresMatrix, labels] 

##########################  READING FILE AS LINES #############################

def readDataset(fileName, labelIndex = DEFAULT_LABEL_INDEX, splitChar = ','):  
    file = open(fileName, 'rb') 
    dataset = []
    for rawLine in file: 
        row = str.split(rawLine, splitChar) 
        featuresAndLebel = []
        for i in range(len(row)):
           featuresAndLebel.append(float(row[i]))
        dataset.append(featuresAndLebel)
    return dataset

###########################  EUCLIDEAN DISTANCE  ##############################

def euclideanDistance(example1, example2):
	distance = 0
	for i in range(len(example1)):
		distance += (example1[i] - example2[i]) ** 2
	return math.sqrt(distance)

###############################  ACCURACY  ####################################

def getAccuracyCount(testSet, predictions, labelIndex = DEFAULT_LABEL_INDEX):
	accuracyCount = 0
	for x in range(len(testSet)):
		if testSet[x][labelIndex] == predictions[x]:
			accuracyCount += 1
	return accuracyCount
	
#################################  ERROR  #####################################

def getErrorCount(testSet, predictions, labelIndex = DEFAULT_LABEL_INDEX):
	errorCount = 0
	for x in range(len(testSet)):
		if testSet[x][labelIndex] != predictions[x]:
			errorCount += 1
	return errorCount

###############################  PERCENTAGE  ##################################

def percentage(dataset, count):
    return (count/float(len(dataset))) * 100

#############################  FORMATTING FLOATS  #############################

def removezeros(number):
    number = '%.15f' % number
    while len(number):
        if number[::-1][0] == '0':
            number = number[:-1]
        elif number[::-1][0] == '.':
            number = number[:-1]
            break
        else:
            break
    return number

############################# FORMATTING PLOTTING  ############################

plotCount = 1
def formatPlot(x, y, title = '', xLabel = '', yLabel = '', legendList = [], xBorder = 0, yBorder = 0): 
    xmin, xmax = plt.xlim()
    plt.xlim(xmin, xmax+xBorder)  
    ymin, ymax = plt.ylim()
    plt.ylim(ymin, ymax+yBorder)  
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    if legendList != []:
        plt.legend(legendList, loc='best', numpoints=1)
    plt.tight_layout()
    if title == '':
        global plotCount  
        title = 'Plot' + str(plotCount)
        plotCount += 1
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.xticks(x)
    plt.yticks(y) 

############################  PLOTTING SINGLE LINE  ###########################

def plotSingleLine(x, y, title = '', xLabel = '', yLabel = '', legendList = [], xBorder = 0, yBorder = 0):  
    plot = plt.plot(x, y) 
    formatPlot(x, y, title, xLabel, yLabel, legendList, xBorder, yBorder)
    plt.savefig(title, bbox_inches='tight')
    plt.close()
    return plot

############################  PLOTTING MULTI LINE  ############################

def plotMultiLine(xyList, title = '', xLabel = '', yLabel = '', legendList = [], xBorder = 0, yBorder = 0): 
    X, Y = [], []
    for xy in xyList:
        [x, y] = xy[:2]
        X, Y = X+x, Y+y 
        plot = plt.plot(x, y) 
        formatPlot(x, y, title, xLabel, yLabel, legendList, xBorder, yBorder)
    xmin, xmax = plt.xlim()
    plt.xlim(xmin, xmax+xBorder)  
    ymin, ymax = plt.ylim()
    plt.ylim(ymin, ymax+yBorder)  
    plt.xticks(X)
    plt.yticks(Y) 
    plt.savefig(title, bbox_inches='tight')
    plt.close()

############################  LIST TRANSPOSE  #################################

def transposeList(l):
    return map(list, zip(*l))