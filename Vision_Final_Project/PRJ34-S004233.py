#   Muratcan Cicek Department of Computer Science                           #
#   CS 423/523 Computer Vision Fall 2016 [Project 3-4] @Ozyegin_University  # 

import cv2
from Algorithms import *
from ProjectFilesIO import *
from sklearn.neighbors import KNeighborsClassifier

def main():
    trainData =unpickle('trainData_PCA30')
    testData = unpickle('testData_PCA30')
    neigh = KNeighborsClassifier(n_neighbors=3)
    bench_estimator(trainData, testData, estimator = neigh, name = 'KNeighborsClassifier')

main()
print 'DONE' 