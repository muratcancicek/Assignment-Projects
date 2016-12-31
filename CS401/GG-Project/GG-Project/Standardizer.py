from SpecsReader import * 
from Quantizer import *
from BsonIO import *
import math

def generateMeansMap(map, fileName = 'MeanMap.bson'):
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
    
def generateSDMap(map,meanMap, fileName = 'SDMap.bson'): 
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

def generateZ_ScoredMap(map,meanMap,SDMap, fileName = 'ScoresMap.bson'):
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

def preprocessData(valuesFile = 'ValueMap.bson', meansFile = 'MeanMap.bson', SDFile = 'SDMap.bson', scoresFile = 'ScoresMap.bson'):
    specsDict = getAllCategorySpecs() 
    generateQuantizedValuesMap(specsDict, valuesFile)
    map = evalBson(valuesFile)
    generateMeansMap(map, meansFile)
    meanMap = evalBson(meansFile)
    generateSDMap(map, meanMap, SDFile)
    SDMap = evalBson(SDFile)
    generateZ_ScoredMap(map, meanMap, SDMap, scoresFile)
    ScoresMap = evalBson(scoresFile)
    print ScoresMap['phda']['Plak Türü']['10" (inch)']
    print SDMap['tc']['Yüz Algılama']