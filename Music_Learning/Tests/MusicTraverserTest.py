from FeatureProcesser.FeatureAnalyzer import *
from FeatureProcesser.GenreAnalyzer import *
from FeatureLearner.SVMTrainer import *
from paths import *
    
testInputFolder = 'D:\\OneDrive\Music\\Classical Music Top 100\\ncesaz_-_7_Yollar___Roads_2011mp3yolu.net\\İncesaz - 7 Yollar & Roads (2011)\\'
testOutputFolder = joinPath(trainDataFolder, 'Classical Music Top 100\\ncesaz_-_7_Yollar___Roads_2011mp3yolu.net\\İncesaz - 7 Yollar & Roads (2011)\\')

def printFilesTest():
    #subFoldersubFolderss = getSubDirs(musicFolder)
    #traverseDirTree(musicFolder, listFileTypes)
    #print_({t: allTypes.count(t) for t in unique(allTypes) if t in supportedTypes})
    #makeTrainFolder(musicFolder, trainDataFolder)
    print_('Acoustic features will be extracted.')

def runtraverseMusicTest():
    featuresList = collectFeaturesList()
    trainData, testData, testCounts = generateTrainData(featuresList)
    for c in range(4):
        experienceSVMTrain(trainData, testData, testCounts, c)