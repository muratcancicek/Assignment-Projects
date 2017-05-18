from paths import *

from Sparker.PySparkImports import *
import sys
if sys.version_info[0] == 3:
    from sklearn.metrics import auc, roc_curve, average_precision_score, log_loss, mean_squared_error
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD
from MainSrc.PythonVersionHandler import *
from pyspark.mllib.classification import SVMWithSGD, SVMModel
from pyspark.mllib.feature import StandardScaler, StandardScalerModel
from pyspark.mllib.feature import Normalizer
from pyspark.mllib.util import MLUtils
from pyspark.mllib.linalg import DenseVector, SparseVector, Vectors 
from pyspark.mllib.common import *
from . import fm_parallel_sgd
import numpy as np
import time

trainUSPSFileName = 'usps-4-9-train.csv'
testUSPSFileName = 'usps-4-9-test.csv'

def csvLineToLabeledPoint(line, labelIndex = -1):
    return [np.float64(x) for x in line.split(',')]

def getSparseVectorsAsLabeledPoints(data, labelIndex = -1):
    sv = lambda features: SparseVector(len(features), enumerate(features))
    lbl = lambda l: 1 if l == 1 else -1
    getLabeledPoint = lambda vector: LabeledPoint(lbl(vector[labelIndex]), sv(vector[:labelIndex] + vector[labelIndex+1:]))
    return data.map(getLabeledPoint)

def readCSVDataAsDenseVectors(sc, fileName):
    fileName = joinPath(sparkFolder, fileName)
    data = sc.textFile(fileName).map(csvLineToLabeledPoint)
    data = getSparseVectorsAsLabeledPoints(data)
    return data

def getFloatListsAsLabeledPoints(data, labelIndex = -1):
    getLabeledPoint = lambda vector: LabeledPoint(vector[labelIndex], vector[:labelIndex] + vector[labelIndex+1:])
    return data.map(getLabeledPoint)

def readCSVDataAsLabeledPoints(sc, fileName):
    fileName = joinPath(sparkFolder, fileName)
    data = sc.textFile(fileName).map(csvLineToLabeledPoint)
    data = getFloatListsAsLabeledPoints(data)
    return data

def evaluateModelOnData(model, data):
    labelsAndPreds = data.map(lambda p: (p.label, model.predict(p.features)))
    trainErr = labelsAndPreds.filter(lambda vp: vp[0] == vp[1]).count() / float(data.count())
    print_('Accuracy = ' + str(trainErr))
    
def saveLogisticRegressionSparkModel(sc, model, modelFileName):
    modelFileName = joinPath(sparkFolder, modelFileName)
    model.save(sc, modelFileName)
    print_(nowStr() + ':', modelFileName, 'has been saved...')
    
def loadLogisticRegressionSparkModel(sc, modelFileName):
    print_(nowStr() + ':', 'loading', modelFileName + '...')
    modelFileName = joinPath(sparkFolder, modelFileName)
    return LogisticRegressionModel.load(sc, modelFileName)

def summaryData(trainData, testData = None):
    print_('trainData summary', trainData.map(lambda p: p.label).countByValue())
    if testData != None:
        print_('testData summary', testData.map(lambda p: p.label).countByValue())
        
def evaluateFM_SGD(data, w):
    evo = fm_parallel_sgd.evaluation(data)
    evo.evaluate(w)
    evo.display()
