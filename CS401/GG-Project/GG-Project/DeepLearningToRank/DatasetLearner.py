from .NNetworkHandler import runCFirstCustomCNN, firstCNN, secondCNN
from .DatasetLoader import load_trainDataset
from MainSrc.PythonVersionHandler import *
import tensorflow as tf
from . import MyModel
from . import MyModel2
from . import tfFLAGS 
from paths import *

def getXY_(n = 12, clusters = 2):
    x = tf.placeholder(tf.float64, [None, n])
    y_ = tf.placeholder(tf.float64, [None, clusters])
    return x, y_

def learn(trainDataset, dataset = ''):
    tfFLAGS.printExperimentDetails()
    xSize = trainDataset.train.images.shape[1]
    x, y_ = getXY_(xSize)#trainDataset.train.labels.shape, clusters, trainDataset.train.labels.shape
    if tfFLAGS.network == 1: 
        MyModel.summarizeModel()
        text = 'The First Network on ' + dataset
        runCFirstCustomCNN(trainDataset, x, y_, xSize, cnn = MyModel.network, iterations = tfFLAGS.max_steps, text = text)
    if tfFLAGS.network == 2: 
        MyModel2.summarizeModel()
        text = 'The Second Network on ' + dataset
        runCFirstCustomCNN(trainDataset, x, y_, xSize, cnn = MyModel2.network, iterations = tfFLAGS.max_steps, text = text)
    
def learnDataset(trainDataPath, datasetName): 
    trainDataset = load_trainDataset(trainDataPath)
    learn(trainDataset, dataset = datasetName)