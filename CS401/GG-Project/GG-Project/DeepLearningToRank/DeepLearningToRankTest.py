from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from Sparker.Logic.FakeProductGenerator import *
from Sparker.Logic.ProductPreferrer import *
from Sparker.Logic.TrainDataHandler import *
from Sparker.Logic.LogicTests import *
from Sparker.Logic.Trainer import *
from .DeepDataHandler import *
from .DeepTrainer import *
from pyspark import SparkContext

def test0():
    keyword = 'tv_unitesi'
    convertHDFStoPickle(keyword)

def test1():
    trainPairWiseDataTestKeyword('iphone_6', inputFolder = joinPath(textTrainDataFolder, 'HDFS'))

def runTests():
    #sc = SparkContext() 
    #setSparkContext(sc)
    #trainPairWiseDataTestKeyword2('iphone 6')
    #convertPickleToHDFS('iphone_6')
    test1()