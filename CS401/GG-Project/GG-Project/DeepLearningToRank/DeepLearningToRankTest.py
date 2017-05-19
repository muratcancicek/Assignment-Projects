from Sparker.SparkLogProcesser.SparkLogFileHandler import *
from Sparker.Logic.FakeProductGenerator import *
from Sparker.Logic.ProductPreferrer import *
from Sparker.Logic.TrainDataHandler import *
from Sparker.Logic.LogicTests import *
from MainSrc.SparkerMethods import *
from Sparker.Logic.Trainer import *
from .DeepDataHandler import *
from DeepLearningToRank.MultiGPU_Tools.cifar10_multi_gpu_train import *
from .DatasetLearner import *
from .DeepTrainer import *
from pyspark import SparkContext

def test0():
    keyword = 'tv_unitesi'
    convertHDFStoPickle(keyword)

def test1():
    runSpark()
    for keyword in ['iphone 6', 'jant', 'nike air max', 'kot ceket', 'camasir makinesi', 'bosch']:#'tv unitesi', /soe/cicekm/Projects/offlineData/all_day_tv_unitesi_journey_products.txt problem
        convertPickleToHDFS(keyword)

def test2():
    learnDataset(joinPath(textTrainDataFolder, 'all_day_jant_TrainData.txt'))

def test3():
    dataset = load_trainDataset(joinPath(textTrainDataFolder, 'all_day_iphone_6_TrainData.txt'))
    trainOnMultiGPU(dataset)

def runTests():
    #sc = SparkContext() 
    #setSparkContext(sc)
    ##trainPairWiseDataTestKeyword2('iphone 6')
    ##convertPickleToHDFS('iphone_6')
    #trainPairWiseDataTestKeyword('iphone_6', inputFolder = offlineDataHDFSFolder)
    test3()