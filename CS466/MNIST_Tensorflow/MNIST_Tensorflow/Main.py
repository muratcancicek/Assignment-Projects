
from myMnist import load_mnist
from SoftmaxTutorial import runSoftmax
from CNNTutorial import runCNNTutorial
from PythonVersionHandler import *
import tensorflow as tf
import numpy as np
import struct
import os

def getXY_(xSize = 784, ySize = 10):
    x = tf.placeholder(tf.float32, [None, 784])
    y_ = tf.placeholder(tf.float32, [None, 10])
    return x, y_

def main(): 

    mnist = load_mnist('t10k') # LocalMnist()
    x, y_ = getXY_()
    runSoftmax(mnist, x, y_)
    runCNNTutorial(mnist, x, y_)

