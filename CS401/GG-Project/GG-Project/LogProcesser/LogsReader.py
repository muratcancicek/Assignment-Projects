import scalaToPython.python_codes.LumberjackParser as LumberjackParser
from paths import * 
from JsonIO import *

WRITING_ALLOWED = False

def readLogs(fileName, duplicated = False):
    print fileName + '.json has been read successfully.'
    f = open(fileName, 'rb')
    logs = f.readlines() if duplicated else list(set(f.readlines())) 
    f.close() 
    return logs

def parseLog(log):
    return LumberjackParser.parse(log)

def parseAllLogs(logs):
    return map(parseLog, logs)

def readParseLogs_Head(fileName, n):
    logs = readLogs(fileName)
    length = len(logs)
    n = n if n < length else length
    return parseAllLogs(logs[:n])

def readParseLogs(fileName):
    logs = readLogs(fileName)
    return parseAllLogs(logs)

def generateParsedLogs(fromFileName, toFileName): # for development only 
    logs = readParseLogs(fromFileName)
    writeToJson(logs, toFileName) 

def readParsedLogs(fileName):
    fileName = fileName.split(os.path.sep)[-1]
    fileName = joinPath(joinPath(logInfoFolder, fileName), fileName + '.json')
    if os.path.exists(fileName):
        return evalJson(fileName[:-5])
    else:
        return []

def getLogsFromLocal(fileName):
    logs = readParsedLogs(fileName)
    if logs == []:
        return readParseLogs(fileName)
    else:
        return logs
        
def getLogs_Head(fileName, n):
    if WRITING_ALLOWED:
        return getLogsFromLocal(fileName)[:n]
    else:
        return readParseLogs_Head(fileName, n)   
            
def getLogs(fileName):   
    if WRITING_ALLOWED:
        return getLogsFromLocal(fileName)
    else:
        return readParseLogs(fileName)   