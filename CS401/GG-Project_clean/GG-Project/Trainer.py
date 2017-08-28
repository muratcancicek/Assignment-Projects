features = {'photos': 0, 'soldCount': 1, 'feedbackPercentage': 2, 'memberSoldCount': 3, 'memberSegment': 4, 
            'subtitleFlag': 5, 'brandNew': 6, 'freeCargo': 7, 'dailyOffer': 8, 'windowOptionFlag': 9, 'price': 10,
            'productCount': 11, 'hasphotos': 12, 'feedbackPercantageBlock': 13}
featuresList = ['photos', 'soldCount', 'feedbackPercentage', 'memberSoldCount', 'memberSegment', 
            'subtitleFlag', 'brandNew', 'freeCargo', 'dailyOffer', 'windowOptionFlag', 'price',
            'productCount', 'hasphotos', 'feedbackPercantageBlock']
featureVector = None

outputTable = []
def addColumnTitles(feature_names = None):
    titles = ['Keyword', 'LabeledPairs', 'LabeledProducts', 'FoundProducts', 'FoundPairs', 'TrainingPairs', 'TestPairs']
    if feature_names == None:
        feature_names = featuresList
    titles = titles + feature_names + ['TrainingAccuracy', 'TestAccuracy']
    outputTable.append(titles)

def setFeatureVector(feature_names):
    global featureVector
    import PythonVersionHandler
    PythonVersionHandler.print_(PythonVersionHandler.nowStr() + ': Features selected for the following trains:')
    PythonVersionHandler.print_(feature_names)
    addColumnTitles(feature_names)
    featureVector = [features[name] for name in feature_names]

def getFeatureVector():
    global featureVector
    if featureVector == None:
        return list(features.values())
    else:
        return featureVector
        
def evalProduct(productText):
    if 'D' in productText:
        productText = productText.replace('DenseVector([', '')[:-3] + ')'
    product = eval(productText)
    product = (product[0], product[1:])
    return product

def readProductsFromHDFS(fileName = None):
    import paths, SparkLogFileHandler
    if fileName == None:
        products = SparkLogFileHandler.sc_().textFile(paths.newProductVectorFolder)
    else:
        products = SparkLogFileHandler.sc_().textFile(fileName)
    products = products.map(evalProduct)
    #print_(products.first())
    #print_(fileName, products.count(), ' products have been read successfully by', nowStr())
    return products

def getProducts(ids, fileName = None):  
    products = readProductsFromHDFS(fileName)
    ids = ids.map(lambda i: (i, i))
    featureVector = getFeatureVector()
    def getReducedVector(vector):
        import pyspark.mllib.linalg 
        vector = [vector[i] for i in featureVector] 
        return pyspark.mllib.linalg.DenseVector(vector)
    foundProducts = ids.join(products).map(lambda p: (p[1][0], getReducedVector(p[1][1])))
    import PythonVersionHandler
    if PythonVersionHandler.LOGGING:
        ic = ids.count()
        fc = foundProducts.count()
        PythonVersionHandler.print_logging(ic, 'ids have been gathered from the labeled pairs by', PythonVersionHandler.nowStr())
        PythonVersionHandler.print_logging(fc, 'products have been found in database to train by', PythonVersionHandler.nowStr())
        outputTable[-1].extend([ic, fc])
    #print_(products.first())
    #products = products.map(lambda x: (x[0], DenseVector(x[1:])))
    return foundProducts

def readLabeledPairs(path):
    import paths, PythonVersionHandler, SparkLogFileHandler
    labeledPairs = SparkLogFileHandler.sc_().textFile(path)
    labeledPairs = labeledPairs.map(eval)
    if PythonVersionHandler.LOGGING:
        lc = labeledPairs.count()
        PythonVersionHandler.print_logging(path, 'with', lc, 'labeledPairs will be reading by', PythonVersionHandler.nowStr())
        outputTable[-1].append(lc)
    return labeledPairs

def normalizeTrainData(data):
    labels = data.map(lambda x: x.label)
    features = data.map(lambda x: x.features)
    normalizer1 = Normalizer()
    # Each sample in data1 will be normalized using $L^2$ norm.
    print_(data.count(), 'instances have been normalized by', PythonVersionHandler.nowStr())
    return labels.zip(normalizer1.transform(features)).map(lambda x: LabeledPoint(x[0], x[1]))

def scaleTrainData(features):
    import PythonVersionHandler, pyspark.mllib.feature
    scaler = pyspark.mllib.feature.StandardScaler(withMean=True, withStd=True).fit(features)
    PythonVersionHandler.print_high_logging(features.count(), 'instances have been scaled by', PythonVersionHandler.nowStr())
    return scaler.transform(features)

def generateTrainData(labeledPairs, products):  #TO DO 
    import PythonVersionHandler
    from pyspark.mllib.regression import LabeledPoint
    PythonVersionHandler.print_high_logging('train instances is being generated by', PythonVersionHandler.nowStr())
    products = products.collectAsMap()
    labeledPairs =labeledPairs.filter(lambda x: x[0][0] in products.keys() and x[0][1] in products.keys())
    labels = labeledPairs.map(lambda x: x[1])
    features =  labeledPairs.map(lambda x: products[x[0][0]] - products[x[0][1]])
    features = scaleTrainData(features)
    trainData = labels.zip(features).map(lambda x: LabeledPoint(x[0], x[1]))
    if PythonVersionHandler.LOGGING:
        tc = trainData.count()
        PythonVersionHandler.print_high_logging(tc, 'train instances have been generated by', PythonVersionHandler.nowStr())
        outputTable[-1].append(tc)
    return trainData 

def splitDataScientifically(data, weights = [0.70, 0.30]):
    import PythonVersionHandler
    if data.count() > 7000:
        weights = [0.90, 0.10]
    else: 
        weights = [0.80, 0.20]
    trainData, testData = data.randomSplit(weights)
    if PythonVersionHandler.LOGGING:
        trc = trainData.count(); tsc = testData.count()
        PythonVersionHandler.print_high_logging(trc, 'instances have been selected to be trained', PythonVersionHandler.nowStr())
        PythonVersionHandler.print_high_logging(tsc, 'instances have been selected to be tested', PythonVersionHandler.nowStr())
        outputTable[-1].extend([trc, tsc])
    return trainData, testData

def evaluateModelOnData(model, data, dataName = 'Data', modelName = 'Model'):
    instanceCount = data.count()
    if instanceCount == 0:
        return
    import PythonVersionHandler
    labelsAndPreds = data.map(lambda p: (p.label, model.predict(p.features)))
    truePredictionCount = labelsAndPreds.filter(lambda vp: vp[0] == vp[1]).count()
    accuracy = 100 * truePredictionCount / float(instanceCount)
    outputTable[-1].append(accuracy)
    PythonVersionHandler.print_high_logging('\n'+modelName, 'has been evaluated on', dataName, 'by', PythonVersionHandler.nowStr())
    PythonVersionHandler.print_logging('The result accuracy is %' + '%.3f\n' % (accuracy))
    return accuracy

def trainPairWiseData(data, dataName = 'Data', modelName = 'Model', evaluate = True):
    import pyspark.mllib.classification, PythonVersionHandler
    model = pyspark.mllib.classification.SVMWithSGD.train(data, iterations=1000)
    PythonVersionHandler.print_high_logging('\n'+modelName, 'has been trained on', dataName, 'by', PythonVersionHandler.nowStr())
    PythonVersionHandler.print_('The learned weights:\n' + str(model.weights).replace(',', ', ') + '\n')
    global lastWeights
    outputTable[-1].extend(model.weights)
    if evaluate:
        evaluateModelOnData(model, data, dataName, modelName)
    return model

def saveSpecificProduct(products, outputPath):
    import paths, SparkLogFileHandler
    #products = products.map(lambda x: tuple([x[0]]+x[1].toArray()))
    try: 
       SparkLogFileHandler.saveRDDToHDFS(products, outputPath)
    except:
        pass

def train(labeledPairsPath, productsPath, outputPath = None, saving = True, keyword = None):
    if len(outputTable) == 0: addColumnTitles()
    outputTable.append([] if keyword == None else [keyword])
    #try:
    labeledPairs = readLabeledPairs(labeledPairsPath)
    #except:
    #    import PythonVersionHandler
    #    PythonVersionHandler.print_(labeledPairsPath, 'does not exist!!!')
    #    return
    ids = labeledPairs.flatMap(lambda i: i[0]).distinct()
    products = getProducts(ids, productsPath)
    if outputPath != None and saving:
        saveSpecificProduct(products, outputPath)
    trainData = generateTrainData(labeledPairs, products)
    if trainData.isEmpty(): 
        return 
    trainData, testData = splitDataScientifically(trainData)
    model = trainPairWiseData(trainData, dataName = 'TrainData')
    accuracy = evaluateModelOnData(model, testData, dataName = 'TestData')
    return trainData, testData, model, accuracy

def getOutputTable():
    s = ''
    for r in outputTable:
        s += str(r).replace('\'', '')[1:-1] + '\n'
    return s

def printOutputTable():
    import PythonVersionHandler
    PythonVersionHandler.print_(getOutputTable())

def saveOutputTable():
    import os, paths
    c = 0
    fileName = paths.joinPath(paths.joinPath('outputs', 'tables'), 'outputTable' + str(c) + '.csv')
    while os.path.isfile(fileName):
        c += 1
        fileName = paths.joinPath(paths.joinPath('outputs', 'tables'), 'outputTable' + str(c) + '.csv')
    f = open(fileName, 'w')
    f.write(getOutputTable())
    f.close()
    import PythonVersionHandler
    PythonVersionHandler.print_(fileName, 'has been saved successfully by', PythonVersionHandler.nowStr())