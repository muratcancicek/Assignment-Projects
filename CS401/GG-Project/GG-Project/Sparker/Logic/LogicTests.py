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
    runTrainingExperiment(trainData, testData, modelName, True)
    
def trainLocalDataTest():
    #trainIPhone6DataGenerationTest()
    trainTestOnIPhone6Data()
    #extractJourneyLogsFromDay0(4)
    #mergeJourneys()