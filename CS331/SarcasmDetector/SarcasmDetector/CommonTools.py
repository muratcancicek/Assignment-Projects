import math

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