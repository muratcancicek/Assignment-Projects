import LogProcesser.scalaToPython.python_codes.LumberjackParser as LumberjackParser
from MainSrc.PythonVersionHandler import *
from LogProcesser.JsonIO import *
from . import ActionsWithSpark as Actions
from Sparker.PySparkImports import *
from . import SparkLogAnalyzer as LA
from paths import * 
import datetime
import math
import time

WRITING_ALLOWED = False
def readLogs(_sc, fileName, duplicated = False):
    logs = _sc.textFile(fileName) if duplicated else _sc.textFile(fileName).distinct()
    print_(fileName + ' has been read successfully.')
    return logs

def readAllLogFiles(_sc, folder):
    logs = _sc.emptyRDD()
    for filename in os.listdir(folder):
        if filename == '_SUCCESS' or filename[-4:] == '.crc':
            continue
        filename = joinPath(folder, filename)
        logs = logs.union(readLogs(_sc, filename))
    print_('All logs have been read successfully.')
    return logs

def convertPossibleType(value):
    if isinstance(value, list):
        return [convertPossibleType(v) for v in value]
    try:
        value = float(value)
    except ValueError:
        return value
    if math.isinf(value) and value > 0:
        return value
    return value if value - int(value) > 0 else int(value)

parseCounter = 0
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
    global parseCounter
    parseCounter += 1
    if parseCounter % 10000 == 0: 
        print_('%i logs have been parsed by %s' % (parseCounter, nowStr()))
    return log

def parseAllLogs(logs):
    logs = logs.map(parseLog)
    #print_('All logs have been parsed on ', nowStr())
    return logs

def readParseLogs(_sc, fileName):
    logs = readLogs(_sc, fileName)
    return parseAllLogs(logs)

def generateParsedLogs(_sc, fromFileName, toFileName): # for development only 
    logs = readParseLogs(fromFileName)
    writeToJson(logs.collect(), toFileName) 

def readParsedLogs(fileName):
    #fileName = fileName.split(os.path.sep)[-1]
    #fileName = joinPath(joinPath(logInfoFolder, fileName), fileName + '.json')
    #if os.path.exists(fileName):
        return LA.sc_().parallelize(evalJson(fileName[:-5]))

def readParsedLogsFromTextFile(_sc, folder):
    return readAllLogFiles(_sc, folder)

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
            
def getLogs(_sc, fileName):   
    if WRITING_ALLOWED:
        return getLogsFromLocal(fileName)
    else:
        return readParseLogs(_sc, fileName)   

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
    keys = list(log.keys())
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
    print_(logToStr(log, orderedKeys, colorMap, logColor))
    
def sortedLogs(logs, key = 'timestamp', ascending = False):
    sorter = lambda log: (log['_c'] if '_c' in list(log.keys()) else '000', log[key])
    if isinstance(logs, list):
        return sorted(logs, key = sorter)
    return logs.sortBy(sorter, ascending = ascending)

def printJourney(logs, printActions = True, printLogs = True, orderedKeys = None, colorMap = {}, group = True):
    if group:
        groupedLogs = LA.groupLogsByCookie(logs)
        for journey in groupedLogs:
            printJourney(journey, printActions, printLogs, orderedKeys, colorMap, group = False)
        return
    if isinstance(logs, PipelinedRDD):
        logs = logs.collect()
    print_(green('Journey begins...'))
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
                #print_(logToStr(log, orderedKeys, colorMap, color))
                print_(logToStr(log, orderedKeys, colorMap, color)) 
    print_(green('Journey end.'))

def printLogs(logs, orderedKeys = None, colorMap = {}, group = True):
    printJourney(logs, printActions = False, group = group)

def printActions(logs, orderedKeys = None, colorMap = {}, group = True):
    printJourney(logs, printLogs = False, group = group)

    
def writeRDDToJson(rdd, fileName,  printing = False): 
    f = open(fileName + '.json', 'w')
    rddString = json.dumps(rdd.collect())
    f.write(rddString) 
    if printLog:
        print_(fileName + '.json has been written successfully.')
    f.close() 