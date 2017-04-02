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

def trainIPhone6DataTest():  
    keyword = 'iphone 6'
    inputName = 'Day1_Part0'
    outputFolder = Day1_iPhone_6_DataFolder
    journeyFile = joinPath(outputFolder, 'iphone_6_part0_journey')
    #productsFile = joinPath(sparkFolder, 'sampleProducts')\\part-00045
    #productsFile = None
    #journey = readJourneyFromHDFS(journeyFile)
    #modulizedIds = getLabeledPairsWithModulizedIds(journey)
    #print_( modulizedIds['labeledPairs'].take(40))
    #extractLabeledPairsFromJourney(keyword, inputName, journeyFile, productsFile, outputFolder)
    
    keyword = keyword.replace(' ', '_')
    labeledPairsFile = inputName + '_' + keyword + '_' + 'labeledPairs'
    modulizedIds = {'labeledPairs': sc_().textFile(joinPath(outputFolder, labeledPairsFile))}
    print_(modulizedIds['labeledPairs'].count(), 'labeledPairs have been read successfully by', nowStr())
    #products.saveAsTextFile(joinPath(outputFolder, journeyProductsFile))
    #products = getProducts(modulizedIds['listed'], productsFile)
    journeyProductsFile = inputName + '_' + keyword + '_' + 'journey_products'
    products = readProductsFromHDFS(joinPath(outputFolder, journeyProductsFile))
    print_(type(products.first()), products.first())
    print_(products.count(), 'products have been read successfully by', nowStr())
    trainData = generateTrainData(modulizedIds['labeledPairs'], products)
    trainDataFile = inputName + '_' + keyword + '_' + '_TrainData'
    trainData.saveAsTextFile(joinPath(outputFolder, trainDataFile))
    print_(trainDataFile, 'has been saved successfully by', nowStr())
    return trainData

def trainLocalLG_G4DataTest(): 
    keyword = 'lg g4'
    inputName = 'fake'
    outputFolder = Day1_lg_g4_DataFolder
    journeyFile = joinPath(outputFolder, 'lg_g4_journey')
    productsFile = joinPath(sparkFolder, 'sampleProducts')
    extractLabeledPairsFromJourney(keyword, inputName, journeyFile, productsFile, outputFolder)
    
def trainLocalDataTest():
    trainIPhone6DataTest()