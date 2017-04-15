from Sparker.MLlibTests.MlLibHelper import DenseVector, LabeledPoint
from MainSrc.PythonVersionHandler import *
from paths import *
from LogProcesser.JsonIO import *
from . import SparkLogReader as LogReader

TEST_LOGS_FILE = 'part-r-00000'
TEST_LOGS_FILE_ORINAL = 'part-r-00000_original'
TEST_LOGS = joinPath(clickstreamFolder, TEST_LOGS_FILE)
testFolder = joinPath(logInfoFolder, 'part-r-00000')

def saveOutput():
    outputFileName = joinPath(outputFolder, outputFileName)
    sys.stdout = open(outputFileName, 'w')

def setTestFile(testFile):
    global TEST_LOGS_FILE, TEST_LOGS, testFolder
    TEST_LOGS_FILE = testFile
    TEST_LOGS = joinPath(clickstreamFolder, TEST_LOGS_FILE)
    #testFolder = joinPath(logInfoFolder, TEST_LOGS_FILE)
    
#saveOutput()
#setTestFile(TEST_LOGS_FILE_ORINAL) 
#setTestFile('part-r-00000_iphone_6') 

_sc = None
def setSparkContext(scInstance):
   global _sc
   _sc = scInstance

def sc_():
    return _sc

lastReadLogs = None
def getAllLogs(logs = None, folder = allRawLogsfolder):
    global lastReadLogs
    if logs == None:
        if lastReadLogs != None and folder == allRawLogsfolder:
            return lastReadLogs
        else:
            logs = LogReader.readAllLogFiles(folder)
            logs = LogReader.parseAllLogs(logs)
            return logs 
    else:
        return logs
    return logs

def getLogs(logs = None, fromFileName = TEST_LOGS):
    global lastReadLogs
    if logs == None:
        if lastReadLogs != None and fromFileName == TEST_LOGS:
            return lastReadLogs
        else:
            logs = LogReader.getLogs(_sc, fromFileName)
            logs2 = []
            def botFilter(log):
                return '_bot' in log.keys() and log['_bot'] == 0
            return logs.filter(botFilter)
    else:
        return logs

def mergeAllParsedLogFiles(inputFolder, outputFileName, printing = True):  # Running, do not modify! 
    logs = sc_().emptyRDD()
    for i, filename in enumerate(os.listdir(inputFolder)):
        #if filename[-5:] != '.json':
        #    continue[:-5]
        filename = joinPath(inputFolder, filename)
        printing1 = printing or i % 200 == 0
        logs.union(LogReader.readAllLogFiles(sc_(), filename))
    writeToJson(logs, outputFileName)
    return logs

def mergeAllParsedLogLines(inputFolder, outputFileName, printing = True):
    f = open(outputFileName + '.json', 'w')
    f.write('[\n') 
    inputFolderList = os.listdir(inputFolder)
    last = len(inputFolderList) - 1
    for i, fileName in enumerate(inputFolderList):
        if fileName[-5:] != '.json':
            continue
        fileName = joinPath(inputFolder, fileName)        
        part = open(fileName, 'r')
        for line in part:
            if not line[0] in ['[', ']']:
                if line[-2] != ',' and i != last:
                    line = line[:-1] + ',\n'
                f.write(line) 
        printing1 = printing or i % 200 == 0
        if printing:
            print_(fileName + '.json has been appended successfully.')
    f.write(']') 
    f.close() 
    print_(outputFileName + '.json has been written successfully.')

def merge2016_09_27_iphone_6():
    path = joinPath(entireDayParsedLogsFolder1, 'TC_Journeys\\parts\\part-r-%05d\\part-r-%05d_keyword00000.json')#part-r-00000
    logs = sc_().emptyRDD()
    for i in range(24):
        filePath = path % (i, i)
        print_(filePath)
        logs = logs.union(readParsedLogs(filePath))
    logs.saveAsTextFile(joinPath(sparkFolder, '2016-09-27_iphone_6'))
    
def fixKeywords(logText):
    #a = "{u'orderBy': u'wbm', u'pageNum': 1, u'_bot': 0, u'keyword': 10000000000000000159028911097599180468360808563945281389781327557747838772170381060813469985856815104L, u'format': u'1%2C2%2C3%2C4', 'timestamp': 1482660614461, 'time': '2016-12-25 13:10:14.461000', u'agent': u'Mozilla%2F5.0 %28Windows NT 10.0%3B Win64%3B x64%29 AppleWebKit%2F537.36 %28KHTML%2C like Gecko%29 Chrome%2F55.0.2883.87 Safari%2F537.36', u'_ip': u'b0a84faead90d72d25b7d12a96eda8b4243a32dc18fdea214fe9a6f51b0da669', u'resultType': u'catalog', u'referer': u'http%3A%2F%2Fwww.gittigidiyor.com%2Farama', u'module': u'search', u'sid': u'onpnqor329b7a45o4qgnn4s8s2', u'_c': u'ae964d071805c570818642e61b325a07e7edabfe1af9c40181ec5fd87cf4e499', u'source': u'z'};"
    while(True):
        j = logText.find("L, u'")
        k = logText.find("L, '")
        if j == -1 and k == -1: break
        b = (j if j > -1 and j < k or k == -1 else k)+1
        i = logText[:b].rfind('\': ') + 3
        print_(logText[i:b])
        logText = logText[:i]+'u\''+logText[i:b]+'\''+logText[b:]
        print_(logText)
    return logText
    #
evalCounter = 0
def evalLog(logText):
    try:
        log = eval(logText)
    except SyntaxError:
        #begin, end = logText.find('{'), logText.find('}')
        log = eval(fixKeywords(logText))
    global evalCounter 
    evalCounter += 1
    if evalCounter % 100000 == 0: 
        print_('%i logs have been evaluated to Python Dict by %s' % (evalCounter, nowStr()))
    return log

def readParsedLogsFromHDFS(fileName): 
    logs = sc_().textFile(fileName)
    global evalCounter 
    evalCounter = 0
    logs = logs.map(evalLog)
    print_(fileName, 'has been read by', nowStr())
    return logs

def readJourneyFromHDFS(fileName): 
    journey = sc_().textFile(fileName)
    global evalCounter 
    evalCounter = 0
    journey = journey.map(evalLog)
    print_(fileName, 'has been read as journey by', nowStr())
    return journey

evalCounterForProducts = 0
def evalProduct(productText):
    if 'D' in productText:
        productText = productText.replace('DenseVector(', '')[:-1]
    product = eval(productText)
    product = (product[0], DenseVector(product[1]))
    global evalCounterForProducts
    evalCounterForProducts += 1
    if evalCounterForProducts % 100000 == 0: 
        print_('%i products have been evaluated to Python Dict by %s' % (evalCounterForProducts, nowStr()))
    return product

def readProductsFromHDFS(fileName = None):
    if fileName == None:
        fileName = "hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/product/vector" 
    products = sc_().textFile(fileName)
    products = products.map(evalProduct)
    return products

def readLabeledPairsFromHDFS(fileName):
    labeledPairs = sc_().textFile(fileName)
    labeledPairs = labeledPairs.map(eval)
    #ids = labeledPairs.map(lambda x: x[0].split('_'))sc_().parallelize(.collect())
    #def extender(a, b): a.extend(b); return a
    #ids = list(set(ids.reduce(extender)))
    #print_(labeledPairs.count())
    #print_(len(ids))
    return labeledPairs#, [int(id) for id in ids]

def readTrainDataFromHDFS(fileName):
    trainData = sc_().textFile(fileName)
    print_(fileName, 'has been read successfully by', nowStr())
    return trainData.map(eval).map(lambda x: LabeledPoint(1.0 if x[0] > 0 else 0.0, x[1])) 

def saveTrainDataToHDFS(trainData, outputFolder, inputName, keyword):
    trainDataFile = inputName + '_' + keyword + '_TrainData'
    trainData.saveAsTextFile(joinPath(outputFolder, trainDataFile))
    print_(trainDataFile, 'has been saved successfully by', nowStr())

def saveRDDToHDFS(rdd, fileName):
    rdd.saveAsTextFile(fileName)
    print_(fileName, 'has been saved successfully by', nowStr())

def parseAllDay(allDayPath, outputPath):
    logs = getLogs(None, allDayPath).sortBy(lambda log: log['timestamp'])
    saveRDDToHDFS(logs, outputPath)
