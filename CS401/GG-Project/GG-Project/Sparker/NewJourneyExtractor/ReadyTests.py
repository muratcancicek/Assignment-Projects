from paths import *
from MainSrc.PythonVersionHandler import *
from Sparker.NewJourneyExtractor.BotFilter import *
from Sparker.NewJourneyExtractor.Sessionizer import *
from Sparker.NewJourneyExtractor.SearchExtractor import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from LogProcesser.scalaToPython.python_codes.StringUtil import *

def get32Keywords():
    keywords = open(joinPath(rankingFolder, 'keywords'), 'rb').readlines()
    keywords = [convertTrChars(keyword.decode("utf-8")).replace('\n', '').lower() for keyword in keywords]
    return keywords

def get5Keywords():
    return ['lg g4', 'samsung galaxy s6', 'galaxy s3', 'nike air max', 'tupperware']
            
def filteringTest():
    #fromPath = joinPath(may17Folder, '2017-05-16/part-r-00000')
    fromPath = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/searchlogs/2017-05-16'
    #fromPath = joinPath(clickstreamFolder, 'part-r-00000')joinPath(clickstreamFolder, 'part-r-00000_filtered')
    toPath = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/2017-05-16_filtered_wtc'
    filterSaveLogs(fromPath, toPath)
    
def hdfsTests(logs):
    #logs = logs.map(refererParserOnLog).filter(lambda log: 'page' in log[KEY_REFERER].keys())\
    #.map(lambda log: log[KEY_REFERER]['page']).distinct().foreach(print)
    #logs = logs.map(refererParserOnLog).filter(isProduct)\
    #.map(lambda log: log[KEY_REFERER]).distinct().foreach(print).foreach(print)[:-len(str([KEY_ID]))]
    logs = logs.map(refererParserOnLog).filter(lambda log: log[KEY_MODULE] == KEY_MODULE_CART)
    print(logs.count(), 'logs in total by', nowStr())
    logs = logs.filter(lambda log: str(log[KEY_ID]) in log[KEY_REFERER]['page'])
    print(logs.count(), 'logs in total by', nowStr())
    logs = logs.map(lambda log: log[KEY_REFERER])
    #print(total, 'logs in total by', nowStr())

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

def searchesExtractionTests(logs):
    if len(sys.argv) == 2:
        filteredPath = sys.argv[1]
    else:
        filteredPath = joinPath(clickstreamFolder, 'part-r-00000_filtered')
    logs = getLogs(None, filteredPath, False)
    keywordsTests(logs)
    #hdfsTests(logs)
    
def mergeAllParsedLogLines(inputFolder, outputFileName):
    f = open(outputFileName, 'w')
    inputFolderList = os.listdir(inputFolder)
    for i, fileName in enumerate(inputFolderList):
        if fileName == '_SUCCESS':
            continue
        fileName = joinPath(inputFolder, fileName)        
        part = open(fileName, 'r')
        for line in part:
                f.write(line) 
    f.close() 
    print_(outputFileName + ' has been written successfully.')

def mergingTest():
    extractedPath = joinPath(clickstreamFolder, 'part-r-00000_filtered_extracted_32_server')
    outputPath = joinPath(clickstreamFolder, 'part-r-00000_filtered_extracted_32_server_file')
    mergeAllParsedLogLines(extractedPath, outputPath)
    print_(outputPath, 'has', logs.count(), 'logs.')

def botTest():
    fromPath = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/searchlogs/2017-05-16'
    logs = readLogs(sc_(), fromPath, True)#
    total = logs.count()
    def b(l):
        i = l.find('_bot=')
        return l[i:i+6]
    logs = logs.filter(lambda l: '_bot=' in l).map(b).distinct()
    logs.foreach(print)
    filtered = logs.count()
    print(filtered, 'logs has been filtered from', total, 'logs in total by', nowStr())