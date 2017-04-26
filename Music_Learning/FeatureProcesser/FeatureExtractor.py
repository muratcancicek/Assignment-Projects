from Extractor.ExtractorRunner import run as runExtractor 
from FeatureProcesser.MusicTraverser import *
from paths import *

def makeTrainFolder(inputFolder, outputFolder):
    def makeFolder(dir):
        newFolder = getFixedEncodingValue(dir.replace(inputFolder, outputFolder))
        if not os.path.exists(newFolder):
            os.mkdir(newFolder)
    traverseDirTree(inputFolder, makeFolder)

def extractFeaturesFromFolder(inputFolder, outputFolder):
    def processFile(path):
        fileType = getFileType(path)
        if not fileType in supportedTypes: return
        features = path.replace(inputFolder, outputFolder).replace('.'+fileType, '.json')
        features = getFixedEncodingValue(features)
        if os.path.exists(features): pass
            #print_(features, 'already exists, will be skipped.')
        else: 
            try:
                path0 = path.encode('ascii')
            except UnicodeEncodeError:
                print_(features, 'has unicode problems, will be skipped.')
                return
            runExtractor(path, features)
         
    def processFolder(dir):
        newFolder = getFixedEncodingValue(dir.replace(inputFolder, outputFolder))
        if not os.path.exists(newFolder):
            os.mkdir(newFolder)
            print_(newFolder, 'cannot be found, will be created now.')
        for file in getFilesIn(dir):
            processFile(joinPath(dir, file))
    traverseDirTree(inputFolder, processFolder)

def extractFeatures():
    extractFeaturesFromFolder(musicFolder,trainDataFolder)
