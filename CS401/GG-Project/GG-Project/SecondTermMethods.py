from paths import clickstreamFolder 
import scalaToPython.python_codes.LumberjackParser as LumberjackParser

def readClickstreamData(fileName = clickstreamFolder + 'part-r-00000'):
    f = open(fileName, 'rb')
    logs = f.readlines()
    f.close() 
    return logs

def parseLog(log):
    return LumberjackParser.parse(log)

def run():
    logs = readClickstreamData()
    log = logs[0]
    print log
    map = parseLog(log)
    print map
    print '\n', map['title']