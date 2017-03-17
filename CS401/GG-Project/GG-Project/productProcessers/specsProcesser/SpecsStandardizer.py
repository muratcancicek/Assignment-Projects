from SpecsQuantizer import *
from SpecsReader import * 
from productProcessers.BsonIO import *
from paths import *
import math

def generateMeansMap(map, fileName = specsFolder + 'SpecsMeanMap.bson', products = None):
    products = readProducts(products)
    meanMap = {}
    for categoryCode, category in map.items():
        axisMeanMap = {}
        for axisName, axis in category.items():
            sum = 0
            for valueName, value in axis.items():
                 sum += value
            mean = float(sum)/len(axis)
            axisMeanMap[axisName.decode('utf8')] = mean
        meanMap[categoryCode] = axisMeanMap
    writeToBson(meanMap, fileName)
    
def generateSDMap(map,meanMap, fileName = specsFolder + 'SpecsSDMap.bson'): 
    SDMap = {}
    for categoryCode, category in map.items():
        axisSDMap = {}
        for axisName, axis in category.items():
            sum = 0
            for valueName, value in axis.items():
                 sum += (value - meanMap[categoryCode][axisName])**2 
            SD = math.sqrt(float(sum)/len(axis))
            axisSDMap[axisName.decode('utf8')] = SD
        SDMap[categoryCode] = axisSDMap
    writeToBson(SDMap, fileName)

def generateZ_ScoredMap(map,meanMap,SDMap, fileName = specsFolder + 'SpecsZ_ScoredValueMap.bson'):
    ScoresMap = {}
    for categoryCode, category in map.items():
        axisScoresMap = {}
        for axisName, axis in category.items():
            scoreValueMap = {}
            for valueName, value in axis.items():
                 if '\"' in valueName:
                  valueName = fixQuotes(valueName)
                 if SDMap[categoryCode][axisName] != 0:
                  scoreValueMap[valueName] = (value - meanMap[categoryCode][axisName])/SDMap[categoryCode][axisName]
                 else:
                    #print valueName,value,SDMap[categoryCode][axisName]
                    scoreValueMap[valueName] = 12
            axisScoresMap[axisName] = scoreValueMap
        ScoresMap[categoryCode] = axisScoresMap
    writeToBson(ScoresMap, fileName)

def preprocessSpecsData(valuesFile = 'SpecsValueMap.bson', meansFile = 'SpecsMeanMap.bson', SDFile = 'SpecsSDMap.bson', scoresFile = 'SpecsZ_ScoredValueMap.bson'):
    specsDict = getAllCategorySpecs() 
    global specsFolder 
    generateQuantizedValuesMap(specsDict, specsFolder + valuesFile)
    map = evalBson(specsFolder + valuesFile)
    generateMeansMap(map, specsFolder + meansFile)
    meanMap = evalBson(specsFolder + meansFile)
    generateSDMap(map, meanMap, specsFolder + SDFile)
    SDMap = evalBson(specsFolder + SDFile)
    generateZ_ScoredMap(map, meanMap, SDMap, specsFolder + scoresFile)
    scoresMap = evalBson(specsFolder + scoresFile)
    return scoresMap