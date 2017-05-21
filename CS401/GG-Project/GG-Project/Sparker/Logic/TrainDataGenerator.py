from Sparker.MLlibTests.MlLibHelper import *
from .ProductPreferrer import *
from .UpdatedProductPreferrer import *
from .FakeProductGenerator import *
from .TrainDataHandler import *
from .Trainer import *
    
def generateJourney(logs, keyword, day): 
    rawKeyword = keyword
    keyword = keyword.replace(' ', '_')
    outputFolder = joinPath(HDFSDataFolder, 'Day' + str(day) + '_' + keyword + '_Data')
    #if not os.path.exists(outputFolder):
    #    os.mkdir(outputFolder)
    inputName = 'all_day'
    journeyFile = joinPath(outputFolder, keyword + '_' + inputName + '_journey')
    journey = getJourneyByKeyword(logs, rawKeyword)
    saveRDDToHDFS(journey, journeyFile)

def generateJourneys(keywords = None, logs = None, day = 1):
    if logs == None: logs = readParsedLogsFromHDFS(entireDayParsedLogsFolder1)
    if keywords == None: #keywords = ['nike air max', 'spor ayyakab?', 'tv unitesi', 'kot ceket', 'camasir makinesi', 'bosch', 'k�pek mamas?']
        keywords = ['iphone 6', 'jant', 'nike air max', 'tv unitesi', 'kot ceket', 'camasir makinesi', 'bosch']
    for keyword in keywords:
        #print_('Day1_' + keyword.replace(' ', '_') + '_Data')
        generateJourney(logs, keyword, day)

def countJourneys():
    counts = []
    keywords = ['jant', 'nike air max', 'spor ayyakab?', 'tv unitesi', 'kot ceket', 'camasir makinesi', 'bosch', 'k�pek mamas?']
    for keyword in keywords:
        keyword = keyword.replace(' ', '_')
        outputFolder = joinPath(HDFSDataFolder, 'Day1_' + keyword + '_Data')
        inputName = 'all_day'
        journeyFile = joinPath(outputFolder, keyword + '_' + inputName + '_journey')
        journey = readJourneyFromHDFS(journeyFile)
        c = journey.count()
        counts.append((keyword, c))
        print_(journeyFile, 'contains', c, 'logs,', nowStr())
    for k, c in counts:
        print_(k, '=', c, 'relevant logs')

def generateKeywordLabeledPairsAndProducts(keyword, inputName, journeyFile, productsFile, outputFolder):
    journey = readJourneyFromHDFS(journeyFile)
    labeledPairsFile = joinPath(outputFolder, inputName + '_' + keyword + '_' + 'labeledPairs')
    modulizedIds = getLabeledPairsWithModulizedIds(journey)
    if not os.path.exists(labeledPairsFile):
        try:
            modulizedIds['labeledPairs'].saveAsTextFile(labeledPairsFile)
            print_(labeledPairsFile, 'have been saved successfully by', nowStr())
        except Py4JJavaError:
            pass
    products = getProducts(modulizedIds['listed'], productsFile)
    journeyProductsFile = joinPath(outputFolder, inputName + '_' + keyword + '_' + 'journey_products')
    if not os.path.exists(labeledPairsFile):
        try:
            products.saveAsTextFile(journeyProductsFile)
            print_(journeyProductsFile, 'have been saved successfully by', nowStr())
        except Py4JJavaError:
            pass
    labeledPairs = modulizedIds['labeledPairs']
    return labeledPairs, products

evalCounterForProducts = 0
def evalProduct(productText):
    if 'D' in productText:
        productText = productText.replace('DenseVector(', '')[:-1]
    product = eval(productText)
    product = (product[0], DenseVector(product[1:]))
    global evalCounterForProducts
    #evalCounterForProducts += 1
    #if evalCounterForProducts % 1000000 == 0: 
    #    print_('%i products have been evaluated to Python Dict by %s' % (evalCounterForProducts, nowStr()))
    return product

def readProductsFromHDFS(fileName = None):
    if fileName == None:
        fileName = "hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/product/vector" 
    products = sc_().textFile(fileName)
    products = products.map(evalProduct)
    #print_(products.first())
    print_(fileName, products.count(), ' products have been read successfully by', nowStr())
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
    trainData = trainData.map(lambda x: x.replace('LabeledPoint', '')).map(eval)
    return trainData.map(lambda x: x[1]).map(lambda x: LabeledPoint(1.0 if x[0] > 0 else 0.0, x[1:])) 

def saveTrainDataToHDFS(trainData, outputFolder, inputName, keyword, ext = ''):
    trainDataFile = inputName + '_' + keyword + '_TrainData' + ext
    trainData.saveAsTextFile(joinPath(outputFolder, trainDataFile))
    print_(trainDataFile, 'has been saved successfully by', nowStr())

def readKeywordLabeledPairsAndProducts(keyword, inputName, outputFolder):
    labeledPairsFile = joinPath(outputFolder, inputName + '_' + keyword + '_' + 'labeledPairs')
    labeledPairs = readLabeledPairsFromHDFS(labeledPairsFile)
    journeyProductsFile = joinPath(outputFolder, inputName + '_' + keyword + '_' + 'journey_products')
    products = readProductsFromHDFS(journeyProductsFile)
    print_('LabeledPairs And Products for', keyword, 'have been read successfully by', nowStr())
    return labeledPairs, products

def generateTrainDataAndSave(keyword, inputName, journeyFile, productsFile, outputFolder, generating = True):
    keyword = keyword.replace(' ', '_')
    #generating = False
    if generating:
        labeledPairs, products = generateKeywordLabeledPairsAndProducts(keyword, inputName, journeyFile, productsFile, outputFolder)
    else:
        labeledPairs, products = readKeywordLabeledPairsAndProducts(keyword, inputName, outputFolder)
    trainData = generateTrainData(labeledPairs, products)
    saveTrainDataToHDFS(trainData, outputFolder, inputName, keyword)
    return trainData

def trainDataGenerationTest(keyword): 
    keyword = keyword.replace(' ', '_')
    inputName = 'all_day'
    outputFolder = joinPath(HDFSDataFolder, 'Day1_' + keyword + '_Data')
    journeyFile = joinPath(outputFolder, keyword + '_' + inputName + '_journey')
    productsFile = None
    return generateTrainDataAndSave(keyword, inputName, journeyFile, productsFile, outputFolder)

def runtrainDataGenerationTest():
    #keywords = ['jant', 'nike air max',[:1] 'spor ayyakab?', 'tv unitesi', 'kot ceket', 'camasir makinesi', 'bosch', 'k�pek mamas?']
    keywords = ['jant', 'nike air max', 'tv unitesi', 'kot ceket', 'camasir makinesi', 'bosch']
    for keyword in keywords:
        trainDataGenerationTest(keyword)

def trainPairWiseDataTestKeyword(keyword, inputFolder = HDFSDataFolder):
    keyword = keyword.replace(' ', '_')
    inputName = 'all_day'
    outputFolder = joinPath(inputFolder, 'Day1_' + keyword + '_Data')
    trainDataFile = joinPath(outputFolder, inputName + '_' + keyword + '_TrainData')
    trainData = readTrainDataFromHDFS(trainDataFile)
    trainData = scaleTrainData(trainData)
    trainPairWiseData(trainData, dataName = keyword + '_TrainData', modelName =  keyword + '_TrainModel', evaluate = True)

def generateKeywordUpdatedLabeledPairsAndProducts(keyword, inputName, journeyFile, outputFolder):
    journey = readJourneyFromHDFS(journeyFile)
    labeledPairsFile = joinPath(outputFolder, inputName + '_' + keyword + '_' + 'UpdatedLabeledPairs')
    labeledPairs = getUpdatedLabeledPairs(journey)
    if not os.path.exists(labeledPairsFile):
        try:
            labeledPairs.saveAsTextFile(labeledPairsFile)
            print_(labeledPairsFile, 'have been saved successfully by', nowStr())
        except Py4JJavaError:
            pass
    journeyProductsFile = joinPath(outputFolder, inputName + '_' + keyword + '_' + 'journey_products')
    products = readProductsFromHDFS(journeyProductsFile)
    return labeledPairs, products

def readKeywordLabeledPairsAndProducts(keyword, inputName, outputFolder):
    labeledPairsFile = joinPath(outputFolder, inputName + '_' + keyword + '_' + 'UpdatedLabeledPairs')
    labeledPairs = readLabeledPairsFromHDFS(labeledPairsFile)
    journeyProductsFile = joinPath(outputFolder, inputName + '_' + keyword + '_' + 'journey_products')
    products = readProductsFromHDFS(journeyProductsFile)
    print_('LabeledPairs And Products for', keyword, 'have been read successfully by', nowStr())
    return labeledPairs, products


def generateUpdatedTrainDataAndSave(keyword, inputName, journeyFile, productsFile, outputFolder, generating = True):
    keyword = keyword.replace(' ', '_')
    #generating = False
    if generating:
        labeledPairs, products = generateKeywordUpdatedLabeledPairsAndProducts(keyword, inputName, journeyFile, productsFile, outputFolder)
    else:
        labeledPairs, products = readKeywordUpdatedLabeledPairsAndProducts(keyword, inputName, outputFolder)
    trainData = generateTrainData(labeledPairs, products)
    saveTrainDataToHDFS(trainData, outputFolder, inputName, keyword, '_Updated')
    return trainData

def updatedTrainDataGenerationTest(keyword): 
    keyword = keyword.replace(' ', '_')
    inputName = 'all_day'
    outputFolder = joinPath(HDFSDataFolder, 'Day1_' + keyword + '_Data')
    journeyFile = joinPath(outputFolder, keyword + '_' + inputName + '_journey')
    productsFile = None
    return generateUpdatedTrainDataAndSave(keyword, inputName, journeyFile, productsFile, outputFolder)

def runUpdatedTrainDataGenerationTest(i = 6):
    #keywords = ['jant', 'nike air max',[:1] 'spor ayyakab?', 'tv unitesi', 'kot ceket', 'camasir makinesi', 'bosch', 'k�pek mamas?']
    keywords = ['jant', 'nike air max', 'tv unitesi', 'kot ceket', 'camasir makinesi', 'bosch']
    for keyword in keywords[:i]:
        updatedTrainDataGenerationTest(keyword)