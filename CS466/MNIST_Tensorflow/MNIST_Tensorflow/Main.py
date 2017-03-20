from FirstCustomCNNetwork import runCFirstCustomCNN
from SoftmaxTutorial import runSoftmax
from CNNTutorial import runCNNTutorial
from MNISTDatasetGenerator import *
from myMnistHandler import load_mnist
from PythonVersionHandler import *
import tensorflow as tf

def getXY_(n = 784, clusters = 10):
    x = tf.placeholder(tf.float32, [None, n])
    y_ = tf.placeholder(tf.float32, [None, clusters])
    return x, y_

def learn(mnist, iterations = 1000): # LocalMnist()
    xSize = mnist.train.images.shape[1]
    x, y_ = getXY_(xSize)
    #runSoftmax(mnist, x, y_, xSize, iterations = iterations)
    runCNNTutorial(mnist, x, y_, xSize, iterations = iterations)
    #runCFirstCustomCNN(mnist, x, y_, xSize, iterations = iterations)

def main(): 
    #original_mnist, downsampled_mnist, augmented_mnist = generateThreeMNIST()
    original_mnist = loadOriginalMNIST()
    learn(original_mnist)
    #downsampled_mnist= generateDownsampledMNIST()
    #learn(downsampled_mnist)
    #augmented_mnist = generateAugmentedMNIST()
    #learn(augmented_mnist)

    #original_mnist = load_mnist('t10k')
    #downsample(original_mnist.train.images)
