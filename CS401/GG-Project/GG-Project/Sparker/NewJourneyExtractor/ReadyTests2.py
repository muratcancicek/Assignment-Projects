from paths import *
from MainSrc.PythonVersionHandler import *
from Sparker.NewJourneyExtractor.BotFilter import *
from Sparker.NewJourneyExtractor.Sessionizer import *
from Sparker.NewJourneyExtractor.ReadyTests import *
from Sparker.NewJourneyExtractor.SearchExtractor import *
from Sparker.NewJourneyExtractor.NewProductPreferrer import *
from Sparker.SparkLogProcesser.SparkLogReader import *
from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from LogProcesser.scalaToPython.python_codes.StringUtil import *

def keywordsSessionizingTest(keywordDict):
    for v in keywordDict:
        #print(keywordDict[v][0].count(), 'searches and', keywordDict[v][1].count(), 
        #      'product logs have been found for', v, 'by', nowStr())
        sessions = sessionize(keywordDict[v])
        global WRITE_OUTPUTS
        WRITE_OUTPUTS = False
        for s in sessions:
            printSessionActions(s)
        WRITE_OUTPUTS = True
        
def keywordsSavingTest(keywordDict):
    objectiveLogs = sc_().parallelize([])
    for v in keywordDict:
        (searches, viewedProductLogs, cartedOrPaidProductLogs) = keywordDict[v]
        objectiveLogs = objectiveLogs.union(searches).union(viewedProductLogs).union(cartedOrPaidProductLogs)
    if COMPUTERNAME == 'osldevptst02' :
        toPath = joinPath(clickstreamFolder, 'part-r-00000_filtered_extracted_' + str(len(keywordDict.keys())) + '_server')
    else:
        toPath = joinPath(clickstreamFolder, 'part-r-00000_filtered_extracted_' + str(len(keywordDict.keys())) + '_local')
    objectiveLogs = objectiveLogs.coalesce(24)
    saveRDDToHDFS(objectiveLogs, toPath)

def keywordsTests(logs):
    keywords = get32Keywords() # 'tupperware' # get5Keywords() # 
    keywordDict = searchNProductLogsByKeywords(logs, keywords)
    keywordsSessionizingTest(keywordDict)
    keywordsSavingTest(keywordDict)
    
def wtcTest():
    fromPath = 'hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/2017-05-16_filtered_wtc'
    logs = readLogs(sc_(), fromPath, True)
    logs = parseAllLogs(logs)
    keywordsTests(logs)

def oldTest():
    extractedPath = joinPath(clickstreamFolder, 'part-r-00000_filtered_extracted_32_server_file_old')
    logs = readParsedLogsFromHDFS(extractedPath)
    keywordsTests(logs)
    #botTest()
    #filteringTest()

def preferrerTest():
    extractedPath = joinPath(clickstreamFolder, 'part-r-00000_filtered_extracted_32_server')
    keywords = get32Keywords() # "BEKO 9 KG CAMASIR MAKINESI" # 'iphone 7' # 'tupperware' # get5Keywords() # _file_old
    logs = readParsedLogsFromHDFS(extractedPath)
    keywordDict = searchNProductLogsByKeywords(logs, keywords)
    trainingInstancesDict = trainingInstancesByKeywords(keywordDict)

def outputsTest():
    outputFileName = joinPath(dataFolder, 'output3.5_clean.txt')
    f = open(outputFileName, 'w')
    fileName = joinPath(dataFolder, 'output3.5.txt')      
    part = open(fileName, 'r')
    for line in part:
        if not 'm2017-05-16 ' in line and not 'mCOOKIE ' in line and not 'mSession ' in line and line[:4] != '2017':
            f.write(line) 
    f.close() 
    print_(outputFileName + ' has been written successfully.')
    
def outputsTest2():
    outputFileName = joinPath(dataFolder, 'output3.5_clean.txt')
    f = open(outputFileName, 'r')
    lines = [] 
    for line in f:
        lines.append(line[:-1])
    i = 0
    table = []
    c = 0
    while i < len(lines):
        l = lines[i]
        i += 1
        if len(l) > 2:
            if ':' == l[-1]:
                table.append([l[(3 if '.' == l[1] else 4):-1].lower()])
                j = i+5
                while i < j:
                    i += 1
                    l = lines[i]
                    s = l.split()
                    if len(s) < 2: 
                        t = i
                        while t < j:
                            table[-1 if len(table) > 0 else 0].append(0)
                            table[-1 if len(table) > 0 else 0].append("N/A")
                            t += 1
                        break
                    else:
                        table[-1 if len(table) > 0 else 0].append(int(s[0]))
                        table[-1 if len(table) > 0 else 0].append(s[-1])
            if 'sessions have been found' in l:
                j = i+1
                #print_(l)
                while i < j:
                    l = lines[i]
                    if "root" in l:
                        break
                    s = l.split()
                    table[c].append(int(s[0]))
                    table[c].append(s[-1])
                    i += 1
                c += 1
    print_(c)
    for r in table:
        print_(str(r)[1:-1].replace(", ", ",").replace("'", ""))
    f.close() 

def makeFolder():
    a = sc_().parallelize([])
    fromPath = joinPath(HDFSRootFolder, 'filteredLogsFromMay')
    saveRDDToHDFS(a, fromPath)

def runNewExtractionMethods():
    #oldTest()
    #wtcTest()
    # preferrerTest()
   outputsTest2()