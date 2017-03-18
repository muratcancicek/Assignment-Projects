from myMnistHandler import generateDatasetsWithValidation, DataSet, load_mnist
from PythonVersionHandler import *

def downsample(images):
    print_('Downsampling...')
    return images

def augment(images):
    images = downsample(images)
    print_('Aaugmenting...')
    return images

def generateThreeMNIST():
    original_mnist = load_mnist('t10k')
    downsampled_mnist = load_mnist('t10k', downsample)
    augmented_mnist = load_mnist('t10k', augment)
    return original_mnist, downsampled_mnist, augmented_mnist 