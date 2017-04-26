from FeatureProcesser.MusicTraverser import *
from paths import *
import json
    
unicodeDecodeErrorCount = 0
JSONDecodeErrorCount = 0
def analyseFeatures(featureFile, analyzeMethod):
    try:
        features = json.load(open(featureFile, 'r'))
    except UnicodeDecodeError:
        global unicodeDecodeErrorCount
        unicodeDecodeErrorCount += 1
        return 
    except json.decoder.JSONDecodeError:
        global JSONDecodeErrorCount
        JSONDecodeErrorCount += 1
        return 
    analyzeMethod(features)

def analyseFeaturesFromFolder(inputFolder, outputFolder, analyzeMethod):
    def processFile(path):
        fileType = getFileType(path)
        if not fileType in supportedTypes: return
        features = path.replace(inputFolder, outputFolder).replace('.'+fileType, '.json')
        features = getFixedEncodingValue(features)
        if os.path.exists(features):
            analyseFeatures(features, analyzeMethod)
         
    def processFolder(dir):
        newFolder = getFixedEncodingValue(dir.replace(inputFolder, outputFolder))
        if not os.path.exists(newFolder):
            os.mkdir(newFolder)
            print_(newFolder, 'cannot be found, will be created now.')
        for file in getFilesIn(dir):
            processFile(joinPath(dir, file))
    traverseDirTree(inputFolder, processFolder)

def countValues(features):
    text = ''
    for k, i in features.items():
        if k in ['tags', "beats_position"]: continue
        if isinstance(i, dict):
            text += countValues(i)
            #text += k + ': ' + str(len(i.keys())) + ', ' + countValues(i)
        elif isinstance(i, list):
            text += str(len(i)) + ', ' 
        elif isinstance(i, float) or isinstance(i, int):
            text += '1, ' 
    return text

def analyseCountFeatures(features):
    counts = countValues(features)
    sum = 0
    for c in eval('['+counts[:-1]+']'):
        sum += c
    print_(sum, counts)

def analyseAllFeatures(analyseMethod):
    analyseFeaturesFromFolder(musicFolder, trainDataFolder, analyseMethod)
