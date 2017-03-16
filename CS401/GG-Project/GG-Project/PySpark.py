import os
import sys
import LogProcesser.scalaToPython.python_codes.LumberjackParser as LumberjackParser
SPARK_HOME = os.environ['SPARK_HOME']

# Add the PySpark\\py4j to the Python Path
sys.path.insert(0, os.path.join(SPARK_HOME, "python", "lib"))
sys.path.insert(0, os.path.join(SPARK_HOME, "python"))

from pyspark import SparkContext 
from pyspark.mllib.regression import LabeledPoint
from pyspark import SparkContext, SparkConf
from pyspark.mllib.util import MLUtils
from pyspark.storagelevel import *
import pyspark.mllib.linalg
import numpy as np
from sklearn.metrics import auc, roc_curve, average_precision_score, log_loss, mean_squared_error
import time
import pickle
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def wordCount():
    sc=SparkContext() 
    lines = sc.textFile('D:\\OneDrive\\Projects\\Assignment-Projects\\CS401\\GG-Project\\GG-Project\\data\\ranking\\clickstream\\part-r-00000')
    lines = lines.map(lambda l: LumberjackParser.parse(l))#l.split('\t'))print(x)toLocalIterator()
    lines = lines.filter(lambda l: l['module'] == 'item')
    lines.foreach(print)
    #print('tan muratcan', lines.top(1))
#wordCount() data #

def fm_gradient_sgd_trick(X, y, W, regParam):
    """
    Computes the gradient for one instance using Rendle FM paper (2010) trick (linear time computation)
    """
    xa = np.array([X])
    x_matrix = xa.T.dot(xa)

    VX =  xa.dot(W)
    VX_square = (xa*xa).dot(W*W)
    phi = 0.5*(VX*VX - VX_square).sum()

    expnyt = np.exp(-y*phi)
    np.fill_diagonal(x_matrix,0)
    result = (-y*expnyt)/(1+expnyt)* (np.dot(x_matrix, W))
    return regParam*W + result

    
def subSGD(train_X, train_Y, w, iter_sgd, alpha, regParam):
    print(w)
    N = len(train_X)
    wsub = w
    G=np.ones(w.shape)
    for i in range(iter_sgd):
        np.random.seed(int(time.time())) 
        random_idx_list = np.random.permutation(N)
        for j in range(N):
            idx = random_idx_list[j]
            X = train_X[idx]
            y = train_Y[idx]
            grads = fm_gradient_sgd_trick(X, y, wsub, regParam)
            G += grads * grads
            wsub -= alpha * grads / np.sqrt(G)
    return wsub

def trainFM_parallel_sgd (sc, data, iterations=50, iter_sgd= 5,\
    alpha=0.01, regParam=0.01, factorLength=4,\
                verbose=False, savingFilename = None, evalTraining=None):

    train =data.persist(StorageLevel.MEMORY_ONLY_SER)

    # glom() allows to treat a partition as an array rather as a single row at time
    train_Y = train.map(lambda row: row['label']).glom()
    train_X = train.map(lambda row: row['features']).glom()
    train_XY = train_X.zip(train_Y).persist(StorageLevel.MEMORY_ONLY_SER)
    #train_XY = train_X.zip(train_Y).cache()

    nrFeat = len(train_XY.first()[0][0])
    np.random.seed(int(time.time())) 
    w =  np.random.ranf((nrFeat, factorLength))
    w = w / np.sqrt((w*w).sum())

    for i in range(iterations):
        wb = sc.broadcast(w)
        wsub = train_XY.map(lambda p: subSGD(p[0], p[1], wb.value, iter_sgd, alpha, regParam))
        w = wsub.mean()
    return w 

def test():
    sc=SparkContext() 
    lines = sc.textFile('D:\\OneDrive\\Projects\\Assignment-Projects\\CS401\\GG-Project\\GG-Project\\data\\productToPoint\\common\\ProductVector.csv')
    lines = lines.map(lambda line: [np.float64(v) for v in line.split(",")])
    lines = lines.map(lambda line: {'features':line[:-7], 'label': line[-1]})
    #lines.foreach(print)
    w = trainFM_parallel_sgd(sc, lines, iterations=5)
    print(w)
test()

#ssh -p 22 miek@127.0.0.1