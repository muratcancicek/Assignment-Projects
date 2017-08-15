from paths import *
from PythonVersionHandler import *
from BotFilter import *
from Sessionizer import *
from ReadyTests import *
from ReadyTests2 import *
from FinalizedRunners import *
from SearchExtractor import *
from NewProductPreferrer import *
from SparkLogReader import *
from SparkLogFileHandler import *
from StringUtil import *

def may17ExtractionTest(day):
    dateStr = '2017-05-' + str(day)
    import paths, FinalizedRunners
    inputPath = paths.joinPath(may2017Folder, dateStr)
    keywords = get32Keywords()
    outputPath = paths.joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
    FinalizedRunners.saveExtractedLogsByKeywordsFromHDFS(inputPath, keywords, outputPath)
    
def pairLabellingFromObjectiveLogsTest(day):
    keywords = 'iphone 7' # get32Keywords() # "BEKO 9 KG CAMASIR MAKINESI" # 'tupperware' # get5Keywords() # _file_old
    dateStr = '2017-05-' + str(day)
    import paths, SparkLogFileHandler, SearchExtractor, FinalizedRunners
    extractedPath = paths.joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
    logs = SparkLogFileHandler.readParsedLogsFromHDFS(extractedPath)
    keywordDict = SearchExtractor.searchNProductLogsByKeywords(logs, keywords)
    trainingInstancesDict = FinalizedRunners.trainingInstancesByKeywords(keywordDict)

def m16():
    keywords = get32Keywords()
    import paths, FinalizedRunners
    inputPath = paths.joinPath(filteredLogsFromMayFolder, '2017-05-16_filtered')
    outputPath = paths.joinPath(filteredLogsFromMayFolder, '2017-05-16_extractedLogs')
    FinalizedRunners.saveExtractedLogsByKeywordsFromHDFS(inputPath, keywords, outputPath)

def printAct(day):
    keywords = 'iphone 7' # get32Keywords() # "BEKO 9 KG CAMASIR MAKINESI" # 'tupperware' # get5Keywords() # _file_old
    dateStr = '2017-05-' + str(day)
    import paths, SparkLogFileHandler, SearchExtractor
    extractedPath = paths.joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
    extractedPath = paths.joinPath(clickstreamFolder, 'part-r-00000_filtered_extracted_32_server')
    logs = SparkLogFileHandler.readParsedLogsFromHDFS(extractedPath)
    keywordDict = SearchExtractor.searchNProductLogsByKeywords(logs, keywords)  
    #sessions = sessionize(keywordDict['iphone 7'])
    #printSessionActions(sessions[0])

def joinTests():
    import SparkLogFileHandler
    searches = SparkLogFileHandler.sc_().parallelize([{'p': 'a', 'l': [7, 2, 6]}, {'p': 'b', 'l': [7, 87, 65]}, {'p': 'c', 'l': [1, 65, 6]}, {'p': 'd', 'l': [7, 1, 6]}]) 
    products = SparkLogFileHandler.sc_().parallelize([{'i': 1}, {'i': 2}, {'i': 7}, {'i': 65}, {'i': 87}, {'i': 999}])
    products2 = SparkLogFileHandler.sc_().parallelize([{'i': 1}, {'i': 45}, {'i': 87}, {'i': 999}])
    searches = searches.flatMap(lambda p: [(i, p) for i in p['l']]).collect()#.map(lambda p: (p['l'], p)).flatMap(lambda p: (p, p)).distinct()
    for search in searches:
        print(search)

    #products = products.map(lambda p: (p['i'], p))
    #products2 = products2.map(lambda p: (p['i'], p))
    #print(products.join(products2).collect())

def coalesceAll(days, p):
    for d in days:
        dateStr = '2017-05-' + str(d)
        import paths, SparkLogFileHandler, FinalizedRunners
        inputPath = paths.joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
        outputPath = paths.joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs_coalesced')
        logs = FinalizedRunners.getPreparedLogsFromHDFS(inputPath, filtering = False)
        logs = logs.coalesce(p)
        SparkLogFileHandler.saveRDDToHDFS(logs, outputPath)

def runNewExtractionMethods():
    #may17ExtractionTest(21)
    #printAct(16)
    #joinTests()
    coalesceAll([16, 18, 19], 24)