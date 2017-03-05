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

def newTest(logs = None): # Under development 
    readAllTCJourneysFromPart('part-r-00000')
    readAllTCJourneysFromPart('part-r-00001')
    #extractAllTCJourneysFromPart('part-r-00001')
    #parseSingleLogFile('part-r-00000', 'part-r-00000')
    #parseSingleLogFile('part-r-00001', 'part-r-00001')
    #parseSingleLogFile('part-r-00002', 'part-r-00002')