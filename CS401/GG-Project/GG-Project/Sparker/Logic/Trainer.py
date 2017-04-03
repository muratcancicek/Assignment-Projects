from .ProductPreferrer import *
from Sparker.MLlibTests.MlLibHelper import *


def getProducts(ids, fileName = None):
    products = readProductsFromHDFS(fileName)
    ids = unique(ids)
    products = products.filter(lambda x: x[0] in ids).map(lambda x: (x[0], DenseVector(x[1:])))
    print_(products.count(), 'products has been found in database to train by', nowStr())
    return products

def generateTrainData(labeledPairs, products):
    labeledPairs = labeledPairs.map(lambda x: [int(id) for id in x[0].split('_')]+[x[1]])
    products = {id: vector for id, vector in products.collect()}
    productIds = unique(list(products.keys()))
    labeledPairs = labeledPairs.filter(lambda x: x[0] in productIds and x[1] in productIds)
    trainData = labeledPairs.map(lambda x: LabeledPoint(x[2], products[x[0]] - products[x[1]]))
    print_(trainData.count(), 'train instances has been generated by', nowStr())
    return trainData 

def extractJourneyLogsFromDay(keyword, logsFile, journeyFile):
    logs = getLogs(None, logsFile)
    print_(logs.count(), 'Logs have been read successfully by', nowStr())
    journey = getJourneyByKeyword(logs, keyword)
    print_(journey.count(), 'Log have been extracted for ' + keyword + ' journeys by', nowStr())
    journey.saveAsTextFile(journeyFile)
    print_(keyword, 'journey has been saved successfully by', nowStr())
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
    trainDataFile = inputName + '_' + keyword + '_' + '_TrainData'
    trainData.saveAsTextFile(joinPath(outputFolder, trainDataFile))
    print_(trainDataFile, 'has been saved successfully by', nowStr())
    return trainData

def trainPairWiseData(data):
    # Build the model
    model = SVMWithSGD.train(data, iterations=100)
    # Evaluating the model on training data
    labelsAndPreds = data.map(lambda p: (p.label, model.predict(p.features)))
    trainErr = labelsAndPreds.filter(lambda vp: vp[0] == vp[1]).count() / float(data.count())
    print_('\nAccuracy = ' + str(trainErr))
    print_('\nFirst weights = ' + str(model.weights) + '\n')
    return model
