def may17ExtractionTest(day):
    dateStr = '2017-05-' + str(day)
    import paths, FinalizedRunners
    inputPath = paths.joinPath(may2017Folder, dateStr)
    keywords = get32Keywords()
    outputPath = paths.joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
    FinalizedRunners.saveExtractedLogsByKeywordsFromHDFS(inputPath, keywords, outputPath)

def pairingTest(day):
    keywords = get32Keywords() # 'zigon sehpa' # 'iphone 7' # "BEKO 9 KG CAMASIR MAKINESI" # 'tupperware' # get5Keywords() # _file_old
    dateStr = '2017-05-' + str(day)
    import paths, SparkLogFileHandler, FinalizedRunners
    extractedPath = paths.joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
    outputFolder = paths.joinPath(labeledPairsMayFromMayFolder, dateStr)
    FinalizedRunners.pairLabellingFromObjectiveLogsTest(extractedPath, keywords, outputFolder, filtering = False)

def mergeAll():
    import paths, SparkLogFileHandler, FinalizedRunners
    outputPath = paths.joinPath(filteredLogsFromMayFolder, 'allWeek_extractedLogs')
    logs = SparkLogFileHandler.sc_().parallelize([])
    for d in range(15, 22):
        dateStr = '2017-05-' + str(d)
        inputPath = paths.joinPath(filteredLogsFromMayFolder, dateStr + '_extractedLogs')
        logs = logs.union(FinalizedRunners.getPreparedLogsFromHDFS(inputPath, filtering = False))
    logs = logs.coalesce(24)
    SparkLogFileHandler.saveRDDToHDFS(logs, outputPath)

def pairAllTest():
    keywords = get32Keywords() 
    import paths, SparkLogFileHandler, FinalizedRunners
    extractedPath =  paths.joinPath(filteredLogsFromMayFolder, 'allWeek_extractedLogs')
    outputFolder = paths.joinPath(labeledPairsMayFromMayFolder, 'allWeek')
    FinalizedRunners.pairLabellingFromObjectiveLogsTest(extractedPath, keywords, outputFolder, filtering = False)
    
def trainTest():
    import paths, SparkLogFileHandler, FinalizedRunners, Trainer
    keyword = 'KIZ COCUK ABIYE ELBISE'.lower().replace(' ', '_') #'galaxy_s3' #'samsung_galaxy_s5_mini'
    pairsFolder = paths.joinPath(labeledPairsMayFromMayFolder, 'allWeek')
    pairsPath = paths.joinPath(pairsFolder, keyword + '_pairs')
    outputPath = paths.joinPath(paths.specificProductsFolder, keyword + '_products')
    productVectorFolder = outputPath
    Trainer.train(pairsPath, newProductVectorFolder, outputPath)

def trainAllTest():
    import paths, PythonVersionHandler, SparkLogFileHandler, FinalizedRunners, Trainer
    l = ['besiktas', 'kol_saati', 'iphone_7', 'iphone_7_kilif', 'nike_air_max', 'tupperware', 'stres_carki', 
    'buzdolabi', 'vestel_camasir_makinesi', 'samsung_galaxy_j7_prime', 'samsung', 'dikey_elektrikli_supurge', 
    'jbl_hoparlor', 'bisiklet', 'lenovo_k6_note', 'sandalye_kilifi', 'xiaomi', 'samsung_galaxy_s6', 
    'kirmizi_converse', 'kiz_cocuk_abiye_elbise', 'avon_kadin_parfum', 'kamp_cadiri', 'adidas', 'xiaomi_mi5',
    'samsung_galaxy_s5_mini']
    d = ['beko_9_kg_camasir_makinesi', 'kot_pantalon', 'mani_jeans_kot_pantalon']
    p = ['kadin_parfum', 'samsung_galaxy_s5_mini']
    for c, keyword in enumerate(get32Keywords()):
        PythonVersionHandler.print_logging(str(c+1)+'.', keyword.upper() + ':')
        keyword = keyword.lower().replace(' ', '_')
        #if keyword in l:
        #    PythonVersionHandler.print_logging('Weights have already been learned for this keyword')
        #    continue
        if keyword in d:
            PythonVersionHandler.print_logging('Pairs do not exist for this keyword')
            continue
        elif keyword in p:
            PythonVersionHandler.print_logging('TrainingData could not be generated for this keyword')
            continue
        pairsFolder = paths.joinPath(labeledPairsMayFromMayFolder, 'allWeek')
        pairsPath = paths.joinPath(pairsFolder, keyword + '_pairs')
        outputPath = paths.joinPath(paths.specificProductsFolder, keyword + '_products')
        productVectorFolder = outputPath
        Trainer.train(pairsPath, productVectorFolder, outputPath, saving = False)
        
def august(firstDay, lastDay):
    import paths, FinalizedRunners, ReadyTests
    inputPaths =[]
    for day in range(firstDay, lastDay + 1):
        dateStr = '2017-08-0' + str(day) if day < 10 else '2017-08-' + str(day)
        inputPath = paths.joinPath(paths.searchLogsFolder, dateStr)
        inputPaths.append(inputPath)
    keywords = ReadyTests.get27Keywords()[1:]
    outputPath = paths.joinPath(paths.HDFSRootFolder, 'weekAugust')
    FinalizedRunners.pairLabellingFromObjectiveLogs(inputPaths, keywords, outputPath)

def trainingTest21():
    import paths, FinalizedRunners, Trainer
    feature_names = ['photos', 'feedbackPercentage', 'memberSoldCount', 'soldCount',
            'memberSegment', 'subtitleFlag', 'brandNew', 'freeCargo', 'windowOptionFlag']
    Trainer.setFeatureVector(feature_names)
    keywords = ['besiktas', 'kol_saati', 'iphone_7', 'iphone_7_kilif']
    for keyword in keywords: 
        folder = paths.joinPath(paths.joinPath(paths.HDFSRootFolder, 'secondWeek'), keyword)
        FinalizedRunners.trainForKeyword(keyword, folder, saving = True)

def trainingTestAllLoop(feature_names):
    import paths, PythonVersionHandler, FinalizedRunners, Trainer, ReadyTests
    Trainer.setFeatureVector(feature_names)
    keywords = ReadyTests.get27Keywords()[:17]
    for c, keyword in enumerate(keywords): 
        PythonVersionHandler.print_logging(str(c+1)+'.', keyword.upper() + ':')
        keyword = keyword.replace(' ', '_')
        folder = paths.joinPath(paths.joinPath(paths.HDFSRootFolder, 'secondWeek'), keyword)
        FinalizedRunners.trainForKeyword(keyword, folder, saving = False)
    Trainer.printOutputTable()
    Trainer.saveOutputTable()
    Trainer.outputTable = []

def trainingTestAll():
    feature_names = ['photos', 'soldCount', 'feedbackPercentage', 'memberSoldCount', 'memberSegment', 
            'subtitleFlag', 'brandNew', 'freeCargo', 'dailyOffer', 'windowOptionFlag', 'price',
            'productCount']
    trainingTestAllLoop(feature_names)
    feature_names = ['photos', 'feedbackPercentage', 'memberSoldCount', 'soldCount',
            'memberSegment', 'subtitleFlag', 'brandNew', 'freeCargo', 'windowOptionFlag']
    trainingTestAllLoop(feature_names)
    
def bes():
    import paths, SparkLogFileHandler, SearchExtractor, FinalizedRunners, NewProductPreferrer, PythonVersionHandler
    keyword = 'besiktas'
    keyword_name = keyword
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
            
def besTrain():
    import paths, SparkLogFileHandler, SearchExtractor, FinalizedRunners
    keyword = 'besiktas'
    outputFolder = paths.joinPath(paths.HDFSRootFolder, 'weekAugust/' + keyword)
    FinalizedRunners.trainForKeyword(keyword, outputFolder, saving = True)

def runNewExtractionMethods():
    #trainAllTest()
    #may17ExtractionTest(29)
    #may17ExtractionTest(30)
    #may17ExtractionTest(31)
    #trainingTest21()
    august(7, 13)
    #trainingTestAll()
    #besTrain()

def runNewExtractionMethodsOnJupyter():
    import ReadyTests2
    ReadyTests2.printActMan()