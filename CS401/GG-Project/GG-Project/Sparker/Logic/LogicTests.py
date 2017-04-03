from .ProductPreferrer import *
from .FakeProductGenerator import *
from .Trainer import *

def trainTest(logs):
    #labeledPairs, ids = getLabeledIds()
    #products = getProducts(ids)
    #print(products.first())
    trainData = getTrainData()#generateTrainData(labeledPairs, products)
    #print(trainData.first())
    trainPairWiseData(trainData)

def testAlgorithm():
    if logs == None:
        #journey = getSampleJourney(logs)
        #journey.saveAsTextFile(joinPath(sparkFolder, 'lg_g4_journey'))
        #logs = sc_().textFile(joinPath(sparkFolder, 'lg_g4_journey')).map(lambda l: eval(l)) 
        #logs = getLogs()
        #logs = load2016_09_27_iphone_6()
        logs = readParsedLogs(joinPath(sparkFolder, 'part-r-00000_keyword00000.json'))
    ##printActions(journey)
    #labeledPairs = getInterestingIds(logs)
    #sc_().parallelize(labeledPairs.items()).saveAsTextFile(joinPath(sparkFolder, 'labels'))

    ## sc_().textFile(joinPath(sparkFolder, 'sampleProducts'))
    print_(logs.count(), 'Logs have been read and parsed on', nowStr())

def trainIPhone6DataGenerationTest(): 
    keyword = 'iphone 6'
    keyword = keyword.replace(' ', '_')
    inputName = 'train'
    outputFolder = Day1_iPhone_6_DataFolder
    journeyFile = joinPath(outputFolder, 'iphone_6_train_journey')
    productsFile = None
    #productsFile = joinPath(sparkFolder, 'sampleProducts')\\part-00045

    #journey = readJourneyFromHDFS(journeyFile)
    #modulizedIds = getLabeledPairsWithModulizedIds(journey)
    #labeledPairsFile = inputName + '_' + keyword + '_' + 'labeledPairs'
    #modulizedIds['labeledPairs'].saveAsTextFile(joinPath(outputFolder, labeledPairsFile))

    #print_( modulizedIds['labeledPairs'].take(40))
    extractLabeledPairsFromJourney(keyword, inputName, journeyFile, productsFile, outputFolder)
    
    #labeledPairsFile = inputName + '_' + keyword + '_' + 'labeledPairs'
    #modulizedIds = {}
    #modulizedIds['labeledPairs'] = readLabeledIdsFromHDFS(joinPath(outputFolder, labeledPairsFile))
    #print_(modulizedIds['labeledPairs'].count(), 'labeledPairs have been read successfully by', nowStr())
    ###products.saveAsTextFile(joinPath(outputFolder, journeyProductsFile)), modulizedIds['listed'] 
    ###products = getProducts(modulizedIds['listed'], productsFile)
    #journeyProductsFile = inputName + '_' + keyword + '_' + 'journey_products'
    #products = readProductsFromHDFS(joinPath(outputFolder, journeyProductsFile))
    ##print_(type(products.first()), products.first())
    #print_(products.count(), 'products have been read successfully by', nowStr())
    #trainData = generateTrainData(modulizedIds['labeledPairs'], products)
    #trainDataFile = inputName + '_' + keyword + '_' + '_TrainData'
    #trainData.saveAsTextFile(joinPath(outputFolder, trainDataFile))
    #print_(trainDataFile, 'has been saved successfully by', nowStr())
    #return trainData

def trainLocalLG_G4DataTest(): 
    keyword = 'lg g4'
    inputName = 'fake'
    outputFolder = Day1_lg_g4_DataFolder
    journeyFile = joinPath(outputFolder, 'lg_g4_journey')
    productsFile = joinPath(sparkFolder, 'sampleProducts')
    extractLabeledPairsFromJourney(keyword, inputName, journeyFile, productsFile, outputFolder)

def trainTestOnIPhone6Data():  
    keyword = 'iphone 6'
    inputName = 'train'
    keyword = keyword.replace(' ', '_')
    trainDataFile = inputName + '_' + keyword + '_' + '_TrainData'
    trainData = readTrainDataFromHDFS(joinPath(Day1_iPhone_6_DataFolder, trainDataFile))
    print_(type(trainData.first()), trainData.first())
    trainData = scaleTrainData(trainData)
    print_(type(trainData.first()), trainData.first())
    trainPairWiseData(trainData)
    
def extractJourneyLogsFromDay0(part):
    keyword = 'iphone 6'
    logsFile = joinPath(entireDayRawLogsfolder1, 'part-r-0000' + str(part) + '.gz')
    outputFolder = Day1_iPhone_6_DataFolder
    journeyFile = joinPath(outputFolder, 'iphone_6_part' + str(part) + '_journey')
    extractJourneyLogsFromDay(keyword, logsFile, journeyFile)

def mergeJourneys(outputFolder = Day1_iPhone_6_DataFolder):
    mergedJourney = sc_().emptyRDD()
    for part in range(4):
        journeyFile = joinPath(outputFolder, 'iphone_6_part' + str(part) + '_journey')
        journey = readJourneyFromHDFS(journeyFile)
        print_('%i logs have been parsed by %s' % (journey.count(), nowStr()))
        mergedJourney = mergedJourney.union(journey)
    fileName = 'iphone_6_train_journey'
    print_('%i logs have been merged and saved into %s by %s' % (mergedJourney.count(), fileName, nowStr()))
    mergedJourneyFile = joinPath(outputFolder, fileName)
    mergedJourney.saveAsTextFile(mergedJourneyFile)

def trainLocalDataTest():
    trainIPhone6DataGenerationTest()
    #trainTestOnIPhone6Data()
    #extractJourneyLogsFromDay0(4)
    #mergeJourneys()