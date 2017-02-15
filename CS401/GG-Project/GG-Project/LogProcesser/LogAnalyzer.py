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

def getLogs(logs = None, fromFileName = TEST_LOGS):
    if logs == None:
        return LogsReader.getLogs(fromFileName)
    else:
        return logs

def generateParsedTestFile(fromFileName = TEST_LOGS, toFileName = joinPath(logInfoFolder, TEST_LOGS_FILE)):
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
    return transpose, transposeClean
    
def readTransposes(logs = None, fileName = 'transpose'):
    fileName = joinPath(testFolder, fileName)
    if not (infoExists(fileName) and LogsReader.WRITING_ALLOWED):
        return takeTransposesOfLogs(logs)
    return evalJson(fileName), evalJson(fileName + '_clean')

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

def getIndicesValueOccurs(key, value, logs = None, fromFileName = TEST_LOGS):
    column = getLogsColumnAsList(key, logs)
    return [i for i in range(len(column)) if column[i] == value]