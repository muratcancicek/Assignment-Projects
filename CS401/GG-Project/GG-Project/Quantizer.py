from SpecsReader import *
from BsonIO import *

def getSpecValueCounts(specsDict, categoryCode):
    categorySpecs = specsDict[categoryCode]  
    specList = categorySpecs['categorySpecTypeList']
    specsCounts = {}
    for spec in specList:
        name = spec['specName']
        specD = spec['categorySpecDataTypeList']
        specsCounts[name] = len(specD)# if specD != None else 3131322
    return specsCounts

def generateSpecsCountsMap(specsDict, fileName = 'SpecsCounts.bson'):
    outerDict = {}
    for code, spec in specsDict.items():
        specMap = getSpecValueCounts(specsDict, code)
        outerDict[code] = specMap
    writeToBson(outerDict, fileName)

def getSpecsTypes(specsDict, categoryCode):
    typeList = []
    categorySpecs = specsDict[categoryCode]  
    specList = categorySpecs['categorySpecTypeList']
    specsTypes = {}
    for spec in specList:
        name = spec['specName']
        specD = spec['elementType']
        typeList.append(specD)
        specsTypes[name] = specD
    return specsTypes, typeList

def generateSpecsTypesMap(specsDict, fileName = 'SpecsTypes.bson'):
    outerDict = {}
    for code, spec in specsDict.items():
        specMap, typeList = getSpecsTypes(specsDict, code)
        outerDict[code] = specMap
    writeToBson(outerDict, fileName)

def generateSpecsTypeCountsMap(specsDict,fileName = 'SpecsTypes.bson'):
    outerDict = {}
    typeList = []
    for code, spec in specsDict.items():
        specMap, specTypeList = getSpecsTypes(specsDict, code)
        typeList.extend(specTypeList)
    typeSet = list(set(typeList))
    for t in typeSet:
        outerDict[t] = typeList.count(t)
    writeToBson(outerDict, fileName)

def generateSpecsStatistics(countsFile = 'SpecsCounts.bson', typesFile = 'SpecsTypes.bson', typesCountsFile = 'SpecsTypesCounts.bson'):
    specsDict = getAllCategorySpecs() 
    generateSpecsCountsMap(specsDict, countsFile)
    generateSpecsTypesMap(specsDict, typesFile)
    generateSpecsTypeCountsMap(specsDict, typesCountsFile) 
    typeCounts = evalBson(typesCountsFile)
    print typeCounts

def assignQuantizedValues(specsDict, categoryCode):
    categorySpecs = specsDict[categoryCode]  
    specList = categorySpecs['categorySpecTypeList']
    specDict = {}
    for spec in specList:
        name = spec['specName']
        specDList = spec['categorySpecDataTypeList']
        valueDict = {}
        count = 1
        for value in specDList:
            valueName = value['specDataName']
            if '\"' in valueName:
                valueName = fixQuotes(valueName)
            valueDict[valueName] = count
            count += 1
        specDict[name] = valueDict
    return specDict

def generateQuantizedValuesMap(specsDict, fileName = 'ValueMap.bson'):
    outerDict = {}
    for code, spec in specsDict.items():
        specMap = assignQuantizedValues(specsDict, code)
        outerDict[code] = specMap
    writeToBson(outerDict, fileName)
