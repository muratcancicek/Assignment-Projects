from Sparker.MLlibTests.MlLibHelper import *
from .ProductPreferrer import *
from .FakeProductGenerator import *
from .TrainDataGenerator import *
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
   allDayPath, outputPath = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/session/2016-12-26', joinPath('/user/root/Parsed', entireDay2 + '_parsed')
   print_('Output Folder:', outputPath)
   parseAllDay(allDayPath, outputPath)
   
def trainDataGenerationTest():
    logs = None #readParsedLogsFromHDFS(entireDayParsedLogsFolder1)
    keyword = 'jant'
    outputFolder = joinPath(HDFSDataFolder, 'Day1_jant_Data')
    generateTrainData(logs, keyword, outputFolder)

def trainPairWiseDataTest():
    keywords = ['iphone 6', 'jant', 'nike air max', 'tv unitesi', 'kot ceket', 'camasir makinesi', 'bosch']
    for keyword in keywords:
        trainPairWiseDataTestKeyword(keyword)

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
    #runtrainDataGenerationTest()
    #trainDataGenerationTest('iphone 6')
    #trainPairWiseDataTestKeyword()
    #trainPairWiseDataTest()
    runUpdatedTrainDataGenerationTest(i = 1)