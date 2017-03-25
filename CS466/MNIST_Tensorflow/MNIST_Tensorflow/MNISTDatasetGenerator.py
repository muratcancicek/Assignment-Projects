#   
#   By Muratcan Cicek,  S004233, Computer Science at Ozyegin University
#   

from myMnistHandler import generateDatasetsWithValidation, DataSet, load_mnist
from PythonVersionHandler import *
from Transforms import *
import numpy as np

def subMatrix(img, colBgn, colEnd, colStep, rowBgn, rowEnd, rowStep):
    return img[colBgn:colEnd:colStep, rowBgn:rowEnd:rowStep]

def test(img):
    img = img.reshape((28, 28)) 
    img = np.arange(784).reshape((28, 28))
    #img = np.arange(16).reshape((4, 4))
    img = np.arange(64).reshape((8, 8))
    print_(img.shape)
    print_(img)
    print_('')
    print_(subMatrix(img, 0, 2, 1, 0, 2, 1))
    print_(img.shape)
    
def takeSquareMeansWithReshaping(img, squareSize = 2, n = -1):
    if n == -1: n = int(np.sqrt(img.shape[0]))
    img = img.reshape((n, n))
    means = []
    for y, row in enumerate(img):
        if y % squareSize != 0: continue
        for x, pixel in enumerate(row):
            if x % squareSize != 0: continue
            square = subMatrix(img, y, y+2, 1, x, x+2, 1).reshape((squareSize**2))
            means.append(square.mean())
    downsampledImg = np.array(means)
    return downsampledImg

def takeSquareMeans(img, squareN = 2, n = 28, downsampledN = 14):
    means = []
    i, doubleN, length, squareSize = (0, 2*n, n**2, squareN**2)
    while i < length:
        square = img[i] + img[i+1] + img[n+i] + img[n+i+1]
        means.append(square/squareSize)
        i += squareN
        if i % doubleN >= n:
            i += n
    downsampledImg = np.array(means)
    return downsampledImg

def downsample(images):
    print_('Downsampling by taking the mean of 2X2 Square Filtering...')
    images = images.reshape(images.shape[0], 784)
    return np.apply_along_axis(takeSquareMeans, 1, images) 

def augment(images, labels):
    #images = downsample(images)
    augmented = []
    l = []
    for i, img in enumerate(images):
        c = 1
        augmented.append(img)
        #rotated
        augmented.append(transform_image(img, output_shape=None, tf=None, zoom=(1.0, 1.0),
                    rotation=15, shear=0., translation=(0, 0), flip_lr=False,
                    flip_ud=False, warp_kwargs=None)); c += 1
        ## scaled
        augmented.append(transform_image(img, output_shape=None, tf=None, zoom=(.95, 1.0),
                    rotation=.0, shear=0., translation=(0, 0), flip_lr=False,
                    flip_ud=False, warp_kwargs=None)); c += 1

        #on my GPU with there of them
        # rotated & scaled / hope making italic
        augmented.append(transform_image(img, output_shape=None, tf=None, zoom=(.9, 1.0),
                    rotation=-15, shear=0., translation=(0, 0), flip_lr=False,
                    flip_ud=False, warp_kwargs=None)); c += 1

        for j in range(c):
            l.append(labels[i])
    print_('Aaugmenting...')
    return np.array(augmented), np.array(l)

def loadOriginalMNIST():
    return load_mnist('t10k')
    
def generateDownsampledMNIST():
    return load_mnist('t10k', downsample, reshape = False)
    
def generateAugmentedMNIST():
    return load_mnist('t10k', augment)

def generateThreeMNIST():
    return loadOriginalMNIST(), generateDownsampledMNIST(), generateAugmentedMNIST()