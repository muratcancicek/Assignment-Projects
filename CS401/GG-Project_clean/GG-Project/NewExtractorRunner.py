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
        FinalizedRunners.trainForKeyword(keyword, outputFolder, saving = True)
        
def extractPairs():
    import paths, PythonVersionHandler, Trainer, ReadyTests2
    feature_names = ['photos', 'soldCount', 'feedbackPercentage', 'memberSoldCount', 'memberSegment', 
                     'subtitleFlag', 'brandNew', 'freeCargo', 'dailyOffer', 'windowOptionFlag', 'price', 'productCount']
    Trainer.setFeatureVector(feature_names)
    keywords = ReadyTests.get27Keywords()[:22]
    done =['basiktas', 'iphone 7']
    for c, keyword in enumerate(keywords): 
        if keyword in done: continue
        PythonVersionHandler.print_logging(str(c+1)+'.', keyword.upper() + ':')
        trainTesting(keyword)
    Trainer.saveOutputTable()
    Trainer.printOutputTable()
        
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

def runNewExtractionMethods():
    #extractPeriod(7, 13)
    extractPairs()

def runNewExtractionMethodsOnJupyter():
    import ReadyTests2
    ReadyTests2.printActMan()