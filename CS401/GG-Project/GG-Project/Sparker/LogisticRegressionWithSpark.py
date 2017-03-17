from MainSrc.PythonVersionHandler import *
from .PySparkImports import *
from paths import *

def readUSPSData(sc, trainFileName = 'usps-4-9-train.csv', testFileName = 'usps-4-9-test.csv'):
    trainFileName = joinPath(sparkFolder, trainFileName)
    testFileName = joinPath(sparkFolder, testFileName)
    trainData = sc.textFile(trainFileName)
    testData = sc.textFile(testFileName)
    return trainData, testData

def runLogisticRegressionWithSpark():
    sc = SparkContext() 
    trainData, testData = readUSPSData(sc)
    trainData.foreach(print_)