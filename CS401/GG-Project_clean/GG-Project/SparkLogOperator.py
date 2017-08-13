from PythonVersionHandler import *
from SparkLogFileHandler import *
from SparkLogAnalyzer import *
from SparkLogReader import *
import SparkLogFileHandler 
from LogProcesser.JsonIO import *
import SparkLogReader as LogReader 

def getKeywords():
    keywords = []
    fileName = joinPath(testFolder, 'TcDominantKwyowrds.csv')
    f = open(fileName, 'rb')
    logs = f.readlines()
    # get number of columns
    for line in logs:
        array = str(line).split(',')
        keywords.append(array[0])
    print_('Keywords read')
    return keywords

def extractAllTCJourneys(logs = None): # Under development, not working 
    logs = getAllLogs(logs) 
    modules = getModuleMap(logs)  
    keywords = getKeywords()
    #print keywords
    journey = getJourneyByKeyword(modules, keywords)
    #printJourney(journey)
    print_(journey)

def parseSingleLogFile(rawFileName, parsedFileName):
    rawFileName = joinPath(allRawLogsfolder, rawFileName)
    parsedFileName = joinPath(allParsedLogsFolder, parsedFileName)
    generateParsedTestFile(rawFileName, parsedFileName)

def getPartsFolder(inputFolder): # Running, do not modify! 
    parsedFileFolder = inputFolder
    for folder in ['TC_Journeys', 'parts']:
        parsedFileFolder = joinPath(parsedFileFolder, folder)
        if not os.path.exists(parsedFileFolder):
            os.mkdir(parsedFileFolder)
    return parsedFileFolder

def extractAllTCJourneysSeparately(rawFileName, inputFolder, outputFolder, printAllSteps = False): # Running, do not modify! 
    rawFile = joinPath(inputFolder, rawFileName)
    logs = SparkLogFileHandler.getLogs(None, rawFile)
    toc = time.time()
    print_('Reading and parsing', rawFileName, 'are done by', nowStr())
    modules = getModuleMap(logs)  
    keywords = getKeywords()
    parsedFileFolder = getPartsFolder(outputFolder)
    parsedFileFolder = joinPath(parsedFileFolder, rawFileName)
    if not os.path.exists(parsedFileFolder):
        os.mkdir(parsedFileFolder)
    for i, keyword in enumerate(keywords):
        tic = time.time()
        parsedFileName = joinPath(parsedFileFolder, rawFileName + ('_keyword%05d' % (i)))
        journey = getJourneyByKeyword(modules, keyword)
        output = i % 200 == 0 or printAllSteps
        #writeToJson(journey, parsedFileName, printLog = output) 
        journey.saveAsTextFile(parsedFileName)
        toc = time.time()
        if printAllSteps:
            print_('Writing the journey', keyword, 'took', toc - tic)

def mergeAllTCJourneys(fileName, inputFolder, outputFolder):  # Running, do not modify! 
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

def extractAllTCJourneysStepByStep(folder, outputFolder): # Running, do not modify! , 'part-r-00000', 'part-r-00001'
    for rawFileName in os.listdir(folder):
        if rawFileName in ['_SUCCESS']:
            continue        
        extractAllTCJourneysSeparately(rawFileName, folder, outputFolder)
        partsFolder = getPartsFolder(outputFolder)
        mergeAllTCJourneys(rawFileName, partsFolder, outputFolder)
        print_(rawFileName, 'has been processed by %s.' % nowStr())

def mergeAllTCJourneysFromPart(inputFolder, fileName): 
    outputFile = joinPath(inputFolder, fileName + '_All_TC_Journeys')
    inputFolder = joinPath(inputFolder, 'TC_Journeys')
    mergeAllParsedLogLines(inputFolder, outputFile)