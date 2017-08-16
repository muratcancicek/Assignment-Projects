from paths import *
from PythonVersionHandler import *
from BotFilter import *
from Sessionizer import *
from ReadyTests import *
from ReadyTests2 import *
from FinalizedRunners import *
from SearchExtractor import *
from NewProductPreferrer import *
from SparkLogReader import *
from SparkLogFileHandler import *
from StringUtil import *

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
    keyword = 'AVON KADIN PARFUM'.lower().replace(' ', '_') #'galaxy_s3' #'samsung_galaxy_s5_mini'
    pairsFolder = paths.joinPath(labeledPairsMayFromMayFolder, 'allWeek')
    pairsPath = paths.joinPath(pairsFolder, keyword + '_pairs')
    outputPath = paths.joinPath(paths.specificProductsFolder, keyword + '_products')
    productVectorFolder = outputPath
    Trainer.train(pairsPath, newProductVectorFolder, outputPath)

def runNewExtractionMethods():
    #may17ExtractionTest(21)
    #printAct(16)
    #joinTests()
    #coalesceAll([16, 18, 19], 24)
    #pairingTest(16)
    #mergeAll()
    #pairAllTest()
    #outputsTest2()
    trainTest()