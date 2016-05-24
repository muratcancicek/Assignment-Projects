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

def readDataset(fileName, splitChar = ','):  
    file = open(fileName, 'rb') 
    dataset = []
    for rawLine in file: 
        row = str.split(rawLine, splitChar) 
        featuresAndLebel = []
        for i in range(len(row)):
           featuresAndLebel.append(float(row[i]))
        dataset.append(featuresAndLebel)
    return dataset


###############################  ACCURACY  ####################################

def getAccuracyCount(testSet, predictions, labelIndex = DEFAULT_LABEL_INDEX):
	accuracyCount = 0
	for x in range(len(testSet)):
		if isinstance(testSet[x], list):
		    if testSet[x][labelIndex] == predictions[x]:
		        accuracyCount += 1
		else:
		    if testSet[x] == predictions[x]:
		        accuracyCount += 1
	return accuracyCount
	
#################################  ERROR  #####################################

def getErrorCount(testSet, predictions, labelIndex = DEFAULT_LABEL_INDEX):
	errorCount = 0
	for x in range(len(testSet)):
		if isinstance(testSet[x], list):
		    if testSet[x][labelIndex] != predictions[x]:
		        errorCount += 1
		else:
		    if testSet[x] != predictions[x]:
		        errorCount += 1
	return errorCount

###############################  ACCURACY  ####################################

def getAccuracy(testSet, predictions, labelIndex = DEFAULT_LABEL_INDEX):
	accuracyCount = getAccuracyCount(testSet, predictions, labelIndex)
	return percentage(testSet, accuracyCount)

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

############################  LIST TRANSPOSE  #################################

def transposeList(l):
    return map(list, zip(*l))

###########################  EUCLIDEAN DISTANCE  ##############################

def euclideanDistance(example1, example2):
	return math.sqrt(calculateSSE(example1, example2))

###########################  EUCLIDEAN DISTANCE  ##############################

def calculateSSE(xLlist, yList, isYFixed = False): 
    sum = 0
    if isinstance(yList, list):
        if isYFixed:
            for i in range(len(xLlist)): 
                for j in range(len(xLlist[i])): 
                    sum += (yList[j] - xLlist[i][j]) ** 2
        else:
            for i in range(len(xLlist)): 
                sum += (yList[i] - xLlist[i]) ** 2
    else:
        y = yList
        for i in range(len(xLlist)): 
            sum += (y - xLlist[i]) ** 2
    return sum

############################# FORMATTING PLOTTING  ############################

plotCount = 1
def formatPlot(x, y, title = '', xLabel = '', yLabel = '', legendList = [], xBorder = 0, yBorder = 0): 
    if xBorder != 0:
        xmin, xmax = plt.xlim()
        plt.xlim(xmin, xmax+xBorder) 
    if yBorder != 0: 
        ymin, ymax = plt.ylim()
        plt.ylim(ymin, ymax+yBorder)  
    if title != '':
        plt.title(title)
    if xLabel != '':
        plt.xlabel(xLabel)
    if yLabel != '':
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
    plt.yticks(y,  fontsize = 8) 

############################  PLOTTING SINGLE LINE  ###########################

def plotSingleLine(x, y, title = '', xLabel = '', yLabel = '', legendList = [], xBorder = 0, yBorder = 0, marker='.', linestyle='-'):  
    plot = plt.plot(x, y, marker = marker, linestyle = linestyle) 
    formatPlot(x, y, title, xLabel, yLabel, legendList, xBorder, yBorder)
    plt.savefig(title, bbox_inches='tight')
    plt.close()
    return plot
