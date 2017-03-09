from LogProcesser.LogAnalyzer import *
from LogProcesser.LogOperator import *

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
    print counts[:5]
    keyword = counts[3][0]
    #for keyword,  c in counts:
    #    print keyword
    #    journey = getJourneyByKeyword(modules, keyword)
    #    #rintLogs(journey)
    #    printActions(journey)
    #printJourney(journey)
    #printActions(logs)
    printJourney(logs)

def extractAllTCJourneysTest(logs = None): # Running successfully
    extractAllTCJourneysStepByStep(entireDayRawLogsfolder2, entireDayParsedLogsFolder2) 

def mergeAllTCJourneysTest(logs = None): # Running successfully
    mergeAllTCJourneysFromPart(entireDayParsedLogsFolder2, '2016-09-28')

def newTest(logs = None): # Under development 
    #inputFile = joinPath(entireDayParsedLogsFolder1, '2016-09-27_All_TC_Journeys') # MemoryError on Dell
    inputFile = joinPath(joinPath(entireDayParsedLogsFolder1, 'TC_Journeys'), 'part-r-00000_TC_Journeys')
    logs = evalJson(inputFile)
    printActions(logs)
