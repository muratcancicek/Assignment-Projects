from paths import *
from MainSrc.PythonVersionHandler import *
from Sparker.NewJourneyExtractor.BotFilter import *
from Sparker.NewJourneyExtractor.Sessionizer import *
from Sparker.NewJourneyExtractor.SearchExtractor import *
from Sparker.NewJourneyExtractor.NewProductPreferrer import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from Sparker.SparkLogProcesser.SparkLogFileHandler import *

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

def getPreparedLogsFromHDFS(inputPaths):
    logs = readAndFilterLogs(inputPaths)
    return parseAllLogs(logs)

def extractLogsByKeywordsFromHDFS(inputPaths, keywords):
    return searchNProductLogsByKeywords(logs, keywords)

def saveExtractedLogsByKeywordsFromHDFS(inputPaths, keywords, outputPath):
    keywordDict = extractLogsByKeywordsFromHDFS(inputPaths, keywords)
    objectiveLogs = sc_().parallelize([])
    for v in keywordDict:
        (searches, viewedProductLogs, cartedOrPaidProductLogs) = keywordDict[v]
        objectiveLogs = objectiveLogs.union(searches).union(viewedProductLogs).union(cartedOrPaidProductLogs)
    objectiveLogs = objectiveLogs.coalesce(24)
    saveRDDToHDFS(objectiveLogs, outputPath)

#def getTrainingPairs():