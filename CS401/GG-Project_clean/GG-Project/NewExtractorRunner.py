def trainTesting(keyword = 'iphone 7'):
    import paths, SparkLogFileHandler, SearchExtractor, FinalizedRunners, NewProductPreferrer, PythonVersionHandler
    keyword_name = keyword.replace(' ', '_')
    outputFolder = paths.joinPath(paths.HDFSRootFolder, 'weekAugust')
    outputPath = paths.joinPath(outputFolder, keyword_name + '/' + keyword_name + '_extractedLogs')
    logs = FinalizedRunners.getPreparedLogsFromHDFS(outputPath, filtering = False)
    searchNProductLogs = SearchExtractor.searchNProductLogsForSingleKeyword(logs, keyword)
    pairs = NewProductPreferrer.trainingInstancesForSingleKeyword(searchNProductLogs)
    if pairs.isEmpty():
        return
    else:
        pairs = pairs.coalesce(24)
        outputPath = paths.joinPath(outputFolder, keyword_name + '/' + keyword_name + '_pairs')
        SparkLogFileHandler.saveRDDToHDFS(pairs, outputPath)
        FinalizedRunners.trainForKeyword(keyword, outputFolder + '/' + keyword_name, saving = True)
        
def extractPairs():
    import paths, PythonVersionHandler, Trainer, ReadyTests
    feature_names = ['photos', 'soldCount', 'feedbackPercentage', 'memberSoldCount', 'memberSegment', 
                     'subtitleFlag', 'brandNew', 'freeCargo', 'dailyOffer', 'windowOptionFlag', 'price', 'productCount']
    Trainer.setFeatureVector(feature_names)
    keywords = ReadyTests.get27Keywords()[23:]
    for c, keyword in enumerate(keywords): 
        PythonVersionHandler.print_logging(str(c+1)+'.', keyword.upper() + ':')
        trainTesting(keyword)
    #Trainer.saveOutputTable()
    #Trainer.printOutputTable()

def trainingTestAllLoop(feature_names):
    import paths, PythonVersionHandler, FinalizedRunners, Trainer, ReadyTests
    Trainer.setFeatureVector(feature_names)
    keywords = ReadyTests.get27Keywords()
    for c, keyword in enumerate(keywords): 
        PythonVersionHandler.print_logging(str(c+1)+'.', keyword.upper() + ':')
        keyword = keyword.replace(' ', '_')
        folder = paths.joinPath(paths.joinPath(paths.HDFSRootFolder, 'weekAugust'), keyword)
        FinalizedRunners.trainForKeyword(keyword, folder, saving = False)
    Trainer.printOutputTable()
    Trainer.saveOutputTable()
    Trainer.outputTable = []

def trainingTestAll():
    feature_names = ['photos', 'soldCount', 'feedbackPercentage', 'memberSoldCount', 'memberSegment', 
            'subtitleFlag', 'brandNew', 'freeCargo', 'dailyOffer', 'windowOptionFlag', 'price', 'productCount']
    trainingTestAllLoop(feature_names)
    feature_names = ['photos', 'soldCount', 'feedbackPercentage', 'memberSoldCount',
            'memberSegment', 'brandNew', 'freeCargo', 'windowOptionFlag']
    trainingTestAllLoop(feature_names)
        
def extractPeriod(firstDay, lastDay):
    import paths, FinalizedRunners, ReadyTests
    inputPaths =[]
    for day in range(firstDay, lastDay + 1):
        dateStr = '2017-08-0' + str(day) if day < 10 else '2017-08-' + str(day)
        inputPath = paths.joinPath(paths.searchLogsFolder, dateStr)
        inputPaths.append(inputPath)
    keywords = ReadyTests.get27Keywords()
    outputPath = paths.joinPath(paths.HDFSRootFolder, 'weekAugust')
    FinalizedRunners.pairLabellingFromObjectiveLogs(inputPaths, keywords, outputPath, pairing = False, doneWords = 9)

def selection():
    import feature_selection
    feature_selection.selectFeaturesForAllKeywords()

def getLabeledPairsAndProductsPath(outputFolder, keyword, onlyFollowings = False, AllPageButId = False):
    keyword_name = keyword.replace(' ', '_')
    extension = '_extended'
    if onlyFollowings: extension + '_onlyFollowings'
    elif AllPageButId: extension + '_allPage'
    import paths
    pairsPath = paths.joinPath(outputFolder, keyword_name + '/' + keyword_name + '_pairs' + extension)
    productsPath = paths.joinPath(outputFolder, keyword_name + '/' + keyword_name + '_products' + extension)
    return pairsPath, productsPath

def extendedPairs(keyword = 'iphone 7', onlyFollowings = False, AllPageButId = False):
    import paths, SparkLogFileHandler, SearchExtractor, FinalizedRunners, NewProductPreferrer, PythonVersionHandler, Trainer
    keyword_name = keyword.replace(' ', '_')
    outputFolder = paths.joinPath(paths.HDFSRootFolder, 'weekAugust')
    inputPath = paths.joinPath(outputFolder, keyword_name + '/' + keyword_name + '_extractedLogs')
    logs = FinalizedRunners.getPreparedLogsFromHDFS(inputPath, filtering = False)
    searchNProductLogs = SearchExtractor.searchNProductLogsForSingleKeyword(logs, keyword)
    pairs = NewProductPreferrer.trainingInstancesForSingleKeyword(searchNProductLogs, onlyFollowings = onlyFollowings, AllPageButId = AllPageButId)
    if pairs.isEmpty():
        return
    pairs = pairs.coalesce(24)
    outputPath, productsPath = getLabeledPairsAndProductsPath(outputFolder, keyword, onlyFollowings = onlyFollowings, AllPageButId = AllPageButId)
    SparkLogFileHandler.saveRDDToHDFS(pairs, outputPath)
    ids = pairs.flatMap(lambda i: i[0]).distinct()
    PythonVersionHandler.print_logging(ids.count(), 'ids have been gathered from the labeled pairs by', PythonVersionHandler.nowStr())
    productVectorFolder = paths.newProductVectorFolder3
    products = Trainer.getProducts(ids, productVectorFolder)
    Trainer.saveSpecificProduct(products, productsPath)

def extendedProductExtraction(keyword = 'iphone 7', onlyFollowings = False, AllPageButId = False):
    import paths, SparkLogFileHandler, SearchExtractor, FinalizedRunners, NewProductPreferrer, PythonVersionHandler, Trainer
    outputFolder = paths.joinPath(paths.HDFSRootFolder, 'weekAugust')
    pairs = Trainer.readLabeledPairs(outputPath)
    ids = pairs.flatMap(lambda i: i[0]).distinct()
    PythonVersionHandler.print_logging(ids.count(), 'ids have been gathered from the labeled pairs by', PythonVersionHandler.nowStr())
    productVectorFolder = paths.newProductVectorFolder3
    products = Trainer.getProducts(ids, productVectorFolder)
    Trainer.saveSpecificProduct(products, productsPath)

def extractExtendedPairs(onlyFollowings = False, AllPageButId = False, doneWords = 0):
    import paths, PythonVersionHandler, Trainer, ReadyTests
    keywords = ReadyTests.get27Keywords()
    for c, keyword in enumerate(keywords): 
        PythonVersionHandler.print_logging(str(c+1)+'.', keyword.upper() + ':')
        if c < doneWords:
            PythonVersionHandler.print_logging('Extended pairs have already been extracted for', keyword)
            continue
        extendedPairs(keyword, onlyFollowings = onlyFollowings, AllPageButId = AllPageButId)

def trainExtendedPairs(keyword = 'iphone 7', onlyFollowings = False, AllPageButId = False):
    import Trainer, paths
    outputFolder = paths.joinPath(paths.HDFSRootFolder, 'weekAugust')
    pairsPath, productsPath = getLabeledPairsAndProductsPath(outputFolder, keyword, onlyFollowings = onlyFollowings, AllPageButId = AllPageButId)
    productVectorFolder = paths.newProductVectorFolder3
    Trainer.train(pairsPath, productVectorFolder, keyword = keyword)

def trainExtendedPairsLoop(onlyFollowings = False, AllPageButId = False):
    import paths, PythonVersionHandler, Trainer, ReadyTests
    feature_names = ['photos', 'soldCount', 'feedbackPercentage', 'memberSoldCount', 'memberSegment', 
                     'subtitleFlag', 'brandNew', 'freeCargo', 'dailyOffer', 'windowOptionFlag', 'sameDay']
    Trainer.setFeatureVector(feature_names)
    keywords = ReadyTests.get27Keywords()
    for c, keyword in enumerate(keywords): 
        PythonVersionHandler.print_logging(str(c+1)+'.', keyword.upper() + ':')
        trainExtendedPairs(keyword, onlyFollowings = onlyFollowings, AllPageButId = AllPageButId)
    Trainer.saveOutputTable()
    Trainer.printOutputTable()
    
def runNewExtractionMethods():
    extendedPairs('besiktas', AllPageButId = True)
    #extractExtendedPairs(AllPageButId = True)
    #trainExtendedPairsLoop(AllPageButId = True)
    #extractExtendedPairs(onlyFollowings = True)
    #trainExtendedPairsLoop(onlyFollowings = True)
    
def runNewExtractionMethods_old():
    #extractPeriod(7, 13)
    #extractPairs()
    #trainingTestAll()
    #selection()
    #extendedPairs(keyword = 'kol saati')
    #extendedProductExtraction(keyword = 'besiktas')
    pass

def runNewExtractionMethodsOnJupyter():
    import ReadyTests2
    ReadyTests2.printActMan()