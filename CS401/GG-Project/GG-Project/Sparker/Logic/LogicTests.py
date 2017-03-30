from .ProductPreferrer import *
from Sparker.MLlibTests.MlLibHelper import *

def getSampleJourney(logs):
    keyword = 'lg g4'#'iphone 6'# getKeywords()[1]
    return getJourneyByKeyword(logs, keyword)

def getLabeledIds():
    labeledPairs = sc_().textFile(joinPath(sparkFolder, 'labels'))#('hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/data/part-r-00000_iphone_6')
    labeledPairs = labeledPairs.map(eval)
    ids = labeledPairs.map(lambda x: x[0].split('_'))
    def extender(a, b): a.extend(b); return a
    ids = unique(ids.reduce(extender))
    #print_(labeledPairs.count())
    #print_(len(ids))
    return labeledPairs, [int(id) for id in ids]

def csvLineToDenseVector(line, labelIndex = -1):
    return tuple([np.float64(x) for x in line.split(',')][:10])

def readCSVDataAsLabeledPoints(sc, fileName):
    fileName = joinPath(sparkFolder, fileName)
    data = sc.textFile(fileName).map(csvLineToDenseVector)
    return data

def getFakeProducts(ids):
    trainData = readCSVDataAsLabeledPoints(sc_(), trainUSPSFileName)
    testData = readCSVDataAsLabeledPoints(sc_(), testUSPSFileName)
    products = trainData.union(testData).collect()
    if len(products) >= len(ids):
        products = products[:len(ids)]
    else:
        ids = ids[:len(products)]
    productTuples = []
    for id, v in zip(ids, products):
        productTuples.append(tuple([id]+list(v)))
    productTuples = sc_().parallelize(productTuples)
    productTuples.saveAsTextFile(joinPath(sparkFolder, 'sampleProducts'))
    return productTuples

def getProducts(ids):
    ## sc.textFile ("hdfs://osldevptst01.host.gittigidiyor.net:8020/user/root/product/vector")
    products = sc_().textFile(joinPath(sparkFolder, 'sampleProducts'))
    print(products.first())
    products = products.map(eval)
    products = products.filter(lambda x: x[0] in ids).map(lambda x: (x[0], DenseVector(x[1:])))
    return products

def generateTrainData(labeledPairs, products):
    labeledPairs = labeledPairs.map(lambda x: [int(id) for id in x[0].split('_')]+[x[1]])
    products = {id: vector for id, vector in products.collect()}
    trainData = labeledPairs.map(lambda x: LabeledPoint(x[2], products[x[0]] - products[x[1]]))
    trainData.saveAsTextFile(joinPath(sparkFolder, 'iPhone_6_TrainData'))
    return trainData 

def getTrainData():
    trainData = sc_().textFile(joinPath(sparkFolder, 'iPhone_6_TrainData'))
    return trainData.map(eval).map(lambda x: LabeledPoint(x[0], x[1])) 

def trainPairWiseData(data):
    # Build the model
    model = SVMWithSGD.train(data, iterations=100)

    # Evaluating the model on training data
    labelsAndPreds = data.map(lambda p: (p.label, model.predict(p.features)))
    trainErr = labelsAndPreds.filter(lambda vp: vp[0] == vp[1]).count() / float(data.count())
    print("Accuracy = " + str(trainErr))


def getIdsTest(logs):
    #labeledPairs, ids = getLabeledIds()
    #products = getProducts(ids)
    #print(products.first())
    trainData = getTrainData()#generateTrainData(labeledPairs, products)
    print(trainData.first())
    trainPairWiseData(trainData)

def testAlgorithm():
    if logs == None:
        #journey = getSampleJourney(logs)
        #journey.saveAsTextFile(joinPath(sparkFolder, 'lg_g4_journey'))
        #logs = sc_().textFile(joinPath(sparkFolder, 'lg_g4_journey')).map(lambda l: eval(l)) 
        #logs = getLogs()
        #logs = load2016_09_27_iphone_6()
        logs = readParsedLogs(joinPath(sparkFolder, 'part-r-00000_keyword00000.json'))
    ##printActions(journey)
    labeledPairs = getInterestingIds(logs)
    #sc_().parallelize(labeledPairs.items()).saveAsTextFile(joinPath(sparkFolder, 'labels'))