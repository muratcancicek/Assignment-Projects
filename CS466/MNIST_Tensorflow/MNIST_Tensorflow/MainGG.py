#   
#   By Muratcan Cicek,  S004233, Computer Science at Ozyegin University
#   

from CNNetworkHandler import runCFirstCustomCNN, firstCNN, secondCNN
from MNISTDatasetGenerator import *
from myGGDataHandler import load_gg
from PythonVersionHandler import *
import tensorflow as tf

sys_argv = ['', 'network_1', '28x28_dataset', '/root/Projects/Assignment-Projects/CS466/MNIST_Tensorflow/MNIST_Tensorflow'] 
def getXY_(n = 784, clusters = 10):
    x = tf.placeholder(tf.float32, [None, n])
    y_ = tf.placeholder(tf.float32, [None, clusters])
    return x, y_

def learn(mnist, iterations = 100, downsampling = False, dataset = ''):
    xSize = mnist.train.images.shape[1]
    x, y_ = getXY_(xSize)
    if sys_argv[1] == 'network_1':
        text = 'The First Network on ' + dataset
        runCFirstCustomCNN(mnist, x, y_, xSize, cnn = firstCNN, iterations = iterations, downsampling = downsampling, text = text)
    if sys_argv[1] == 'network_2':
        text = 'The Second Network on ' + dataset
        runCFirstCustomCNN(mnist, x, y_, xSize, cnn = secondCNN, iterations = iterations, downsampling = downsampling, text = text)
    

def main(): 
    original_mnist = load_gg('D:\\Slow_Storage\\Senior_Data\\offlineData\\all_day_iphone_6_TrainData.txt')
    learn(original_mnist, dataset = 'GG')