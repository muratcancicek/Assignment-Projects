import matplotlib.pyplot as plt
import average_precision as ap
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier 
from CommonTools import *
import numpy as np

def readXYFromFile(fileName, indices = [], labelIndex = 9, dateIndex = 0):  
    featuresMatrix, labels = [], [] 
    def readRow(row):
        features = []
        for i in range(len(row)):
            if i == labelIndex:
                labels.append(float(row[-1])) 
            else:#if not i == 3:
                features.append(float(row[i]))
        featuresMatrix.append(features)
    def readOriginalRow(row):
        features = []
        for i in indices: 
            if i == labelIndex and labelIndex != -1:
                labels.append(int(row[i])) 
            elif i == dateIndex:
                year, month = row[i][:4], row[i][5:7]
                features.extend([int(year), int(month)])
            else:
                features.append(float(row[i]))
        featuresMatrix.append(features)
    if indices == []:
        iterateRows(readRow, fileName)
    else:
        iterateRows(readOriginalRow, fileName)
    return np.array(featuresMatrix), np.array(labels)

def roundToInt(a):
    for i, v in enumerate(a):
        a[i] = int(round(v))
    return a

def getPredictedRankings(predictions):
    predictedRankings = []
    for v in predictions:
        v, oV, rankings = int(round(v)), v, []
        if v > oV:
            rankings = [v, v+1, v-1, v+2, v-2]
        else:
            rankings = [v, v-1, v+1, v-2, v+2]
        if v < 2:
            d = 2-v
            rankings = [v+d, v+d-1, v+d+1, v+d-2, v+d+2]
        if v > 97:
            d = 97-v
            rankings = [v+d, v+d-1, v+d+1, v+d-2, v+d+2]
        predictedRankings.append(rankings)
    return predictedRankings

def linearRegressionMethod(trainFeatures, trainLabels, testFeatures, testLabels): 
    regr = linear_model.LinearRegression()
    regr.fit(trainFeatures, trainLabels)
    predictions = regr.predict(testFeatures)
    printSave('Coefficients: \n', regr.coef_)
    #predictions = np.dot(testFeatures, coefficients)
    #printSave('Linear Regression score: ' + str(regr.score(predictions, testLabels)))  
    return roundToInt(predictions)

def randomForestMethod(trainFeatures, trainLabels, testFeatures, testLabels): 
    forest = RandomForestClassifier(n_estimators = 100)
    forest = forest.fit(trainFeatures, trainLabels)
    predictions = forest.predict(testLabels)
    return roundToInt(predictions)

def getData(trainName, testName, submissionFilename, trainIndices, testIndices): 
    #coefficients = [0, 0.00102729,  0.00014835,  0.11000585, -0.00712165, 0, 0, 0.12590906]
    trainFeatures, trainLabels = [], []
    if trainIndices != []:
        trainFeatures, trainLabels = readXYFromFile(trainName, trainIndices, trainIndices[-1])
    else:
        trainFeatures, trainLabels = readXYFromFile(trainName)
    testFeatures, testLabels = [], []
    if trainIndices != []:
        testFeatures, testLabels = readXYFromFile(testName, testIndices)#, -1, 1 
    else:
        testFeatures, testLabels = readXYFromFile(testName)#, 1 
    return trainFeatures, trainLabels, testFeatures, testLabels

def runAlgorithm(algorithm, trainName, testName, submissionFilename = '', trainIndices = [], testIndices = []):
    trainFeatures, trainLabels, testFeatures, testLabels = getData(trainName, testName, submissionFilename, trainIndices, testIndices)
    
    predictions = algorithm(trainFeatures, trainLabels, testFeatures, testLabels)
    
    return generateOutput(testLabels, predictions, True, submissionFilename)

def generateOutput(testLabels, predictions, singlePrediction, submissionFileName = ''):
    if singlePrediction:
        predictions = roundToInt(predictions)
        printSave('1-1 Accuracy: ' + str(getAccuracy(testLabels, predictions)/100))
    else:
        predictedRankings = getPredictedRankings(predictions)
        listedTestLabels = [[c] for c in testLabels]
        printSave('mapk Accuracy: ' + str(ap.mapk(listedTestLabels, predictedRankings, k = 5)))
        predictions = predictedRankings
    makeSubmission(submissionFileName, predictions)  
    return predictions 

def makeSubmission(submissionFileName, predictions):
    if submissionFileName != '':
        predictedRankings = getPredictedRankings(predictions)
        saveSubmission(submissionFileName, predictedRankings)

def saveSubmission(fileName, predictions):
    write_p = [" ".join([str(l) for l in p]) for p in predictions]
    write_frame = ["{0},{1}".format(i, write_p[i]) for i in range(len(predictions))]
    write_frame = ["id,hotel_cluster"] + write_frame
    with open(fileName, "w+") as f:
        f.write("\n".join(write_frame))
    print 'Predictions are saved' 