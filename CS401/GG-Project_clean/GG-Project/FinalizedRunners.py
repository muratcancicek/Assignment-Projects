def readLogsFromMultiplePaths(inputPaths):
    import SparkLogFileHandler
    logs = SparkLogFileHandler.sc_().parallelize([])
    for p in inputPaths:
        logs.union(readLogs(sc_(), p, True))

def readLogs(inputPaths):
    if isinstance(inputPaths, str):
        import SparkLogReader
        logs = SparkLogReader.readLogs(sc_(), inputPaths, True)
    else:
        logs = readLogsFromMultiplePaths(inputPaths)
        
def readAndFilterLogs(inputPaths):
    logs = readLogs(inputPaths)
    import BotFilter
    return BotFilter.filterLogsForBots(logs)


def getPreparedLogsFromHDFS(inputPaths, filtering = True):
    if filtering:
        import BotFilter, SparkLogReader
        logs = BotFilter.readAndFilterLogs(inputPaths)
        logs = SparkLogReader.parseAllLogs(logs)
    else:
        import SparkLogFileHandler, PythonVersionHandler
        logs = SparkLogFileHandler.sc_().parallelize([])
        if isinstance(inputPaths, str):
            logs = SparkLogFileHandler.readParsedLogsFromHDFS(inputPaths)
        else:
            for p in inputPaths:
                logs = SparkLogFileHandler.readParsedLogsFromHDFS(p)
    PythonVersionHandler.print_logging(logs.count(), 'have been prepared by', nowStr())
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
    PythonVersionHandler.print_logging('Objective logs has been merged by', nowStr())
    objectiveLogs = objectiveLogs.coalesce(24)
    SparkLogFileHandler.saveRDDToHDFS(objectiveLogs, outputPath)