from .ProductPreferrer import *
from Sparker.MLlibTests.MlLibHelper import *
from .ProductPreferrer import *
from pyspark.mllib.feature import Normalizer


def getProducts(ids, fileName = None):
    products = readProductsFromHDFS(fileName)
    ids = unique(ids)
    products = products.filter(lambda x: x[0] in ids)
    print_(products.count(), 'products has been found in database to train by', nowStr())
    print_(products.first())
    #products = products.map(lambda x: (x[0], DenseVector(x[1:])))
    return products

def generateTrainData(labeledPairs, products):
    print_('train instances is being generated by', nowStr())
    labeledPairs = labeledPairs.map(lambda x: [int(id) for id in x[0].split('_')]+[x[1]])
    products = {id: vector for id, vector in products.collect()}
    productIds = unique(list(products.keys()))
    labeledPairs = labeledPairs.filter(lambda x: x[0] in productIds and x[1] in productIds)
    trainData = labeledPairs.map(lambda x: (keyPairIds(x[0], x[1]), LabeledPoint(x[2], products[x[0]] - products[x[1]])))
    print_(trainData.count(), 'train instances have been generated by', nowStr())
    return trainData 

def scaleTrainData(data):
    label = data.map(lambda x: x.label)
    features = data.map(lambda x: x.features)
    scaler = StandardScaler(withMean=True, withStd=True).fit(features)
    return label.zip(scaler.transform(features.map(lambda x: Vectors.dense(x.toArray())))).map(lambda x: LabeledPoint(x[0], x[1]))

def normalizeTrainData(data):
    labels = data.map(lambda x: x.label)
    features = data.map(lambda x: x.features)
    normalizer1 = Normalizer()
    # Each sample in data1 will be normalized using $L^2$ norm.
    print_(data.count(), 'instances have been normalized by', nowStr())
    return labels.zip(normalizer1.transform(features)).map(lambda x: LabeledPoint(x[0], x[1]))

def extractJourneyLogsFromDay(keyword, logsFile, journeyFile):
    logs = getLogs(None, logsFile)
    print_(logs.count(), 'Logs have been read successfully by', nowStr())
    journey = getJourneyByKeyword(logs, keyword)
    print_(journey.count(), 'Logs have been extracted for ' + keyword + ' journeys by', nowStr())
    journey.saveAsTextFile(journeyFile)
    print_(journeyFile, 'as', keyword, 'journey has been saved successfully by', nowStr())
    return journey

def extractLabeledPairsFromJourney(keyword, inputName, journeyFile, productsFile, outputFolder):
    keyword = keyword.replace(' ', '_')
    journey = readJourneyFromHDFS(journeyFile)
    modulizedIds = getLabeledPairsWithModulizedIds(journey)
    labeledPairsFile = inputName + '_' + keyword + '_' + 'labeledPairs'
    modulizedIds['labeledPairs'].saveAsTextFile(joinPath(outputFolder, labeledPairsFile))
    print_(labeledPairsFile, 'have been saved successfully by', nowStr())
    products = getProducts(modulizedIds['listed'], productsFile)
    journeyProductsFile = inputName + '_' + keyword + '_' + 'journey_products'
    products.saveAsTextFile(joinPath(outputFolder, journeyProductsFile))
    print_(journeyProductsFile, 'have been saved successfully by', nowStr())
    trainData = generateTrainData(modulizedIds['labeledPairs'], products)
    saveTrainDataToHDFS(trainData, outputFolder, inputName, keyword)
    return trainData

def generateTrainData1(logs, keyword, outputFolder): 
    rawKeyword = keyword
    keyword = keyword.replace(' ', '_')
    inputName = 'all_day'
    journeyFile = joinPath(outputFolder, keyword + '_' + inputName + '_journey')
    if logs != None:
        journey = getJourneyByKeyword(logs, rawKeyword)
        saveRDDToHDFS(journey, journeyFile)
    productsFile = None
    return extractLabeledPairsFromJourney(keyword, inputName, journeyFile, productsFile, outputFolder)

def evaluateModelOnData(model, data, dataName = 'Data', modelName = 'Model'):
    labelsAndPreds = data.map(lambda p: (p.label, model.predict(p.features)))
    truePredictionCount = labelsAndPreds.filter(lambda vp: vp[0] == vp[1]).count()
    instanceCount = data.count()
    accuracy = 100 * truePredictionCount / float(instanceCount)
    print_('\n'+modelName, 'has been evaluated on', dataName, 'by', nowStr())
    print_('The result accuracy is %' + '%.3f\n' % (accuracy))
    return labelsAndPreds

def trainPairWiseData(data, dataName = 'Data', modelName = 'Model', evaluate = True):
    model = SVMWithSGD.train(data, iterations=100)
    print_('\n', modelName, 'has been trained on', dataName, 'by', nowStr())
    print_('The learned weights:\n' + str(model.weights).replace(',', ', ') + '\n')
    if evaluate:
        evaluateModelOnData(model, data, dataName, modelName)
    return model

def runTrainingExperiment(trainData, testData, modelName = 'Model', save = True, outputFolder = Day1_iPhone_6_DataFolder):
    trainData = scaleTrainData(trainData)
    testData = scaleTrainData(testData)
    model = trainPairWiseData(trainData, 'trainData', modelName)
    if save:
        modelPath = joinPath(outputFolder, modelName)
        try:
            model.save(sc_(), modelPath)
        except Py4JJavaError:
            pass
        print_(modelPath, 'has been saved successfully by', nowStr())
    return evaluateModelOnData(model, testData, 'testData', modelName)

def rankProducts(products, outputFolder, model = None, modelName = 'Model_v04_4'):
    if model == None:
        modelPath = joinPath(outputFolder, modelName)
        model = SVMModel.load(sc_(), modelPath)
    print_(products.first())
    if isinstance(products.first()[1], list):
        products = products.map(lambda x: (x[0], DenseVector(x[1])))
    products = products.map(lambda x: (-x[1].dot(model.weights), (x[0], x[1])))
    #print_(products.take(2))
    products = products.sortByKey()
    #print_(products.take(2))
    products = products.zipWithIndex().map(lambda x: (x[1] + 1, -x[0][0], x[0][1][0], x[0][1][1]))
    print_(products.count(), 'products have been ranked successfully by', nowStr())
    #print_(products.take(2))
    productsPath = joinPath(outputFolder, 'all_day_iphone_6_journey_rankedProducts')
    saveRDDToHDFS(products, productsPath)
    productsList = products.map(lambda x: x[2]).take(50)
    print_(productsList)
    return products
