from Sparker.MLlibTests.LogisticRegressionImpOnSpark import runLogisticRegressionImplementationOnSpark
from Sparker.MLlibTests.LogisticRegressionWithSpark import runLogisticRegressionWithSpark
from Sparker.MLlibTests.HousingTutorialWithFM import runHousingTutorialWithFM
from Sparker.MLlibTests.LogisticRegressionFromCS434_HW2 import main as hw2Main
from Sparker.MLlibTests.MlLibHelper import *

from Sparker.SparkLogProcesser.SparkLogOperatorTests import *
from Sparker.SparkLogProcesser.SparkLogAnalyzerTests import *
from Sparker.Logic.LogicTests import *
from Sparker.SparkLogProcesser.SparkLogOperator import *
from Sparker.SparkLogProcesser.SparkLogAnalyzer import *
from Sparker.PySparkTutorial1 import *

from Sparker.NewJourneyExtractor.NewExtractorRunner import runNewExtractionMethods

def runSparkerTests(sc):
    countModule(sc)
    hw2Main()
    runLogisticRegressionWithSpark(sc)
    testToTrainFM_parallel_sgd(sc)
    runLogisticRegressionImplementationOnSpark(sc)

def runSparkLogProcesserTests(logs):
    logs = getLogs()
    basicTests()
    countTestsForTransposes(logs)
    mapReduceTests(logs)
    moduleTests(logs)
    snippingTests(logs)
    idCookieTests(logs)
    cookieJourneyTest(logs)
    coloredLogPrintingTests(logs)
    coloredJourneyPrintingTest(logs)
    journeyByKeywordTest(logs)
    printingActionsTest(logs)

def runSparkLogOperatorTests(logs):
    logs = getLogs()
    writeRDDToJsonTest(logs)
    readTextFileTest(logs)
    #extractAllTCJourneysTest()
    
l = []
def addPyFiles(sc, dr = joinPath(joinPath(joinPath(gitDir, 'CS401'), 'GG-Project'), 'GG-Project')):
    for filename in os.listdir(dr):
        if filename in l: continue
        l.append(filename)
        p = joinPath(dr, filename)
        if filename[-3:] == '.py':
            sc.addPyFile(p) 
        elif os.path.isdir(p):
            ##sc.addPyFile(p) 
            sc = addPyFiles(sc, p)
    return sc

def runSpark():
    conf = SparkConf()
    #conf.set("spark.master", "spark://osldevptst02.host.gittigidiyor.net:7077")
    conf.set("spark.executor.memory", "12g")
    conf.set("spark.executor.instances", "2")
    sc = SparkContext(conf=conf) 
    #sc = addPyFiles(sc)
    setSparkContext(sc)

def run(): 
    runSpark() 
    #trainLocalDataTest()
    runNewExtractionMethods()