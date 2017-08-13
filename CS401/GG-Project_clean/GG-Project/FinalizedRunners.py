from paths import *
from PythonVersionHandler import *
from BotFilter import *
from Sessionizer import *
from SearchExtractor import *
from NewProductPreferrer import *
from SparkLogReader import *
from SparkLogFileHandler import *

def readLogsFromMultiplePaths(inputPaths):
    logs = sc_().parallelize([])
    for p in inputPaths:
        logs.union(readLogs(sc_(), p, True))

def readAndFilterLogs(inputPaths):
    if isinstance(inputPaths, str):
        logs = readLogs(sc_(), inputPaths, True)
    else:
        logs = readLogsFromMultiplePaths(inputPaths)
    return filterLogsForBots(logs)

def getPreparedLogsFromHDFS(inputPaths, filtering = True):
    if filtering:
        logs = readAndFilterLogs(inputPaths)
        logs = parseAllLogs(logs)
    else:
        logs = sc_().parallelize([])
        for p in inputPaths:
            logs = readParsedLogsFromHDFS(p)
    print_logging(logs.count(), 'have been prepared by', nowStr())
    return logs

def extractLogsByKeywordsFromHDFS(inputPaths, keywords, filtering = True):
    logs = getPreparedLogsFromHDFS(inputPaths, filtering = filtering)
    return searchNProductLogsByKeywords(logs, keywords)

def saveExtractedLogsByKeywordsFromHDFS(inputPaths, keywords, outputPath, filtering = True):
    keywordDict = extractLogsByKeywordsFromHDFS(inputPaths, keywords, filtering = filtering)
    objectiveLogs = sc_().parallelize([])
    for v in keywordDict:
        (searches, viewedProductLogs, cartedOrPaidProductLogs) = keywordDict[v]
        objectiveLogs = objectiveLogs.union(searches).union(viewedProductLogs).union(cartedOrPaidProductLogs)
    print_logging('Objective logs has been merged by', nowStr())
    objectiveLogs = objectiveLogs.coalesce(24)
    saveRDDToHDFS(objectiveLogs, outputPath)