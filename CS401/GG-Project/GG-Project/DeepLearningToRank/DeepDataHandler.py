from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from Sparker.Logic.TrainDataHandler import *
from MainSrc.PythonVersionHandler import *
from paths import *
import pickle

def loadPickle(fileName):
    file = open(fileName, 'rb')
    return pickle.load(file)


def readTrainDataFromPickle(fileName):
    trainData = loadPickle(fileName)
    trainData = map(lambda x: x.replace('LabeledPoint', ''), trainData)
    trainData = map(eval, trainData)
    trainData = map(lambda x: x[1], trainData)
    trainData = list(map(lambda x: (1.0 if x[0] > 0 else 0.0, x[1]), trainData))
    print_(fileName, 'has been read successfully by', nowStr()) 
    return trainData

def convertHDFStoPickle(keyword):
    dataTypes = ['_TrainData', '_labeledPairs', '_journey_products']
    for typ in dataTypes[1:-1]:
        fileName = 'all_day_' + keyword + typ
        trainDataFile = joinPath(textTrainDataFolder, fileName + '/part-00000')
        trainData = open(trainDataFile, 'r').readlines()
        #trainData = map(lambda x: x.replace('LabeledPoint', ''), trainData)
        #trainData = map(eval, trainData)
        #trainData = map(lambda x: x[1], trainData)
        #trainData = list(map(lambda x: (1.0 if x[0] > 0 else 0.0, x[1]), trainData))

        #trainData = map(evalProduct, trainData)

        trainData = map(eval, trainData)

        print_(fileName, 'has been read successfully by', nowStr()) 
        
        trainDataFile = trainDataFile.replace('/part-00000', '.txt')
        print_(trainDataFile, 'has been saved successfully by', nowStr())
        fp = open(trainDataFile, "wb")   #Pickling
        pickle.dump(trainData, fp)

def convertPickleToHDFS(keyword):
    dataTypes = ['_TrainData', '_labeledPairs', '_journey_products']
    for typ in dataTypes[:1]:
        fileName = 'all_day_' + keyword + typ
        trainDataFile = joinPath(textTrainDataFolder, fileName + '.txt')
        trainData = readTrainDataFromPickle(trainDataFile)
        #trainData = readTrainDataFromHDFS(trainDataFile)
        trainData =  sc_().parallelize(trainData)
        print_(trainDataFile, trainData.count())
        saveRDDToHDFS(trainData, joinPath(joinPath(textTrainDataFolder, 'HDFS'), fileName))