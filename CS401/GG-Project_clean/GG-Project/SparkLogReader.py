WRITING_ALLOWED = False
def readLogs(_sc, fileName, duplicated = False):
    logs = _sc.textFile(fileName) if duplicated else _sc.textFile(fileName).distinct()
    import PythonVersionHandler
    PythonVersionHandler.print_(fileName + ' will be reading by', PythonVersionHandler.nowStr())
    return logs

def readAllLogFiles(_sc, folder):
    import os
    logs = _sc.emptyRDD()
    for filename in os.listdir(folder):
        if filename == '_SUCCESS' or filename[-4:] == '.crc':
            continue
        import paths, SparkLogReader
        filename = paths.joinPath(folder, filename)
        logs = logs.union(SparkLogReader.readLogs(_sc, filename))
    import PythonVersionHandler
    PythonVersionHandler.print_('All logs have been read successfully.')
    return logs

def convertPossibleType(value):
    if isinstance(value, list):
        return [convertPossibleType(v) for v in value]
    try:
        value = float(value)
    except ValueError:
        return value
    import math
    if math.isinf(value) and value > 0:
        return value
    try:
        return value if value - int(value) > 0 else int(value)
    except ValueError:
        return 0

parseCounter = 0
def parseLog(log):
    import LumberjackParser
    log = LumberjackParser.parse(log)
    if 'ids' in log.keys():
            if '%2C' in log['ids']:
                log['ids'] = log['ids'].split('%2C')
            else:
                log['ids'] = [log['ids']]
    for key, value in log.items():            
        log[key] = convertPossibleType(value)
    if 'timestamp' in log.keys():
        import datetime
        log["time"] = str(datetime.datetime.fromtimestamp(int(log["timestamp"])/ 1e3))
    global parseCounter
    parseCounter += 1
    #if parseCounter % 1000000 == 0: 
    #    print_('%i logs have been parsed by %s' % (parseCounter, PythonVersionHandler.nowStr()))
    return log

def parseAllLogs(logs):
    logs = logs.map(parseLog)
    return logs

def readParseLogs(_sc, fileName):
    logs = readLogs(_sc, fileName)
    return parseAllLogs(logs)

def readParsedLogs(fileName):
    import SparkLogFileHandler
    return SparkLogFileHandler.sc_().parallelize(evalJson(fileName[:-5]))


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
    import PythonVersionHandler
    PythonVersionHandler.print_(logToStr(log, orderedKeys, colorMap, logColor))
    
def sortedLogs(logs, key = 'timestamp', ascending = False):
    sorter = lambda log: (log['_c'] if '_c' in list(log.keys()) else '000', log[key])
    if isinstance(logs, list):
        return sorted(logs, key = sorter)
    return logs.sortBy(sorter, ascending = ascending)

def printJourney(logs, printActions = True, printLogs = True, orderedKeys = None, colorMap = {}, group = True):
    if group:
        import SparkLogAnalyzer
        groupedLogs = SparkLogAnalyzer.groupLogsByCookie(logs)
        for journey in groupedLogs:
            printJourney(journey, printActions, printLogs, orderedKeys, colorMap, group = False)
        return
    if not isinstance(logs, list):
        logs = logs.collect()
    import PythonVersionHandler
    PythonVersionHandler.print_(green('Journey begins...'))
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
                import ActionsWithSpark
                ActionsWithSpark.printAction(i, logs, color, not printLogs)
            if printLogs:
                #print_(logToStr(log, orderedKeys, colorMap, color))
                PythonVersionHandler.print_(logToStr(log, orderedKeys, colorMap, color)) 
    PythonVersionHandler.print_(green('Journey end.'))

def printLogs(logs, orderedKeys = None, colorMap = {}, group = True):
    printJourney(logs, printActions = False, group = group)

def printActions(logs, orderedKeys = None, colorMap = {}, group = True):
    printJourney(logs, printLogs = False, group = group)
    
def printSession(logs, printActions = True, printLogs = True, orderedKeys = None, colorMap = {}):
    logs = logs.sortBy(lambda log: log['timestamp'])
    if not isinstance(logs, list):
        logs = logs.collect()
    import PythonVersionHandler, Printing
    PythonVersionHandler.print_(Printing.green('Session begins...'))
    for i, log in enumerate(logs):
        if 'module' in log.keys():
            color = None
            if log['module'] in ['cart', 'payment']:
                color = Printing.blue
            elif log['module'] == 'item':
                color = Printing.pink
            elif log['module'] == 'newsession':
                color = Printing.green
            elif not log['module'] in ['newsession', 'search', 'item' 'cart', 'payment']:
                color = Printing.darkCyan
            if printActions:
                import ActionsWithSpark
                ActionsWithSpark.printAction(i, logs, color, not printLogs)
            if printLogs:
                #print_(logToStr(log, orderedKeys, colorMap, color))
                PythonVersionHandler.print_(logToStr(log, orderedKeys, colorMap, color))
    PythonVersionHandler.print_(Printing.green('Session end.'))

def printSessionLogs(logs, orderedKeys = None, colorMap = {}):
    printSession(logs, printActions = False)

def printSessionActions(logs, orderedKeys = None, colorMap = {}):
    printSession(logs, printLogs = False)
    
def writeRDDToJson(rdd, fileName,  printing = False): 
    f = open(fileName + '.json', 'w')
    rddString = json.dumps(rdd.collect())
    f.write(rddString) 
    if printLog:
        import PythonVersionHandler
        PythonVersionHandler.print_(fileName + '.json has been written successfully.')
    f.close() 