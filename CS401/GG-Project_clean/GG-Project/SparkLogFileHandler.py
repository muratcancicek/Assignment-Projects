_sc = None
def setSparkContext(scInstance):
   global _sc
   _sc = scInstance

def sc_():
    return _sc

def fixKeywords(logText):
    while(True):
        j = logText.find("L, u'")
        k = logText.find("L, '")
        if j == -1 and k == -1: break
        b = (j if j > -1 and j < k or k == -1 else k)+1
        i = logText[:b].rfind('\': ') + 3
        logText = logText[:i]+'u\''+logText[i:b]+'\''+logText[b:]
    return logText

evalCounter = 0
def evalLog(logText):
    try:
        log = eval(logText)
    except SyntaxError:
        log = eval(fixKeywords(logText))
    global evalCounter 
    evalCounter += 1
    #if evalCounter % 100000 == 0: 
    #    print_('%i logs have been evaluated to Python Dict by %s' % (evalCounter, nowStr()))
    return log

def readParsedLogsFromHDFS(fileName): 
    logs = sc_().textFile(fileName)
    global evalCounter 
    evalCounter = 0
    logs = logs.map(evalLog)
    import PythonVersionHandler
    PythonVersionHandler.print_(fileName, 'has been read by', nowStr())
    return logs

def saveRDDToHDFS(rdd, fileName):
    rdd.saveAsTextFile(fileName)
    import PythonVersionHandler
    PythonVersionHandler.print_(fileName, 'with', rdd.count(), 'lines has been saved successfully by', nowStr())