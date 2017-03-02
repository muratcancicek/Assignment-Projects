import scalaToPython.python_codes.LumberjackParser as LumberjackParser
import LogAnalyzer as LA
from JsonIO import *
from paths import * 
import datetime
import Actions
import math

WRITING_ALLOWED = False

def readLogs(fileName, duplicated = False):
    f = open(fileName, 'r')
    logs = f.read().split('\n') if duplicated else list(set(f.read().split('\n'))) 
    f.close() 
    print fileName + ' has been read successfully.'
    return logs

def readAllLogFiles(folder):
    logs = [] 
    for filename in os.listdir(folder):
        if filename == '_SUCCESS':
            continue
        filename = joinPath(folder, filename)
        logs.extend(readLogs(filename))
    print 'All logs have been read successfully.'
    return logs

def convertPossibleType(value):
    if isinstance(value, list):
        return map(convertPossibleType, value)
    try:
        value = float(value)
    except ValueError:
        return value
    if math.isinf(value) and value > 0:
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
    
def sortedLogs(logs, key = 'timestamp'):
    #logs.sort(key = lambda log: log[key])  
    logs = sorted(logs, key = lambda log: (log['_c'] if '_c' in log.keys() else '000', log[key]))
    return logs  

def printJourney(logs, printActions = True, printLogs = True, orderedKeys = None, colorMap = {}, group = True):
    if group:
        groupedLogs = LA.groupLogsByCookie(logs)
        for journey in groupedLogs:
            printJourney(journey, printActions, printLogs, orderedKeys, colorMap, group = False)
        return
    print green('Journey begins...')
    logs = sortedLogs(logs)    
    for i, log in enumerate(logs):
        if 'module' in log.keys():
            color = None
            if log['module'] in ['cart', 'payment']:
                color = blue
            elif log['module'] == 'item':
                color = pink
            elif log['module'] == 'newsession':
                color = green
            elif not log['module'] in ['newsession', 'search', 'item' 'cart', 'payment']:
                color = darkCyan
            if printActions:
                Actions.printAction(i, logs, color, not printLogs)
            if printLogs:
                #print logToStr(log, orderedKeys, colorMap, color)
                print logToStr(log, orderedKeys, colorMap, color)
    print green('Journey end.')

def printLogs(logs, orderedKeys = None, colorMap = {}, group = True):
    printJourney(logs, printActions = False, group = group)

def printActions(logs, orderedKeys = None, colorMap = {}, group = True):
    printJourney(logs, printLogs = False, group = group)