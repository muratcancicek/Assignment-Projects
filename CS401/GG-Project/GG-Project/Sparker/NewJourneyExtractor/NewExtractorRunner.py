from paths import *
from MainSrc.PythonVersionHandler import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from LogProcesser.scalaToPython.python_codes.StringUtil import *
from Sparker.NewJourneyExtractor.BotFilter import *

def filteringTest():
    #fromPath = joinPath(may17Folder, '2017-05-16/part-r-00000')
    fromPath = 'hdfs://osldevptst02.host.gittigidiyor.net:8888/user/root/searchlogs/2017-05-16/part-r-00000.gz'
    #fromPath = joinPath(clickstreamFolder, 'part-r-00000')
    toPath = joinPath(clickstreamFolder, 'part-r-00000_filtered')
    filterSaveLogs(fromPath, toPath)
    

def get32Keywords():
    keywords = open(joinPath(rankingFolder, 'keywords'), 'rb').readlines()
    keywords = [convertTrChars(keyword.decode("utf-8")).replace('\n', '').lower() for keyword in keywords]
    return keywords

def get5Keywords():
    return ['lg g4', 'samsung galaxy s6', 'galaxy s3', 'nike air max', 'tupperware']

def findExistingSearchKeywords(filteredPath):
    logs = getLogs(None, filteredPath, False)
    logs = logs.filter(lambda log: log[KEY_MODULE] == KEY_MODULE_SEARCH and KEY_KEYWORD in log.keys())
    keywords32 = get32Keywords()
    logs = logs.filter(lambda log: log[KEY_KEYWORD].lower() in keywords32)
    logs = logs.map(lambda log: log[KEY_KEYWORD])
    keywords = logs.distinct()
    print(keywords.count(), 'keywords has been found in data by', nowStr())
    return keywords.collect()

def keywordsTests():
    filteredPath = joinPath(clickstreamFolder, 'part-r-00000_filtered')
    logs = getLogs(None, filteredPath, False)
    searches = logs.filter(lambda log: log[KEY_MODULE] == KEY_MODULE_SEARCH and KEY_KEYWORD in log.keys())
    keywords5 = get5Keywords()
    searches = searches.filter(lambda log: log[KEY_KEYWORD].lower() in keywords5)
    #print(searches.count(), 'logs has been found in data by', nowStr())
    cookies = searches.map(lambda log: log[KEY_PERSISTENT_COOKIE]).distinct()
    #group = logs.cogroup(

def runNewExtractionMethods():
    filteringTest()
    #keywordsTests()
    