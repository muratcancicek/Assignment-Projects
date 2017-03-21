from CNNetworkHandler import runCFirstCustomCNN, firstCNN, secondCNN
from MNISTDatasetGenerator import *
from myMnistHandler import load_mnist
from PythonVersionHandler import *
import tensorflow as tf

def getXY_(n = 784, clusters = 10):
    x = tf.placeholder(tf.float32, [None, n])
    y_ = tf.placeholder(tf.float32, [None, clusters])
    return x, y_

def learn(mnist, iterations = 300, downsampling = False, dataset = ''):
    xSize = mnist.train.images.shape[1]
    x, y_ = getXY_(xSize)
    if sys.argv[1] == 'network_1':
        text = 'The First Network on ' + dataset
        runCFirstCustomCNN(mnist, x, y_, xSize, cnn = firstCNN, iterations = iterations, downsampling = downsampling, text = text)
    
    if sys.argv[1] == 'network_2':
        text = 'The Second Network on ' + dataset
        runCFirstCustomCNN(mnist, x, y_, xSize, cnn = secondCNN, iterations = iterations, downsampling = downsampling, text = text)

def main(cmdargs): 
    print_(cmdargs)
    if sys.argv[2] == '28x28_dataset':
        original_mnist = loadOriginalMNIST()
        learn(original_mnist, dataset = '28x28_dataset')
    if sys.argv[2] == '14x14_dataset':
        original_mnist = loadOriginalMNIST()
        learn(original_mnist, downsampling = True, dataset = '14x14_dataset')
    if sys.argv[2] == '14x14_augmented_dataset':
        augmented_mnist = generateAugmentedMNIST()
        learn(augmented_mnist, downsampling = True, dataset = '14x14_augmented_dataset')

    #cd Assignment-Projects/CS466/MNIST_Tensorflow/MNIST_Tensorflow
     #  python muratcan_cicek_training.py network_1 28x28_dataset