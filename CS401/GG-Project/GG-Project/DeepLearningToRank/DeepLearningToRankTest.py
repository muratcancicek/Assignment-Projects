from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from Sparker.Logic.FakeProductGenerator import *
from Sparker.Logic.ProductPreferrer import *
from Sparker.Logic.TrainDataHandler import *
from Sparker.Logic.LogicTests import *
from Sparker.Logic.Trainer import *
from .DeepDataHandler import *
from .DatasetLearner import *
from .DeepTrainer import *
from pyspark import SparkContext

def test0():
    keyword = 'tv_unitesi'
    convertHDFStoPickle(keyword)

def test1():
    #allData = readTrainDataFromPickle('D:\\Slow_Storage\\Senior_Data\\offlineData\\all_day_iphone_6_TrainData.txt')
    #print_(allData[:9])
    #fp = open('D:\\Slow_Storage\\Senior_Data\\offlineData\\all_day_iphone_6_TrainDataSnipped.txt', "wb")   #Pickling
    #pickle.dump(allData[:100], fp)
    #allData = readTrainDataFromPickle('D:\\Slow_Storage\\Senior_Data\\offlineData\\all_day_iphone_6_TrainDataSnipped.txt')
    #print_(allData[:9])#Snipped
    learnDataset('D:\\Slow_Storage\\Senior_Data\\offlineData\\all_day_iphone_6_TrainData.txt')

def runTests():
    #sc = SparkContext() 
    #setSparkContext(sc)
    #trainPairWiseDataTestKeyword2('iphone 6')
    #convertPickleToHDFS('iphone_6')
    #trainPairWiseDataTestKeyword('iphone_6', inputFolder = offlineDataHDFSFolder)
    test1()