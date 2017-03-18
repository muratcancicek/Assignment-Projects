from MNISTDatasetGenerator import generateThreeMNIST
from myMnistHandler import load_mnist
from SoftmaxTutorial import runSoftmax
from CNNTutorial import runCNNTutorial
from PythonVersionHandler import *
import tensorflow as tf

def getXY_(xSize = 784, ySize = 10):
    x = tf.placeholder(tf.float32, [None, 784])
    y_ = tf.placeholder(tf.float32, [None, 10])
    return x, y_

def learn(mnist = load_mnist('t10k')): # LocalMnist()
    x, y_ = getXY_()
    runSoftmax(mnist, x, y_)
    #runCNNTutorial(mnist, x, y_)

def main(): 
    original_mnist, downsampled_mnist, augmented_mnist = generateThreeMNIST()
    #learn(original_mnist)
    learn(downsampled_mnist)
    #learn(augmented_mnist)

