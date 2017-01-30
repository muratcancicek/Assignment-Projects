from CommonTools import *
import operator
  
##############################  GETTING NEIGHBORS  ############################

def getNeighbors(trainingExamples, newExample, k, lebelIndex = DEFAULT_LABEL_INDEX):
	distances = []
	for i in range(len(trainingExamples)):
		featuresOfNewExample = newExample[lebelIndex+1:]
		featuresOfTrainingExample = trainingExamples[i][lebelIndex+1:] 
		singleDistance = euclideanDistance(featuresOfNewExample, featuresOfTrainingExample)
		distances.append((trainingExamples[i], singleDistance))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for i in range(k):
		neighbors.append(distances[i][0])
	return neighbors 

################################  PREDICTION  #################################

def predict(neighbors, lebelIndex = DEFAULT_LABEL_INDEX):
	lebels = {}
	for i in range(len(neighbors)):
		prediction = neighbors[i][lebelIndex]
		if prediction in lebels:
			lebels[prediction] += 1
		else:
			lebels[prediction] = 1
	sortedVotes = sorted(lebels.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

#############################  KNN ALGORITHM  #################################
def getPredictionsBy_KNN_Algorithm(trainingData, testData, k):
	predictions = []
	for i in range(len(testData)):
		neighbors = getNeighbors(trainingData, testData[i], k)
		prediction = predict(neighbors)
		predictions.append(prediction)
	return predictions

###########################  TESTING KNNN ALGORITHM  ##########################

def testKNN_Algorithm(trainingData, testData, startingK, endingK = -1, step = 2, printing = True):
    if endingK == -1:
        endingK = startingK
    k = startingK
    results = []
    if printing: 
        print 'In', len(testData), 'examples:' 
    while k <= endingK:
        if k%2 == 0: k += 1 # Avoiding ties 
        predictions = getPredictionsBy_KNN_Algorithm(trainingData, testData, k)
        errorCount = getErrorCount(testData, predictions)
        accuracy = (100-percentage(testData, errorCount))
        if printing: 
            print '\tFor k =', str(k)+':', '# of mistakes =', errorCount, '| Accuracy =', accuracy
        results.append([k, errorCount, accuracy])
        k += step
    return transposeList(results) 
    
#######################  Leave-one-out Cross Validation  ######################

def Cross_Validation(trainingData, startingK, endingK = -1, step = 2, printing = False):
    errors = []
    kValues = []
    for outIndex in range(len(trainingData)):
        remainingData = trainingData[:outIndex] + trainingData[(outIndex+1):]
        testingExample = [trainingData[outIndex]]
        results = testKNN_Algorithm(remainingData, testingExample, startingK, endingK, step, printing)
        kValues = results[0]
        errors.append(results[1])
    errors = transposeList(errors)
    sums = []
    for errorsForK in errors:
        sum = 0
        for error in errorsForK:
            sum += error
        sums.append(sum)
    return [kValues, sums]
    
############################  PLOTTING KNN RESULTS  ###########################/len(errorsForK)

def plotAndSaveResultsOf_KNN_Algorithm(results, fileName = ''):
    plotSingleLine(results[0], results[1], title = fileName, xLabel = ' k values',
                   yLabel = '# of mistakes', xBorder = 1, yBorder = 1)

#############################  PLOTTING KNN ALL ERRORS  #######################

def plotAndSaveResultsOfAllErrors_KNN_Algorithm(xyList, fileName = '', legendList = []):
    plotMultiLine(xyList, title = fileName, xLabel = ' k values',
                   yLabel = '# of mistakes', xBorder = 1, yBorder = 2, legendList = legendList)
    
##############################  MAIN FUNCTIONALITIES  #########################

def readKNNDataForHW3():
    trainingData = readDataset('knn_train.csv')
    testData = readDataset('knn_test.csv')
    return trainingData, testData

def getKNNResultsOnTrainingData(startingK, endingK = -1, trainingData = ['knn_train.csv'], plotting = False):
    if trainingData == ['knn_train.csv']:
        trainingData = readDataset('knn_train.csv')
    resultsOnTrainingData = testKNN_Algorithm(trainingData, trainingData, startingK, endingK, printing = plotting)
    if plotting: 
        plotAndSaveResultsOf_KNN_Algorithm(resultsOnTrainingData, 'KNN_Results_on_Training_Data')
    return resultsOnTrainingData

def getKNNResultsOfCrossValidation(startingK, endingK = -1, trainingData = ['knn_train.csv'], plotting = False):
    if trainingData == ['knn_train.csv']:
        trainingData = readDataset('knn_train.csv')
    resultsOfCrossValidation = Cross_Validation(trainingData, startingK, endingK)
    if plotting: 
        plotAndSaveResultsOf_KNN_Algorithm(resultsOfCrossValidation, 'Cross_Validation_Results_on_Training_Data') 
    return resultsOfCrossValidation

def getKNNResultsOnTestData(startingK, endingK = -1, trainingData = ['knn_train.csv'], testData = ['knn_test.csv'], plotting = False):
    if trainingData == ['knn_train.csv']:
        trainingData = readDataset('knn_train.csv')
    if testData == ['knn_test.csv']:
        testData = readDataset('knn_test.csv')
    resultsOnTestData = testKNN_Algorithm(trainingData, testData, startingK, endingK, printing = plotting)
    if plotting: 
        plotAndSaveResultsOf_KNN_Algorithm(resultsOnTestData, 'KNN_Results_on_Test_Data')
    return resultsOnTestData 

def getResultsOfAllErrors_KNN_Algorithm(startingK, endingK = -1, trainingData = ['knn_train.csv'], testData = ['knn_test.csv'], plotting = False):
    trainingData, testData = readKNNDataForHW3()
    resultsOnTrainingData = getKNNResultsOnTrainingData(startingK, endingK, trainingData)
    resultsOfCrossValidation = getKNNResultsOfCrossValidation(startingK, endingK, trainingData)
    resultsOnTestData = getKNNResultsOnTestData(startingK, endingK, trainingData, testData)
    xyList = [resultsOnTrainingData, resultsOfCrossValidation,  resultsOnTestData]
    lengendList = ['ErrorsOnTrainingData', 'resultsOfCrossValidation',  'ErrorsOnTestData']
    if plotting:
        plotAndSaveResultsOfAllErrors_KNN_Algorithm(xyList, 'ResultsOfAllErrors_KNN_Algorithm', lengendList)
    return xyList