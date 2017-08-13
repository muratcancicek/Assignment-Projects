
from SparkLogOperatorTests import *
from SparkLogAnalyzerTests import *
from SparkLogOperator import *
from SparkLogAnalyzer import *

from NewExtractorRunner import runNewExtractionMethods
l = []
def addPyFiles(sc, dr = joinPath(joinPath(joinPath(gitDir, 'CS401'), 'GG-Project'), 'GG-Project')):
    for filename in os.listdir(dr):
        #if filename in l: continue
        l.append(filename)
        p = joinPath(dr, filename)
        if filename[-3:] == '.py':
            sc.addPyFile(p) 
        #elif os.path.isdir(p):
        #    ##sc.addPyFile(p) 
        #    sc = addPyFiles(sc, p)
    return sc

def runSpark():
    conf = SparkConf()
    conf.set("spark.master", "spark://osldevptst02.host.gittigidiyor.net:7077")
    conf.set("spark.executor.memory", "12g")
    conf.set("spark.executor.instances", "2")
    sc = SparkContext(conf=conf) 
    sc = addPyFiles(sc)
    setSparkContext(sc)

def run(): 
    runSpark() 
    #trainLocalDataTest()
    runNewExtractionMethods()