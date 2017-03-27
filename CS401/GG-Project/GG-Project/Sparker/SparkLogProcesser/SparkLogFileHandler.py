from MainSrc.PythonVersionHandler import *
from LogProcesser.OutputLogger import OutputLogger
from paths import *
from LogProcesser.JsonIO import *
from . import SparkLogReader as LogReader

TEST_LOGS_FILE = 'part-r-00000'
TEST_LOGS_FILE_ORINAL = 'part-r-00000_original'
TEST_LOGS = joinPath(clickstreamFolder, TEST_LOGS_FILE)
testFolder = joinPath(logInfoFolder, 'part-r-00000')

def saveOutput():
    outputFileName = joinPath(outputFolder, outputFileName)
    sys.stdout = open(outputFileName, 'w')

def setTestFile(testFile):
    global TEST_LOGS_FILE, TEST_LOGS, testFolder
    TEST_LOGS_FILE = testFile
    TEST_LOGS = joinPath(clickstreamFolder, TEST_LOGS_FILE)
    #testFolder = joinPath(logInfoFolder, TEST_LOGS_FILE)
    
#saveOutput()
#setTestFile(TEST_LOGS_FILE_ORINAL) 
#setTestFile('part-r-00000_iphone_6') 

_sc = None
def setSparkContext(scInstance):
   global _sc
   _sc = scInstance

def sc_():
    return _sc

sys.stdout = OutputLogger(testFolder) 

lastReadLogs = None
def getAllLogs(logs = None, folder = allRawLogsfolder):
    global lastReadLogs
    if logs == None:
        if lastReadLogs != None and folder == allRawLogsfolder:
            return lastReadLogs
        else:
            logs = LogReader.readAllLogFiles(folder)
            logs = LogReader.parseAllLogs(logs)
            return logs 
    else:
        return logs
    return logs

def getLogs(logs = None, fromFileName = TEST_LOGS):
    global lastReadLogs
    if logs == None:
        if lastReadLogs != None and fromFileName == TEST_LOGS:
            return lastReadLogs
        else:
            logs = LogReader.getLogs(_sc, fromFileName)
            logs2 = []
            def botFilter(log):
                return '_bot' in log.keys() and log['_bot'] == 0
            return logs.filter(botFilter)
    else:
        return logs

def mergeAllParsedLogFiles(inputFolder, outputFileName, printing = True):  # Running, do not modify! 
    logs = sc_().emptyRDD()
    for i, filename in enumerate(os.listdir(inputFolder)):
        #if filename[-5:] != '.json':
        #    continue[:-5]
        filename = joinPath(inputFolder, filename)
        printing1 = printing or i % 200 == 0
        logs.union(LogReader.readAllLogFiles(sc_(), filename))
    writeToJson(logs, outputFileName)
    return logs

def mergeAllParsedLogLines(inputFolder, outputFileName, printing = True):
    f = open(outputFileName + '.json', 'w')
    f.write('[\n') 
    inputFolderList = os.listdir(inputFolder)
    last = len(inputFolderList) - 1
    for i, fileName in enumerate(inputFolderList):
        if fileName[-5:] != '.json':
            continue
        fileName = joinPath(inputFolder, fileName)        
        part = open(fileName, 'r')
        for line in part:
            if not line[0] in ['[', ']']:
                if line[-2] != ',' and i != last:
                    line = line[:-1] + ',\n'
                f.write(line) 
        printing1 = printing or i % 200 == 0
        if printing:
            print_(fileName + '.json has been appended successfully.')
    f.write(']') 
    f.close() 
    print_(outputFileName + '.json has been written successfully.')