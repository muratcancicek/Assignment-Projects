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
    inputPath = joinPath(may2017Folder, dateStr)
    keywords = get32Keywords()
    outputPath = joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
    saveExtractedLogsByKeywordsFromHDFS(inputPath, keywords, outputPath)
    
def pairLabellingFromObjectiveLogsTest(day):
    keywords = 'iphone 7' # get32Keywords() # "BEKO 9 KG CAMASIR MAKINESI" # 'tupperware' # get5Keywords() # _file_old
    dateStr = '2017-05-' + str(day)
    extractedPath = joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
    logs = readParsedLogsFromHDFS(extractedPath)
    keywordDict = searchNProductLogsByKeywords(logs, keywords)
    trainingInstancesDict = trainingInstancesByKeywords(keywordDict)

def m16():
    keywords = get32Keywords()
    inputPath = joinPath(filteredLogsFromMayFolder, '2017-05-16_filtered')
    outputPath = joinPath(filteredLogsFromMayFolder, '2017-05-16_extractedLogs')
    saveExtractedLogsByKeywordsFromHDFS(inputPath, keywords, outputPath)

def printAct(day):
    keywords = 'iphone 7' # get32Keywords() # "BEKO 9 KG CAMASIR MAKINESI" # 'tupperware' # get5Keywords() # _file_old
    dateStr = '2017-05-' + str(day)
    extractedPath = joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
    extractedPath = joinPath(clickstreamFolder, 'part-r-00000_filtered_extracted_32_server')
    logs = readParsedLogsFromHDFS(extractedPath)
    keywordDict = searchNProductLogsByKeywords(logs, keywords)  
    #sessions = sessionize(keywordDict['iphone 7'])
    #printSessionActions(sessions[0])

def joinTests():
    searches = sc_().parallelize([{'p': 'a', 'l': [7, 2, 6]}, {'p': 'b', 'l': [7, 87, 65]}, {'p': 'c', 'l': [1, 65, 6]}, {'p': 'd', 'l': [7, 1, 6]}]) 
    products = sc_().parallelize([{'i': 1}, {'i': 2}, {'i': 7}, {'i': 65}, {'i': 87}, {'i': 999}])
    products2 = sc_().parallelize([{'i': 1}, {'i': 45}, {'i': 87}, {'i': 999}])
    searches = searches.flatMap(lambda p: [(i, p) for i in p['l']]).collect()#.map(lambda p: (p['l'], p)).flatMap(lambda p: (p, p)).distinct()
    for search in searches:
        print(search)

    #products = products.map(lambda p: (p['i'], p))
    #products2 = products2.map(lambda p: (p['i'], p))
    #print(products.join(products2).collect())

def runNewExtractionMethods():
    may17ExtractionTest(21)
    #joinTests()
    #printAct(16)