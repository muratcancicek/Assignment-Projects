from .MlLibHelper import *


def csvLineToLabeledPoint(line, labelIndex = -1):
    return [np.float64(x) for x in line.split(',')]

def getSparseVectorsAsLabeledPoints(data, labelIndex = -1):
    sv = lambda features: SparseVector(len(features), enumerate(features))
    lbl = lambda l: 1 if l == 1 else -1
    getLabeledPoint = lambda vector: LabeledPoint(lbl(vector[labelIndex]), sv(vector[:labelIndex] + vector[labelIndex+1:]))
    return data.map(getLabeledPoint)

def readCSVDataAsSparseVectors(sc, fileName):
    fileName = joinPath(sparkFolder, fileName)
    data = sc.textFile(fileName).map(csvLineToLabeledPoint)
    data = getSparseVectorsAsLabeledPoints(data)
    return data

def getFloatListsAsLabeledPoints(data, labelIndex = -1):
    getLabeledPoint = lambda vector: LabeledPoint(vector[labelIndex], vector[:labelIndex] + vector[labelIndex+1:])
    return data.map(getLabeledPoint)

def readCSVDataAsLabeledPoints(sc, fileName):
    fileName = joinPath(sparkFolder, fileName)
    data = sc.textFile(fileName).map(csvLineToLabeledPoint)
    data = getFloatListsAsLabeledPoints(data)
    return data

def runLogisticRegressionWithSpark(sc = None):
    if sc == None: sc = SparkContext()
    trainData = readCSVDataAsLabeledPoints(sc, trainUSPSFileName)
    testData = readCSVDataAsLabeledPoints(sc, testUSPSFileName)

    modelFileName = 'pythonLogisticRegressionWithLBFGSModel'
    sameModel = loadLogisticRegressionSparkModel(sc, modelFileName)
    
    print_(sameModel.weights)
    
    evaluateModelOnData(sameModel, testData)