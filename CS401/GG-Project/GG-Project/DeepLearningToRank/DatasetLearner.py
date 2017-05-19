from .NNetworkHandler import runCFirstCustomCNN, firstCNN, secondCNN
from .DatasetLoader import load_trainDataset
from MainSrc.PythonVersionHandler import *
import tensorflow as tf
from .MyModel import *
from . import tfFLAGS 
from paths import *

def getXY_(n = 12, clusters = 2):
    x = tf.placeholder(tf.float32, [None, n])
    y_ = tf.placeholder(tf.float32, [None, clusters])
    return x, y_

def learn(trainDataset, iterations = 200, downsampling = False, dataset = ''):
    xSize = trainDataset.train.images.shape[1]
    x, y_ = getXY_(xSize)#trainDataset.train.labels.shape, clusters, trainDataset.train.labels.shape
    text = 'The First Network on ' + dataset
    runCFirstCustomCNN(trainDataset, x, y_, xSize, cnn = inference, iterations = iterations, downsampling = downsampling, text = text)
    
def learnDataset(trainDataPath): 
    trainDataset = load_trainDataset(trainDataPath)
    learn(trainDataset, dataset = 'GG')