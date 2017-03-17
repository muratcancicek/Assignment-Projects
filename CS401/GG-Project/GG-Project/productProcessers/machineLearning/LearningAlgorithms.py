from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
#from sknn import MLPClassifier
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from MainSrc.PythonVersionHandler import *
from sklearn import metrics
from sklearn.svm import SVC
from time import time
import numpy as np
  
def bench_estimator(trainData, testData, estimator, name):
    t0 = time()
    X = np.float64(trainData['data'])
    estimator.fit(X, trainData['labels'])
    testX = np.float64(testData['data'])
    labels2 = estimator.predict(testX)
    print('\n%s accuracy: %f in %.2fs\n' % (name, metrics.accuracy_score(labels2, testData['labels']), time() - t0))

def runKmaens(trainData, testData, clusterCount = 100, sampleCount = 700, n_init = 10):
    estimator1 = KMeans(init='k-means++', n_clusters=clusterCount, n_init = n_init)
    bench_estimator(trainData, testData, estimator1, 'k-means++')
    estimator2 = KMeans(init='random', n_clusters=clusterCount, n_init = n_init)
    bench_estimator(trainData, testData, estimator2, 'random')

def runRandomForestClassifier(trainData, testData, featureCount, n_estimators = 100, n_jobs = 1):
    rfc = RandomForestClassifier(n_estimators= n_estimators, n_jobs = n_jobs)
    name = 'RandomForestClassifier on ' + str(featureCount) + ' features with ' + str(n_estimators) + ' estimators'
    bench_estimator(trainData, testData, estimator = rfc, name = name)

def runKNeighborsClassifier(trainData, testData, featureCount, n_neighbors = 3):
    neigh = KNeighborsClassifier(n_neighbors = n_neighbors)
    name = 'KNeighborsClassifier on ' + str(featureCount) + ' features with ' + str(n_neighbors) + ' neighbors' 
    bench_estimator(trainData, testData, estimator = neigh, name = name)

def runSuccessfulAlgorithms(trainData, testData):
    neural_network = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    bench_estimator(trainData, testData, estimator = neural_network, name = 'MLPClassifier')
    svc = SVC()
    bench_estimator(trainData, testData, estimator = svc, name = 'Support Vector Classifier')
    print_('DONE')

def _runPCA(trainData, testData, n_components = 200):
    pca = PCA(n_components=n_components).fit(trainData['data'])
    trainData['data'] = pca.transform(trainData['data'])
    testData['data'] = pca.transform(testData['data'])
    return trainData, testData

def _generatePCAReducedData(trainData, testData, n_components = 200, suffix = ''):
    trainData, testData = _runPCA(trainData, testData, n_components = n_components)
    return trainData, testData