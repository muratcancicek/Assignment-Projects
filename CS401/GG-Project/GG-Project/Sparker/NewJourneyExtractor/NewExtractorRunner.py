from paths import *
from MainSrc.PythonVersionHandler import *
from Sparker.NewJourneyExtractor.BotFilter import *
from Sparker.NewJourneyExtractor.Sessionizer import *
from Sparker.NewJourneyExtractor.SearchExtractor import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from LogProcesser.scalaToPython.python_codes.StringUtil import *

def filteringTest():
    #fromPath = joinPath(may17Folder, '2017-05-16/part-r-00000')
    fromPath = 'hdfs://osldevptst02.host.gittigidiyor.net:8020/user/root/searchlogs/2017-05-16/part-r-00000.gz'
    #fromPath = joinPath(clickstreamFolder, 'part-r-00000')
    toPath = joinPath(clickstreamFolder, 'part-r-00000_filtered')
    filterSaveLogs(fromPath, toPath)

def get32Keywords():
    keywords = open(joinPath(rankingFolder, 'keywords'), 'rb').readlines()
    keywords = [convertTrChars(keyword.decode("utf-8")).replace('\n', '').lower() for keyword in keywords]
    return keywords

def get5Keywords():
    return ['lg g4', 'samsung galaxy s6', 'galaxy s3', 'nike air max', 'tupperware']

def testExtractingLogsByKeywords(logs, keywords):
    keywordDict = searchNProductLogsByKeywords(logs, keywords)
    for keyword, (searches, productLogs) in keywordDict.items():
        print(keyword, searches.count(), productLogs.count())

def readClickstreamFromHDFS():
    fromPath = sys.argv[1]
    logs = readLogs(sc_(), fromPath, True)#
    total = logs.count()
    logs = logs.filter(isRelevant)
    filtered = logs.count()
    print(filtered, 'logs has been filtered from', total, 'logs in total by', nowStr())
    return parseAllLogs(logs)

def keywordsTests(logs):
    keywords = 'tupperware'#get32Keywords()
    keywordDict = searchNProductLogsByKeywords(logs, keywords)
    print(keywordDict)
    for v in keywordDict:
        print(v)
        sessions = sessionize(keywordDict[v])
        for s in sessions:
            printActions(s)
            
def hdfsTests(logs):
    total = logs.count()
    print( total, 'logs in total by', nowStr())

def runNewExtractionMethods():
    if len(sys.argv) == 2:
        logs = readClickstreamFromHDFS()
        hdfsTests(logs)
    else:
        filteredPath = joinPath(clickstreamFolder, 'part-r-00000_filtered')
        logs = getLogs(None, filteredPath, False)
        keywordsTests(logs)
    #filteringTest()