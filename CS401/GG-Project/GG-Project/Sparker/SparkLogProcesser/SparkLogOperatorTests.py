from MainSrc.PythonVersionHandler import *
from .SparkLogAnalyzer import *
from .SparkLogOperator import *
from paths import *
#[(None, 1619), ('erkek kol saati', 336), ('nike air max', 204), ('iphone 6', 186), ('hali', 180)]
def extractPopularKeywordsTest(logs = None): # Under development 
    logs = getLogs(logs) 
    modules = getModuleMap(logs)   
    keywords = getLogsColumnAsList('keyword', modules['search'])
    counts = []
    for key in unique(keywords):
        counts.append((key, keywords.count(key)))
    counts.sort(key=lambda x: x[1], reverse=True)
    counts = counts[1:6]
    print_(counts[:5])
    keyword = counts[3][0]
    #for keyword,  c in counts:
    #    print keyword
    #    journey = getJourneyByKeyword(modules, keyword)
    #    #rintLogs(journey)
    #    printActions(journey)
    #printJourney(journey)
    #printActions(logs)
    printJourney(logs)
    
def writeRDDToJsonTest(logs = None): # Running successfully
    #writeToJson(logs.top(100).collect(), 'SparkTop100Logs', entireDaySparkParsedLogsFolder1) .top(100)
    writeRDDToJson(logs, joinPath(entireDaySparkParsedLogsFolder1, 'SparkTop100Logs'))
    logs.saveAsTextFile(joinPath(entireDaySparkParsedLogsFolder1, 'SparkTop100Logs'))
    
def readTextFileTest(logs = None): # Running successfully
    print_(logs.count())
    logs2 = readParsedLogsFromTextFile(sc(), joinPath(entireDaySparkParsedLogsFolder1, 'SparkTop100Logs'))
    print_(logs2.count())

def extractAllTCJourneysTest(): # Running successfully
    extractAllTCJourneysStepByStep(entireDayRawLogsfolder1, entireDaySparkParsedLogsFolder1) 

def mergeAllTCJourneysTest(): # Running successfully
    mergeAllTCJourneysFromPart(entireDaySparkParsedLogsFolder2, '2016-09-28')

def newTest(): # Under development 
    #inputFile = joinPath(entireDayParsedLogsFolder1, '2016-09-27_All_TC_Journeys') # MemoryError on Dell
    inputFile = joinPath(joinPath(entireDaySparkParsedLogsFolder1, 'TC_Journeys'), 'part-r-00000_TC_Journeys')
    logs = evalJson(inputFile)
    printActions(logs)
