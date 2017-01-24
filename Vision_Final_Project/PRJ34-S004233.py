#   Muratcan Cicek Department of Computer Science                           #
#   CS 423/523 Computer Vision Fall 2016 [Project 3-4] @Ozyegin_University  # 
#   python PRJ34-S004233.py

from Algorithms import *
import cv2
import FileHandler
FileHandler.GENERATING_EXTRA_FILES_ALLOWED = False

def main(): 
    runExperimentWithHighestAccuracy()

def runExperimentWithHighestAccuracy():
    featureCount = 200
    trainData, testData = FileHandler.readGrayscaleData(featureCount = featureCount)
    runRandomForestClassifier(trainData, testData, featureCount = featureCount, n_estimators = 1024, n_jobs = 4)

def runOtherExperiments():
    featureCount = 30
    trainData, testData = FileHandler.readData(featureCount = featureCount)
    runKNeighborsClassifier(trainData, testData, featureCount = featureCount, n_neighbors = 3)
    runRandomForestClassifier(trainData, testData, featureCount = featureCount, n_estimators = 1024, n_jobs = 4)
    featureCount = 200
    runKNeighborsClassifier(trainData, testData, featureCount = featureCount, n_neighbors = 3)
    runRandomForestClassifier(trainData, testData, featureCount = featureCount, n_estimators = 1024, n_jobs = 4)
    featureCount = 30
    trainData, testData = FileHandler.readGrayscaleData(featureCount = featureCount)
    runRandomForestClassifier(trainData, testData, featureCount = featureCount, n_estimators = 1024, n_jobs = 4)

main()
print 'DONE'
