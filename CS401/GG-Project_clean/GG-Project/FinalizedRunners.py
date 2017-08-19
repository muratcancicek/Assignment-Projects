def readLogsFromMultiplePaths(inputPaths):
    import SparkLogFileHandler, SparkLogReader
    logs = SparkLogFileHandler.sc_().parallelize([])
    for p in inputPaths:
        logs = logs.union(SparkLogReader.readLogs(SparkLogFileHandler.sc_(), p, True))
    return logs

def readLogs(inputPaths):
    if isinstance(inputPaths, str):
        import SparkLogFileHandler, SparkLogReader
        logs = SparkLogReader.readLogs(SparkLogFileHandler.sc_(), inputPaths, True)
    else:
        logs = readLogsFromMultiplePaths(inputPaths)
    return logs
        
def readAndFilterLogs(inputPaths):
    logs = readLogs(inputPaths)
    import BotFilter
    return BotFilter.filterLogsForBots(logs)


def getPreparedLogsFromHDFS(inputPaths, filtering = True):
    if filtering:
        import SparkLogReader
        logs = readAndFilterLogs(inputPaths)
        logs = SparkLogReader.parseAllLogs(logs)
    else:
        import SparkLogFileHandler
        logs = SparkLogFileHandler.sc_().parallelize([])
        if isinstance(inputPaths, str):
            logs = SparkLogFileHandler.readParsedLogsFromHDFS(inputPaths)
        else:
            for p in inputPaths:
                logs = SparkLogFileHandler.readParsedLogsFromHDFS(p)
    import PythonVersionHandler
    PythonVersionHandler.print_logging(logs.count(), 'have been prepared by', PythonVersionHandler.nowStr())
    return logs

def extractLogsByKeywordsFromHDFS(inputPaths, keywords, filtering = True):
    logs = getPreparedLogsFromHDFS(inputPaths, filtering = filtering)
    import SearchExtractor
    return SearchExtractor.searchNProductLogsByKeywords(logs, keywords)

def saveExtractedLogsByKeywordsFromHDFS(inputPaths, keywords, outputPath, filtering = True):
    import SparkLogFileHandler, PythonVersionHandler
    keywordDict = extractLogsByKeywordsFromHDFS(inputPaths, keywords, filtering = filtering)
    objectiveLogs = SparkLogFileHandler.sc_().parallelize([])
    for v in keywordDict:
        (searches, viewedProductLogs, cartedOrPaidProductLogs) = keywordDict[v]
        objectiveLogs = objectiveLogs.union(searches).union(viewedProductLogs).union(cartedOrPaidProductLogs)
    PythonVersionHandler.print_logging('Objective logs has been merged by', PythonVersionHandler.nowStr())
    objectiveLogs = objectiveLogs.coalesce(24)
    SparkLogFileHandler.saveRDDToHDFS(objectiveLogs, outputPath)

def tp(log):
    if isinstance(log, tuple):
        if isinstance(log[1], tuple): return log[1][1]
        else: return log[1]
    else: return log

def pairLabellingFromObjectiveLogsTest(inputPaths, keywords, outputFolder, filtering = False):
    import paths, SparkLogFileHandler, SearchExtractor, FinalizedRunners, NewProductPreferrer, PythonVersionHandler
    logs = getPreparedLogsFromHDFS(inputPaths, filtering = filtering) 
    logs = logs.map(tp)
    for keyword in keywords:
        searchNProductLogs = SearchExtractor.searchNProductLogsForSingleKeyword(logs, keyword)
        pairs = NewProductPreferrer.trainingInstancesForSingleKeyword(searchNProductLogs)
        if pairs.isEmpty():
            continue
        else:
            pairs = pairs.coalesce(24)
            outputPath = paths.joinPath(outputFolder, keyword.replace(' ', '_') + '_pairs')
            SparkLogFileHandler.saveRDDToHDFS(pairs, outputPath)
        PythonVersionHandler.print_logging()
    
def pairLabellingFromObjectiveLogs(inputPaths, keywords, outputFolder, filtering = True):
    import paths, SparkLogFileHandler, SearchExtractor, FinalizedRunners, NewProductPreferrer, PythonVersionHandler
    logs = getPreparedLogsFromHDFS(inputPaths, filtering = filtering)
    logs = logs.map(tp)
    for keyword in keywords:
        keyword_name = keyword.replace(' ', '_')
        searchNProductLogs = SearchExtractor.searchNProductLogsForSingleKeyword(logs, keyword)
        snpl = SparkLogFileHandler.sc_().parallelize([])
        for o in searchNProductLogs:
            snpl = snpl.union(o)
        snpl = snpl.coalesce(24)
        outputPath = paths.joinPath(outputFolder, keyword_name + '/' + keyword_name + '_extractedLogs')
        SparkLogFileHandler.saveRDDToHDFS(snpl, outputPath)
        pairs = NewProductPreferrer.trainingInstancesForSingleKeyword(searchNProductLogs)
        if pairs.isEmpty():
            continue
        else:
            pairs = pairs.coalesce(24)
            outputPath = paths.joinPath(outputFolder, keyword_name + '/' + keyword_name + '_pairs')
            SparkLogFileHandler.saveRDDToHDFS(pairs, outputPath)
        PythonVersionHandler.print_logging()

def trainForKeyword(keyword, folder = 'allWeek'):
    keyword = keyword.lower().replace(' ', '_')
    import paths, SparkLogFileHandler, FinalizedRunners, Trainer
    pairsFolder = paths.joinPath(paths.labeledPairsMayFromMayFolder, folder)
    pairsPath = paths.joinPath(pairsFolder, keyword + '_pairs')
    outputPath = paths.joinPath(paths.specificProductsFolder, keyword + '_products')
    ProductVectorFolder = outputPath
    Trainer.train(pairsPath, ProductVectorFolder, outputPath, saving = False)
