from MainSrc.PythonVersionHandler import *
from .LogFileHandler import *
from .LogReader import *
from .JsonIO import *
from paths import *

def unique(list1):
    return list(set(list1))

def checkDuplication():
    logs = LogReader.readLogs(TEST_LOGS, duplicated = True)
    deduplicatedLogs = unique(logs)
    logsCount = len(logs)
    deduplicatedLogsCount = len(deduplicatedLogs)
    duplicationCount = logsCount - deduplicatedLogsCount
    duplicated = logsCount != deduplicatedLogsCount
    print_('Duplication occurred:', duplicated, duplicationCount, logsCount, deduplicatedLogsCount)

def generateParsedTestFile(fromFileName = TEST_LOGS, toFileName = joinPath(testFolder, TEST_LOGS_FILE)):
    LogReader.generateParsedLogs(fromFileName, toFileName)

def infoExists(fileName):
    return os.path.exists(fileName + '.json')

def extractLogKeys(logs = None, fromFileName = TEST_LOGS, toFileName = 'keyList'):
    logs = getLogs(logs, fromFileName)
    keys = set()
    for log in logs:
        keys.update(log.keys())
    keys = list(keys)
    if LogReader.WRITING_ALLOWED:
        writeToJson(keys, joinPath(testFolder, toFileName))
    return keys   
    
def readLogKeys(logs = None, fileName = 'keyList'):
    fileName = joinPath(testFolder, fileName)
    if not (infoExists(fileName) and LogReader.WRITING_ALLOWED):
        return extractLogKeys(logs)
    return evalJson(fileName)

def getSnippedLogs(keys, logs = None, fromFileName = TEST_LOGS, toFileName = 'transpose'): 
    logs = getLogs(logs, fromFileName)
    snippedLogs = []
    if isinstance(keys, str):
        keys = [keys]
    for log in logs:
        snippedLog = {}
        for key in keys:
            if key in log.keys():
                snippedLog[key] = log[key]
            else:
                snippedLog[key] = None
        snippedLogs.append(snippedLog)
    return snippedLogs

transpose = None
transposeClean = None
def takeTransposesOfLogs(logs = None, fromFileName = TEST_LOGS, toFileName = 'transpose'):
    logs = getLogs(logs, fromFileName)
    logKeys = readLogKeys(logs)
    global transpose, transposeClean
    transpose = {}
    transposeClean = {}
    for key in logKeys:
        transpose[key] = []
        transposeClean[key] = []
    for log in logs:
        for key in logKeys:
            if key in log.keys():
                transpose[key].append(log[key])
                transposeClean[key].append(log[key])
            else:
                transpose[key].append(None)
    if LogReader.WRITING_ALLOWED:
        writeToJson(transpose, joinPath(testFolder, toFileName))
        writeToJson(transposeClean, joinPath(testFolder, toFileName + '_clean'))
    else:
        print_('Transposes has been generated' )
    return transpose, transposeClean
    
def readTransposes(logs = None, fileName = 'transpose'):
    fileName = joinPath(testFolder, fileName)
    if not (infoExists(fileName) and LogReader.WRITING_ALLOWED):
        return takeTransposesOfLogs(logs)
    return evalJson(fileName), evalJson(fileName + '_clean')

def getSubTranspose(keys, logs = None, fromFileName = TEST_LOGS): 
    if transpose == None:
        logs = getLogs(logs, fromFileName)
        subTranspose = {}
        for key in keys:
            subTranspose[key] = []
        for log in logs:
            for key in keys:
                subTranspose[key] = log[key] if key in log.keys() else None                
        return subTranspose
    else:
        return  {key: transpose[key] for key in keys}

def extractCounts(logs = None, fromFileName = TEST_LOGS, toFileName = 'counts'):
    logs = getLogs(logs, fromFileName)
    logKeys = readLogKeys(logs)
    transpose, cleenTranspose = readTransposes(logs)
    totalCounts = {}
    valueCounts = {}
    for key in logKeys:
        totalCounts[key] = len(cleenTranspose[key])
        valueCounts[key] = len(list(set(cleenTranspose[key])))
    if LogReader.WRITING_ALLOWED:
        writeToJson(totalCounts, joinPath(testFolder, toFileName + 'OfValues'))
        writeToJson(valueCounts, joinPath(testFolder, toFileName + 'OfUniqueValues'))
    return totalCounts, valueCounts
    
def readCounts(logs = None, fileName = 'counts'):
    totalCountsFileName = joinPath(testFolder, fileName + 'OfValues')
    valueCountsFileName = joinPath(testFolder, fileName + 'OfUniqueValues')
    if not (infoExists(fileName) and LogReader.WRITING_ALLOWED):
        return extractCounts(logs)
    return evalJson(totalCountsFileName), evalJson(valueCountsFileName)

def getLogsColumnAsList(key, logs = None, fromFileName = TEST_LOGS):
    if transpose == None:
        logs = getLogs(logs, fromFileName)
        return map(lambda log: log[key] if key in log.keys() else None, logs)
    else:
        return transpose[key]
    
def isMatching(valueMap, log):
    for key, value in valueMap.items():
        if not key in log.keys():
            return False
        elif isinstance(value, list) and log[key] in value:
            return True 
        elif not key in log.keys() or log[key] != value:
            return False
        else:
            return True

def getLogsWhere(valueMap, logs = None, fromFileName = TEST_LOGS): 
    #logs = getLogs(logs, fromFileName) 
    selectedLogs = []
    indices = []
    for i in range(len(logs)):
        if isMatching(valueMap, logs[i]):
            selectedLogs.append(logs[i])
            indices.append(i)
    return selectedLogs#, indices

def getLogsWhereValue(value, key = None, logs = None, fromFileName = TEST_LOGS):
    if key == None:
        logs = getLogs(logs, fromFileName) 
        selectedLogs = []
        indices = []
        for i in range(len(logs)):
            for logKey in logs[i].keys():
                if isMatching({logKey: value}, logs[i]):
                    selectedLogs.append(logs[i])
                    indices.append(i)
                    break
        return selectedLogs#, indices
    else:
        return getLogsWhere({key: value}, logs, fromFileName)
    
def getModuleMap(logs = None, modules = None): 
    #logs = getLogs(logs)
    moduleMap = {}
    if modules == None:
        for log in logs:
            if log['module'] in moduleMap.keys():
                moduleMap[log['module']].append(log)
            else:
                moduleMap[log['module']] = [log]
    else:
        for module in modules:
            moduleMap[module], indices = getLogsWhereValue(module, 'module', logs = logs)
    return moduleMap

def getModuleCounts(logs = None, modules = None): 
    if logs == None:
        logs = getLogs(logs)
    if isinstance(logs, list):
        logs = getModuleMap(logs)
    counts = {}
    if modules == None:
        for key, logLists in logs.items():
            counts[key] = len(logLists)
    else:
        for module in modules:
            if module in logs.keys():
                counts[module] = len(logs[module])
            else:
                counts[module] = 0
    return counts

def hasSearchThisProduct(searchLog, productLog):
    if not 'ids' in searchLog.keys() or not 'id' in productLog.keys():
        return False
    if isinstance(searchLog['ids'], str):
        return str(productLog['id']) == searchLog['ids']
    else:
        return productLog['id'] in searchLog['ids'] 

def findProductIndexOnSearch(searchLog, productLog):
    if not 'ids' in searchLog.keys() or not 'id' in productLog.keys():
        return -1
    if isinstance(searchLog['ids'], str):
        return 0 if str(productLog['id']) == searchLog['ids'] else -1
    else:
        return searchLog['ids'].index(productLog['id'])

def logsMatching(first, second, keys = None):
    if keys == None:
        keys = [key for key in first.keys() if key in second.keys()]
    elif isinstance(keys, str):
        keys = [keys]
    for key in keys:
        if key in first.keys() and key in second.keys():
            if first[key] != second[key]:
                return False
    return True

focusedModules = ['newsession', 'search', 'item' 'cart', 'payment']
def getJourneyFromCookie(cookie, logs = None): 
    logs = getLogs(logs) 
    modules = getModuleMap(logs)   
    paymentIds = getLogsColumnAsList('id', modules['payment'])
    cartIds = getLogsColumnAsList('id', modules['cart'])    
    commonIds = [id for id in paymentIds if id in cartIds]
    paymentIdCookies = getSnippedLogs(['id', '_c'], modules['payment'])
    focusedLogs = getLogsWhereValue(focusedModules, 'module', logs)
    myLogs = []
    for paymentLog in paymentIdCookies:
        for log in focusedLogs:
            if log['module'] =='search': 
                if hasSearchThisProduct(log, paymentLog):
                    myLogs.append(log)
            else:
                if logsMatching(log, paymentLog, ['_c']):
                    myLogs.append(log)
    sampleJourney = getLogsWhereValue(cookie, '_c', myLogs)
    sampleJourney.sort(key = lambda log: log['timestamp'])
    return sampleJourney

productModules = ['cart', 'payment', 'item']
def getProductLogs(modules):
    if isinstance(modules, list):
        modules = getModuleMap(modules)   
    logs = []
    for module in productModules:
        logs.extend(modules[module])
    return logs

def getSearchLogs(logs):
    return getLogsWhereValue('search', 'module', logs)

def isProductLog(log):
    return 'module' in log.keys() and log['module'] in productModules

def isSearchLog(log):
    return 'module' in log.keys() and log['module'] == 'search'

def getInterestingCookiesFromKeyword(modules, keyword):
    searches = getLogsWhereValue(keyword, 'keyword', modules['search'])
    productCookies = getLogsColumnAsList('_c', getProductLogs(modules))
    interestingCookies = []
    searchCookies = getLogsColumnAsList('_c', searches)
    for c in productCookies:
        if c in searchCookies and c != None:#
            interestingCookies.append(c)
    return list(set(interestingCookies))

def getIdsFromSearches(searches):
    if isinstance(searches, dict): searches = [searches]
    ids = []
    for search in searches:
        if 'ids' in search.keys():
            ids.extend(search['ids'] if isinstance(search['ids'], list) else [search['ids']])
    return ids

def getInterestingLogsFromKeyword(modules, keyword):
    searches = getLogsWhereValue(keyword, 'keyword', modules['search'])
    ids = getIdsFromSearches(searches)
    interestingCookies = getInterestingCookiesFromKeyword(modules, keyword)
    logs = getLogsWhereValue(interestingCookies, '_c', getProductLogs(modules) + modules['newsession'])
    interestingLogs = []
    for log in logs:
        if 'id' in log.keys() and log['id'] in ids:
            interestingLogs.append(log)
    return interestingLogs 

def findLastSearchContainsProduct(productLog, journey):
    searches = getLogsWhereValue('search', 'module', journey)
    searches.reverse()
    for i, search in enumerate(searches):
        if hasSearchThisProduct(search, productLog):
            return i, findProductIndexOnSearch(search, productLog)
    return -1, -1

def getJourneyByKeyword(modules, keyword):
    if isinstance(keyword, str): 
        keyword = [keyword] 
    if isinstance(modules, list):
        modules = getModuleMap(modules)   
    searches = getLogsWhereValue(keyword, 'keyword', modules['search'])
    interestingLogs = getInterestingLogsFromKeyword(modules, keyword)
    journey = searches + interestingLogs
    return sortedLogs(journey)

def cookieChanged(previousLog, currentLog):
    if previousLog == None or \
        ('_c' in previousLog.keys() and not '_c' in currentLog.keys()) or \
        (not '_c' in previousLog.keys() and '_c' in currentLog.keys()) or \
        (not '_c' in previousLog.keys() and not '_c' in currentLog.keys()):
        return False
    else:
        return previousLog['_c'] != currentLog['_c']

def groupLogsByCookie(logs):
    logs = sortedLogs(logs)    
    groupedLogs = []
    for i, log in enumerate(logs):
        if i == 0 or cookieChanged(logs[i-1], log):
            groupedLogs.append([])
        groupedLogs[-1].append(log) 
    return groupedLogs