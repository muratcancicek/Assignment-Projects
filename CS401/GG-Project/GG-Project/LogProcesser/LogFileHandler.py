from OutputLogger import OutputLogger
from paths import *
from JsonIO import *
import LogReader 

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
setTestFile(TEST_LOGS_FILE_ORINAL) 
#setTestFile('part-r-00000_iphone_6') 

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
            logs = LogReader.getLogs(fromFileName)
            logs2 = []
            for log in logs:
                if '_bot' in log.keys() and log['_bot'] == 0:
                    logs2.append(log)
            return logs2 
    else:
        return logs

def mergeAllParsedLogFiles(inputFolder, outputFileName):
    logs = [] 
    for filename in os.listdir(inputFolder):
        if filename[-5:] != '.json':
            continue
        filename = joinPath(inputFolder, filename[:-5])
        logs.extend(evalJson(filename))
    writeToJson(logs, outputFileName)
    return logs
