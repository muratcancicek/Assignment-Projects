from LogProcesser.LogAnalyzer import *
from LogFileHandler import *
from LogReader import *
from JsonIO import *
import LogFileHandler 
import LogReader 

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

def extractAllTCJourneysSeparately(rawFileName, inputFolder, outputFolder, printAllSteps = False):
    rawFile = joinPath(inputFolder, rawFileName)
    logs = LogFileHandler.getLogs(None, rawFile)
    toc = time.time()
    print 'Reading and parsing', rawFileName, 'are done by', nowStr()
    modules = getModuleMap(logs)  
    keywords = getKeywords()
    parsedFileFolder = outputFolder
    for folder in ['TC_Journeys', 'parts']:
        parsedFileFolder = joinPath(parsedFileFolder, folder)
        if not os.path.exists(parsedFileFolder):
            os.mkdir(parsedFileFolder)
    for i, keyword in enumerate(keywords):
        tic = time.time()
        parsedFileName = joinPath(parsedFileFolder, rawFileName + ('_keyword%05d' % (i)))
        journey = getJourneyByKeyword(modules, keyword)
        output = i % 200 == 0 or printAllSteps
        writeToJson(journey, parsedFileName, printLog = output) 
        toc = time.time()
        if printAllSteps:
            print 'Writing the journey', keyword, 'took', toc - tic

def mergeAllTCJourneys(fileName, inputFolder, outputFolder): 
    outputFile = joinPath(joinPath(outputFolder, 'TC_Journeys'), fileName + '_TC_Journeys')
    inputFolder = joinPath(inputFolder, fileName)
    mergeAllParsedLogFiles(inputFolder, outputFile, False)

def extractAllTCJourneysFromPart(rawFileName): 
    extractAllTCJourneysSeparately(rawFileName)
    mergeAllTCJourneys(rawFileName)
    
def readAllTCJourneysFromPart(inputFolder, fileName): 
    fileName = joinPath(joinPath(inputFolder, 'TC_Journeys'), fileName + '_TC_Journeys')
    logs = evalJson(fileName)
    printActions(logs)

def extractAllTCJourneysStepByStep(folder): 
    for rawFileName in os.listdir(folder):
        if rawFileName in ['_SUCCESS']:
            continue        
        extractAllTCJourneysSeparately(rawFileName)
        mergeAllTCJourneys(rawFileName)
        print rawFileName, 'has been processed by %s.' % nowStr()

def mergeAllTCJourneysFromPart(inputFolder, fileName): 
    outputFile = joinPath(inputFolder, fileName)
    inputFolder = joinPath(inputFolder, 'TC_Journeys')
    mergeAllParsedLogFiles(inputFolder, outputFile)
    