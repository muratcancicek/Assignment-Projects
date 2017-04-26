from paths import *
from FeatureProcesser.FeatureAnalyzer import *
from SystemHelpers.JsonIO import *

def getFlattenDict(features, map = None, preKey = ''):
    if map == None: map = {}
    for k, i in features.items():
        #if k in ['tags', "beats_position"]: continue
        if isinstance(i, dict):
                map = getFlattenDict(i, map, k if preKey == '' else preKey + '_' + k)
        elif isinstance(i, list):
            if len(i) == 1:
                map[preKey + '_' + k] = i[0]
            else:
                map[preKey + '_' + k] = i
        elif isinstance(i, float) or isinstance(i, int) or isinstance(i, str):
            map[preKey + '_' + k] = i
    return map

def collectFeaturesList():
    featuresList = []
    analyseAllFeatures(lambda features: featuresList.append(getFlattenDict(features)))
    #print_('unicodeDecodeErrorCount =', str(unicodeDecodeErrorCount)+',', 'JSONDecodeErrorCount =', str(JSONDecodeErrorCount)+',',
    #     'FeaturesListCount =',  len(featuresList))
    print_(len(featuresList), 'features have been collected from different folders successfully by', nowStr())
    return featuresList

def generateFeaturesList(featuresList = None, fileName = 'featuresList', printing = False):
    if featuresList == None: featuresList = collectFeaturesList()
    fileName = joinPath(Acoustic_Features_OfflineFolder, fileName)
    writeToJsonRaw(featuresList, fileName, printText = printing)

def readFeaturesList(fileName = 'featuresList'):
    fileName = joinPath(Acoustic_Features_OfflineFolder, fileName)
    return evalJson(fileName)

def generateFeatureKeyList(featuresList = None, toFileName = 'featureKeyList', printing = False):
    if featuresList == None: featuresList = collectFeaturesList()
    keys = set()
    for features in featuresList:
        keys.update(features.keys())
    keys = list(keys)
    writeToJson(keys, joinPath(AcousticFeaturesFolder, toFileName), printing = printing)
    return keys   

def checkFeaturesCount(featuresList):
    length = len(featuresList[0])
    print_(length)
    for features in featuresList:
        if length != len(features):
            for k in features.keys():
                if not k in featuresList[0].keys():
                    print_(k)

def readFeaturesKeyList(fileName = 'featureKeyList'):
    return evalJson(joinPath(AcousticFeaturesFolder, fileName))

def generateFeaturesValueLists(fileName = 'featureValueLists', featuresList = None, printing = False):
    if featuresList == None: featuresList = collectFeaturesList()
    featureList = readFeaturesKeyList()
    featureValueLists = {}
    for field in featureList:
        featureValueLists[field] = []
    for features in featuresList:
        for field in featureList:
            if not field in features.keys(): continue
            if isinstance(features[field], list):
                if len(features[field]) == 1:
                    featureValueLists[field].append(features[field][0])
                else:
                    featureValueLists[field].append(len(features[field]))
            else:
                featureValueLists[field].append(features[field])
    fileName = joinPath(AcousticFeaturesFolder, fileName)
    writeToJsonRaw(featureValueLists, fileName, printText = printing, sort = False)

def readFeaturesValueLists(fileName = 'featureValueLists'):
    fileName = joinPath(AcousticFeaturesFolder, fileName)
    return evalJson(fileName)

def containsType(l, t):
    for e in l:
        if t == None:
            if e == None:
                return True
        elif isinstance(e, t):
            return True
        return False

def setWithNone(l):
    li = [e for e in l if e != None]
    li.append(None)
    return li

def getTypeOfListElement(l):
    li = setWithNone(l)
    if len(li) == 0:
        return type(None).__name__
    else:
        return type(li[0]).__name__

def generateFeaturesValueTypes(fileName = 'featureValueTypes',  featuresList = None, printing = False):
    if featuresList == None: featuresList = collectFeaturesList()
    featureValueLists = readFeaturesValueLists()
    featureValueTypes = {}
    for field, fieldList in featureValueLists.items():
            featureValueTypes[field] = getTypeOfListElement(fieldList)
    fileName = joinPath(AcousticFeaturesFolder, fileName)
    writeToJsonRaw(featureValueTypes, fileName, printText = printing)

def readFeaturesValueTypes(fileName = 'featureValueTypes'):
    fileName = joinPath(AcousticFeaturesFolder, fileName)
    return evalJson(fileName)

def generateFeaturesValueTypeCounts(fileName = 'featureValueTypeCounts',  featuresList = None, printing = False):
    featureValueTypes = readFeaturesValueTypes()
    typeCounts = {}
    typeList = list(featureValueTypes.values())
    typeSet = list(set(typeList))
    for type in typeSet:
        typeCounts[type] = typeList.count(type)
    fileName = joinPath(AcousticFeaturesFolder, fileName)
    writeToJsonRaw(typeCounts, fileName, printText = printing)

def generateFeaturesValueSets(fileName = 'featureValueSets',  featuresList = None, printing = False):
    if featuresList == None: featuresList = collectFeaturesList()
    featureValueLists = readFeaturesValueLists()
    featureValueSets = {}
    #originalSets = evalJson(valuesFolder + 'features_Values.json')
    for field, fieldList in list(featureValueLists.items()):
        if containsType(fieldList, None):
            fieldList = setWithNone(fieldList)
        if not (containsType(fieldList, dict) or containsType(fieldList, list)):
            fieldList = list(set(fieldList))
        #if field in originalSets.keys():
        #    fieldList.extend([value for value in originalSets[field] if not value in fieldList])
        featureValueSets[field] = fieldList
    fileName = joinPath(AcousticFeaturesFolder, fileName)
    writeToJsonRaw(featureValueSets, fileName, printText = printing)
    
def readFeaturesValueSets(fileName = 'featureValueSets'):
    fileName = joinPath(AcousticFeaturesFolder, fileName)
    return evalJson(fileName)

def generateFeaturesValueCounts(fileName = 'featureValueCounts',  featuresList = None, printing = False):
    featureValueSets = readFeaturesValueSets()
    valueCounts = {}
    for k, v in featureValueSets.items():
        valueCounts[k] = len(v)
    fileName = joinPath(AcousticFeaturesFolder, fileName)
    writeToJsonRaw(valueCounts, fileName, printText = printing)

def readFeaturesValueCounts(fileName = 'featureValueCounts'):
    fileName = joinPath(AcousticFeaturesFolder, fileName)
    return evalJson(fileName)

def generateFeaturesStatistics(featuresList = None, printing = False):
    if featuresList == None: featuresList = collectFeaturesList()
    generateFeatureKeyList(featuresList = featuresList, printing = printing)
    generateFeaturesValueLists(featuresList = featuresList, printing = printing)
    generateFeaturesValueTypes(featuresList = featuresList, printing = printing)
    generateFeaturesValueSets(featuresList = featuresList, printing = printing)
    generateFeaturesValueCounts(featuresList = featuresList, printing = printing)
    generateFeaturesValueTypeCounts(featuresList = featuresList, printing = printing)

def readFeaturesStatistics(featuresList = None, regenerate = False):
    if regenerate:
         featuresList = readFeatures(featuresList)
         generateFeaturesStatistics(featuresList)
    statistics = {}
    statistics["fieldList"] = readFeaturesKeyList()
    statistics["fieldValueLists"] = readFeaturesValueLists()
    statistics["fieldValueSets"] = readFeaturesValueSets()
    statistics["fieldValueTypes"] = readFeaturesValueTypes()
    statistics["fieldValueCounts"] = readFeaturesValueCounts()
    return statistics 

def generateFeaturesStatisticsJson(fileName = 'featureStatistics', featuresList = None, regenerate = False):
    if regenerate:
        if featuresList == None: featuresList = collectFeaturesList()
        generateFeaturesStatistics(featuresList)
    statistics = readFeaturesStatistics(featuresList)
    fileName = joinPath(Acoustic_Features_OfflineFolder, fileName)
    writeToJsonRaw(statistics, fileName)
    
def readFeaturesStatisticsJson(fileName = 'featureStatistics'):
    fileName = joinPath(Acoustic_Features_OfflineFolder, fileName)
    return evalJson(fileName)
   
def regenerateAllFeaturesStatistics():
    featuresList = collectFeaturesList()
    generateFeaturesList(featuresList)
    readFeaturesList()
    generateFeaturesStatisticsJson(featuresList = featuresList, regenerate = True)
    statistics = readFeaturesStatisticsJson()


     

