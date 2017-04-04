from Sparker.MLlibTests.MlLibHelper import DenseVector, LabeledPoint
from .ProductPreferrer import *
from .FakeProductGenerator import *
from .Trainer import *

def readTestingTrainData(keyword = 'iphone 6', inputName = 'train'):
    keyword = keyword.replace(' ', '_')
    trainDataFile = inputName + '_' + keyword + '_TrainData'
    trainData = readTrainDataFromHDFS(joinPath(Day1_iPhone_6_DataFolder, trainDataFile))
    #print_(type(trainData.first()), trainData.first())
    trainData = scaleTrainData(trainData)
    #print_(type(trainData.first()), trainData.first())
    return trainData

def mergeLabeledPairs(trainDataPrefix, testDataPrefix, outputFolder = Day1_iPhone_6_DataFolder):
    trainLabeledPairsFile = joinPath(outputFolder, trainDataPrefix + '_labeledPairs')
    trainLabeledPairs = readLabeledPairsFromHDFS(trainLabeledPairsFile)
    print_(trainLabeledPairs.count(), 'LabeledPairs have been found in the original train data by', nowStr())
    testLabeledPairsFile = joinPath(outputFolder, testDataPrefix + '_labeledPairs')
    testLabeledPairs = readLabeledPairsFromHDFS(testLabeledPairsFile)
    print_(testLabeledPairs.count(), 'LabeledPairs have been found in the original test data by', nowStr())
    labeledPairs = trainLabeledPairs.union(testLabeledPairs).distinct()
    labeledPairsFile = joinPath(outputFolder, 'all_labeledPairs')
    labeledPairs.saveAsTextFile(labeledPairsFile)
    print_(labeledPairs.count(), 'distinct labeled pairs have been merged by', nowStr())
    print_(labeledPairsFile, 'have been saved successfully by', nowStr())
    return labeledPairs

def mergeJourneyProducts(trainDataPrefix, testDataPrefix, outputFolder = Day1_iPhone_6_DataFolder):
    trainProductsFile = joinPath(outputFolder, trainDataPrefix +  '_journey_products')
    trainProducts = readProductsFromHDFS(trainProductsFile)
    print_(trainProducts.count(), 'products have been found in the original train data by', nowStr())
    testProductsFile = joinPath(outputFolder, testDataPrefix +  '_journey_products')
    testProducts = readProductsFromHDFS(testProductsFile)
    print_(testProducts.count(), 'products have been found in the original test data by', nowStr())
    products = trainProducts.union(testProducts).distinct()
    print_(products.count(), 'distinct products have  been merged by', nowStr())
    productsFile = joinPath(outputFolder, 'all_journey_products')
    saveRDDToHDFS(products, productsFile)
    return products

def generateAllTrainData(outputFolder = Day1_iPhone_6_DataFolder):
    labeledPairsFile = joinPath(outputFolder, 'all_labeledPairs')
    labeledPairs = readLabeledPairsFromHDFS(labeledPairsFile)
    productsFile = joinPath(outputFolder, 'all_journey_products')
    products = readProductsFromHDFS(productsFile)
    data = generateTrainData(labeledPairs, products)
    dataFile = joinPath(outputFolder, 'all_TrainData')
    saveRDDToHDFS(data, dataFile)
    return data

def splitDataScientifically(data, outputFolder = Day1_iPhone_6_DataFolder, weights = [0.70, 0.30]):
    print_(data.count(), 'instances have been found in the original data by', nowStr())
    data = data.map(lambda p: (p.features, p)).distinct().map(lambda p: p[1])
    #data = data.distinct()
    print_(data.count(), 'distinct instances have been found in the original data by', nowStr())
    trainData, testData = data.randomSplit(weights)
    print_(trainData.count(), 'distinct instances have been selected to be trained', nowStr())
    print_(testData.count(), 'distinct instances have been selected to be tested', nowStr())
    return trainData, testData

def generateExperimentData(data = None, outputFolder = Day1_iPhone_6_DataFolder, weights = [0.70, 0.30]): 
    if data == None:
        dataFile = joinPath(outputFolder, 'all_day_TrainData')
        data = readTrainDataFromHDFS(dataFile)
    trainData, testData = splitDataScientifically(data, outputFolder, weights)
    trainDataFile = joinPath(outputFolder, 'all_day_train_70_TrainData')
    saveRDDToHDFS(trainData, trainDataFile)
    testDataFile = joinPath(outputFolder, 'all_day_test_30_TrainData')
    saveRDDToHDFS(testData, testDataFile)
    return trainData, testData

def extractJourneyLogsFromDayPart(part):
    keyword = 'iphone 6'
    logsFile = joinPath(entireDayRawLogsfolder1, 'part-r-0000' + str(part) + '.gz')
    outputFolder = Day1_iPhone_6_DataFolder
    journeyFile = joinPath(outputFolder, 'iphone_6_part' + str(part) + '_journey')
    extractJourneyLogsFromDay(keyword, logsFile, journeyFile)

def mergeJourneys(outputFolder = Day1_iPhone_6_DataFolder):
    mergedJourney = sc_().emptyRDD()
    for part in range(5):
        journeyFile = joinPath(outputFolder, joinPath('journey_parts', 'iphone_6_part' + str(part) + '_journey'))
        journey = readJourneyFromHDFS(journeyFile)
        print_('%i logs have been parsed by %s' % (journey.count(), nowStr()))
        mergedJourney = mergedJourney.union(journey)
    fileName = 'all_day_journey'
    mergedJourneyFile = joinPath(outputFolder, fileName)
    mergedJourney.saveAsTextFile(mergedJourneyFile)
    print_('%i logs have been merged and saved into %s by %s' % (mergedJourney.count(), fileName, nowStr()))