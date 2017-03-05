from LogProcesser.LogAnalyzer import *
from LogFileHandler import *
from LogReader import *
from JsonIO import *
import LogFileHandler 
import LogReader 
import time

def getKeywords():
    keywords = []
    fileName = joinPath(testFolder, 'TcDominantKwyowrds.csv')
    f = open(fileName, 'rb')
    logs = f.readlines()
    # get number of columns
    for line in logs:
        array = line.split(',')
        keywords.append(array[0])
    print 'Keywords read'
    return keywords 

def extractAllTCJourneys(logs = None): # Under development, not working 
    logs = getAllLogs(logs) 
    modules = getModuleMap(logs)  
    keywords = getKeywords()
    #print keywords
    journey = getJourneyByKeyword(modules, keywords)
    #printJourney(journey)
    print journey

def parseSingleLogFile(rawFileName, parsedFileName):
    rawFileName = joinPath(allRawLogsfolder, rawFileName)
    parsedFileName = joinPath(allParsedLogsFolder, parsedFileName)
    generateParsedTestFile(rawFileName, parsedFileName)

def extractAllTCJourneysSeparately(rawFileName): 
    tic = time.time()
    rawFile = joinPath(allRawLogsfolder, rawFileName)
    logs = LogFileHandler.getLogs(None, rawFile)
    toc = time.time()
    print 'Reading and parsing', rawFileName, 'are done by', str(datetime.now())
    modules = getModuleMap(logs)  
    keywords = getKeywords()
    parsedFileFolder = joinPath(allParsedLogsFolder, rawFileName)
    if not os.path.exists(parsedFileFolder):
        os.mkdir(parsedFileName)
    for i, keyword in enumerate(keywords):
        tic = time.time()
        parsedFileName = joinPath(parsedFileFolder, rawFileName + ('_keyword%05d' % (i)))
        journey = getJourneyByKeyword(modules, keyword)
        writeToJson(journey, parsedFileName) 
        toc = time.time()
        print 'Writing the journey', keyword, 'took', toc - tic

def mergeAllTCJourneys(inputFolder): 
    outputFile = joinPath(joinPath(allParsedLogsFolder, 'TC_Journeys'), inputFolder + '_TC_Journeys')
    inputFolder = joinPath(allParsedLogsFolder, inputFolder)
    mergeAllParsedLogFiles(inputFolder, outputFile)

def extractAllTCJourneysFromPart(rawFileName): 
    extractAllTCJourneysSeparately(rawFileName)
    mergeAllTCJourneys(rawFileName)
    
def readAllTCJourneysFromPart(fileName): 
    fileName = joinPath(joinPath(allParsedLogsFolder, 'TC_Journeys'), fileName + '_TC_Journeys')
    logs = evalJson(fileName)
    printActions(logs)