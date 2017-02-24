import scalaToPython.python_codes.LumberjackParser as LumberjackParser
from JsonIO import *
from paths import * 
import datetime
import Actions

WRITING_ALLOWED = True

def readLogs(fileName, duplicated = False):
    print fileName + ' has been read successfully.'
    f = open(fileName, 'rb')
    logs = f.readlines() if duplicated else list(set(f.readlines())) 
    f.close() 
    return logs

def convertPossibleType(value):
    if isinstance(value, list):
        return map(convertPossibleType, value)
    try:
        value = float(value)
    except ValueError:
        return value
    return value if value - int(value) > 0 else int(value)

def parseLog(log):
    log = LumberjackParser.parse(log)
    if 'ids' in log.keys():
            if '%2C' in log['ids']:
                log['ids'] = log['ids'].split('%2C')
            else:
                log['ids'] = [log['ids']]
    for key, value in log.items():            
       log[key] = convertPossibleType(value)
    if 'timestamp' in log.keys():
        log["time"] = str(datetime.datetime.fromtimestamp(int(log["timestamp"])/ 1e3))
    return log

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

def logToStr(log, orderedKeys = None, colorMap = {}, logColor = None):
    firstKeys = ['time', 'module', 'keyword', 'id', 'orderBy', 'pageNum', '_c', 'ids', 'title']
    if orderedKeys == None:
        orderedKeys = firstKeys
    elif isinstance(orderedKeys, str):
        orderedKeys = firstKeys + [orderedKeys]
    else:
        for key in firstKeys:
            if key in orderedKeys:
                orderedKeys.remove(key)
        orderedKeys = firstKeys + orderedKeys 
    line = '{ '
    keys = log.keys()
    for key in orderedKeys:
        if key in keys:
            keys.remove(key)
            pair = str(key) + ': ' + str(log[key]) + ', '
            if key in ['time', 'module']:
                pair = str(log[key]) + ', '
            if key in colorMap.keys():
                pair = colorMap[key](pair)
            line += pair
    keys.sort()
    for key in keys:
        pair = str(key) + ': ' + str(log[key]) + ', '
        if key in colorMap.keys():
            pair = colorMap[key](pair) 
        line += pair
    line = line[:-2] + '}'
    if logColor != None:
        line = logColor(line)
    return line

def printLog(log, orderedKeys = None, colorMap = {}, logColor = None):
    print logToStr(log, orderedKeys, colorMap, logColor)

def printJourney(logs, printActions = True, orderedKeys = None, colorMap = {}):
    print 'Journey begins...'
    logs.sort(key = lambda log: log['timestamp'])    
    for i, log in enumerate(logs):
        if 'module' in log.keys():
            if printActions:
                    Actions.printAction(i, logs)
            if log['module'] in ['cart', 'payment']:
                print logToStr(log, orderedKeys, colorMap, blue)
            elif log['module'] == 'item':
                print logToStr(log, orderedKeys, colorMap, pink)
            elif log['module'] == 'newsession':
                print logToStr(log, orderedKeys, colorMap, green)
            elif not log['module'] in ['newsession', 'search', 'item' 'cart', 'payment']:
                print logToStr(log, orderedKeys, colorMap, darkCyan)
            else:
                print logToStr(log, orderedKeys, colorMap)
    print 'Journey end.'