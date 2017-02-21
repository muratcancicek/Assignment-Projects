from JsonIO import *
from LogsReader import *
import LogsReader 

TEST_LOGS_FILE = 'part-r-00000'
TEST_LOGS = joinPath(clickstreamFolder, TEST_LOGS_FILE)
testFolder = joinPath(logInfoFolder, TEST_LOGS_FILE)

def setTestFile(testFile):
    TEST_LOGS_FILE = testFile
    TEST_LOGS = joinPath(clickstreamFolder, TEST_LOGS_FILE)
    testFolder = joinPath(logInfoFolder, TEST_LOGS_FILE)

def checkDuplication():
    logs = LogsReader.readLogs(TEST_LOGS, duplicated = True)
    deduplicatedLogs = list(set(logs))
    logsCount = len(logs)
    deduplicatedLogsCount = len(deduplicatedLogs)
    duplicationCount = logsCount - deduplicatedLogsCount
    duplicated = logsCount != deduplicatedLogsCount
    print 'Duplication occurred:', duplicated, duplicationCount, logsCount, deduplicatedLogsCount

lastReadLogs = None
def getLogs(logs = None, fromFileName = TEST_LOGS):
    if logs == None:
        if lastReadLogs != None and fromFileName == TEST_LOGS:
            return lastReadLogs
        else:
            return LogsReader.getLogs(fromFileName)

    else:
        return logs

def generateParsedTestFile(fromFileName = TEST_LOGS, toFileName = joinPath(testFolder, TEST_LOGS_FILE)):
    LogsReader.generateParsedLogs(fromFileName, toFileName)

def infoExists(fileName):
    return os.path.exists(fileName + '.json')

def extractLogKeys(logs = None, fromFileName = TEST_LOGS, toFileName = 'keyList'):
    logs = getLogs(logs, fromFileName)
    keys = set()
    for log in logs:
        keys.update(log.keys())
    keys = list(keys)
    if LogsReader.WRITING_ALLOWED:
        writeToJson(keys, joinPath(testFolder, toFileName))
    return keys   
    
def readLogKeys(logs = None, fileName = 'keyList'):
    fileName = joinPath(testFolder, fileName)
    if not (infoExists(fileName) and LogsReader.WRITING_ALLOWED):
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
    if LogsReader.WRITING_ALLOWED:
        writeToJson(transpose, joinPath(testFolder, toFileName))
        writeToJson(transposeClean, joinPath(testFolder, toFileName + '_clean'))
    else:
        print 'Transposes has been generated' 
    return transpose, transposeClean
    
def readTransposes(logs = None, fileName = 'transpose'):
    fileName = joinPath(testFolder, fileName)
    if not (infoExists(fileName) and LogsReader.WRITING_ALLOWED):
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
    if LogsReader.WRITING_ALLOWED:
        writeToJson(totalCounts, joinPath(testFolder, toFileName + 'OfValues'))
        writeToJson(valueCounts, joinPath(testFolder, toFileName + 'OfUniqueValues'))
    return totalCounts, valueCounts
    
def readCounts(logs = None, fileName = 'counts'):
    totalCountsFileName = joinPath(testFolder, fileName + 'OfValues')
    valueCountsFileName = joinPath(testFolder, fileName + 'OfUniqueValues')
    if not (infoExists(fileName) and LogsReader.WRITING_ALLOWED):
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
    logs = getLogs(logs, fromFileName) 
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
    logs = getLogs(logs)
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

def hasSearchThisItem(searchLog, itemLog):
    if not 'ids' in searchLog.keys() or not 'id' in itemLog.keys():
        return False
    return itemLog['id'] in searchLog['ids'] 

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

def getJourneyFromCookie(cookie, logs = None): 
    logs = getLogs(logs) 
    modules = getModuleMap(logs)   
    paymentIds = getLogsColumnAsList('id', modules['payment'])
    cartIds = getLogsColumnAsList('id', modules['cart'])    
    commonIds = [id for id in paymentIds if id in cartIds]
    paymentIdCookies = getSnippedLogs(['id', '_c'], modules['payment'])
    focusedModules = ['newsession', 'search', 'item' 'cart', 'payment']
    focusedLogs = getLogsWhereValue(focusedModules, 'module', logs)
    myLogs = []
    for paymentLog in paymentIdCookies:
        for log in focusedLogs:
            if log['module'] =='search': 
                if hasSearchThisItem(log, paymentLog):
                    myLogs.append(log)
            else:
                if logsMatching(log, paymentLog, ['_c']):
                    myLogs.append(log)
    sampleJourney = getLogsWhereValue(cookie, '_c', myLogs)
    sampleJourney.sort(key = lambda log: log['timestamp'])
    return sampleJourney