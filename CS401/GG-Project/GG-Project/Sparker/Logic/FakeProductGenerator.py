from .ProductPreferrer import *
from Sparker.MLlibTests.MlLibHelper import *

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

