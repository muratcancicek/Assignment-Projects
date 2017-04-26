from Sparker.MLlibTests.MlLibHelper import DenseVector, LabeledPoint
from .ProductPreferrer import *
from .FakeProductGenerator import *
from .TrainDataHandler import *
from .Trainer import *
    
def trainLocalLG_G4DataTest(): 
    keyword = 'lg g4'
    inputName = 'fake'
    outputFolder = Day1_lg_g4_DataFolder
    journeyFile = joinPath(outputFolder, 'lg_g4_journey')
    productsFile = joinPath(sparkFolder, 'sampleProducts')
    extractLabeledPairsFromJourney(keyword, inputName, journeyFile, productsFile, outputFolder)

def trainIPhone6DataGenerationTest(): 
    keyword = 'iphone 6'
    keyword = keyword.replace(' ', '_')
    inputName = 'all_day'
    outputFolder = Day1_iPhone_6_DataFolder
    journeyFile = joinPath(outputFolder, inputName + '_journey')
    productsFile = None
    return extractLabeledPairsFromJourney(keyword, inputName, journeyFile, productsFile, outputFolder)

def trainTestOnIPhone6Data():  
    outputFolder = Day1_iPhone_6_DataFolder
    trainDataFile = joinPath(outputFolder, 'all_day_train_70_TrainData')
    trainData = readTrainDataFromHDFS(trainDataFile)
    testDataFile = joinPath(outputFolder, 'all_day_test_30_TrainData')
    testData = readTrainDataFromHDFS(testDataFile)
    #trainData, testData = generateExperimentData()
    modelName = 'Model_v04_4'
    labelsAndPreds = runTrainingExperiment(trainData, testData, modelName, False)
    labelsAndPreds = labelsAndPreds.take(50)
    print_(labelsAndPreds)
    
def rankingTestOnIPhone6Data():  
    outputFolder = Day1_iPhone_6_DataFolder
    productsFile = joinPath(outputFolder, 'all_day_iphone_6_journey_products')
    products = readProductsFromHDFS(productsFile)
    rankProducts(products, outputFolder, model = None, modelName = 'Model_v04_4')
    
def userBehaviorTestOnIPhone6Data():  
    journey = readJourneyFromHDFS(joinPath(Day1_iPhone_6_DataFolder, 'all_day_journey'))
    printJourney(journey)

def parseAllDayTest():
   allDayPath, outputPath = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/session/2016-12-25', joinPath('/user/root/Parsed', entireDay1 + '_parsed')
   print_('Output Folder:', outputPath)
   parseAllDay(allDayPath, outputPath)
   
def trainDataGenerationTest():
    logs = None #readParsedLogsFromHDFS(entireDayParsedLogsFolder1)
    keyword = 'jant'
    outputFolder = joinPath(HDFSDataFolder, 'Day1_jant_Data')
    generateTrainData(logs, keyword, outputFolder)

def generateJourney(logs, keyword): 
    rawKeyword = keyword
    keyword = keyword.replace(' ', '_')
    outputFolder = joinPath(HDFSDataFolder, 'Day1_' + keyword + '_Data')
    #if not os.path.exists(outputFolder):
    #    os.mkdir(outputFolder)
    inputName = 'all_day'
    journeyFile = joinPath(outputFolder, keyword + '_' + inputName + '_journey')
    journey = getJourneyByKeyword(logs, rawKeyword)
    saveRDDToHDFS(journey, journeyFile)

def generateJourneys():
    logs = readParsedLogsFromHDFS(entireDayParsedLogsFolder1)
    keywords = ['nike air max', 'spor ayyakabı', 'tv unitesi', 'kot ceket', 'camasir makinesi', 'bosch', 'köpek maması']
    for keyword in keywords[3:]:
        #print_('Day1_' + keyword.replace(' ', '_') + '_Data')
        generateJourney(logs, keyword)

def countJourneys():
    counts = []
    keywords = ['jant', 'nike air max', 'spor ayyakabı', 'tv unitesi', 'kot ceket', 'camasir makinesi', 'bosch', 'köpek maması']
    for keyword in keywords:
        keyword = keyword.replace(' ', '_')
        outputFolder = joinPath(HDFSDataFolder, 'Day1_' + keyword + '_Data')
        inputName = 'all_day'
        journeyFile = joinPath(outputFolder, keyword + '_' + inputName + '_journey')
        journey = readJourneyFromHDFS(journeyFile)
        c = journey.count()
        counts.append((keyword, c))
        print_(journeyFile, 'contains', c, 'logs,', nowStr())
    for k, c in counts:
        print_(k, '=', c, 'relevant logs')

def extractLabeledPairsFromJourneyTest(keyword, inputName, journeyFile, productsFile, outputFolder):
    keyword = keyword.replace(' ', '_')
    journey = readJourneyFromHDFS(journeyFile)
    modulizedIds = getLabeledPairsWithModulizedIds(journey)
    labeledPairsFile = inputName + '_' + keyword + '_' + 'labeledPairs'
    modulizedIds['labeledPairs'].saveAsTextFile(joinPath(outputFolder, labeledPairsFile))
    print_(labeledPairsFile, 'have been saved successfully by', nowStr())
    products = getProducts(modulizedIds['listed'], productsFile)
    journeyProductsFile = inputName + '_' + keyword + '_' + 'journey_products'
    products.saveAsTextFile(joinPath(outputFolder, journeyProductsFile))
    print_(journeyProductsFile, 'have been saved successfully by', nowStr())
    trainData = generateTrainData(modulizedIds['labeledPairs'], products)
    saveTrainDataToHDFS(trainData, outputFolder, inputName, keyword)
    return trainData

def trainDataGenerationTest(keyword): 
    keyword = keyword.replace(' ', '_')
    inputName = 'all_day'
    outputFolder = joinPath(HDFSDataFolder, 'Day1_' + keyword + '_Data')
    journeyFile = joinPath(outputFolder, inputName + '_journey')
    productsFile = None
    return extractLabeledPairsFromJourneyTest(keyword, inputName, journeyFile, productsFile, outputFolder)

def runtrainDataGenerationTest():
    counts = []
    keywords = ['jant', 'nike air max', 'spor ayyakabı', 'tv unitesi', 'kot ceket', 'camasir makinesi', 'bosch', 'köpek maması']
    for keyword in keywords[:1]:
        trainDataGenerationTest(keyword)

def trainLocalDataTest():
    #trainIPhone6DataGenerationTest()
    #generateAllTrainData()
    #trainTestOnIPhone6Data()
    #rankingTestOnIPhone6Data()
    #userBehaviorTestOnIPhone6Data()
    #parseAllDayTest()
    #trainDataGenerationTest() 
    #generateJourneys()
    #countJourneys()
    runtrainDataGenerationTest()