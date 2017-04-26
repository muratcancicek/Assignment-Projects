from FeatureProcesser.FeatureVectorGenerater import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn import svm
from paths import *

def experienceSVMTrain(trainData, testData, testCounts, classifierNumber = 0):
    if classifierNumber == 0:
        classifier = OneVsRestClassifier(svm.SVC())
        algorithmName = 'OneVsRestClassifier'
    elif classifierNumber == 1:
        classifier = svm.SVC()
        algorithmName = 'SupportVectorClassifier'
    elif classifierNumber == 2:
        classifier = RandomForestClassifier(n_estimators= 1000, n_jobs = 4)
        algorithmName = 'RandomForestClassifier'
    else:
        classifier = KNeighborsClassifier(n_neighbors=3)
        algorithmName = 'KNeighborsClassifier'
    print_(algorithmName, 'has been started to train the data by', nowStr())
    classifier.fit(preprocessing.scale(trainData['X']), trainData['Y'])
    print_(algorithmName, 'has been started to predict the test data by', nowStr())
    predictions = classifier.predict(preprocessing.scale(testData['X']))
    truePositives = 0
    truePositiveCounts = {genre: 0 for genre in genreSet}
    predictionCount = len(predictions)
    for i in range(predictionCount):
        if predictions[i] == testData['Y'][i]:
            truePositives += 1
            truePositiveCounts[genreSet[testData['Y'][i]]] += 1
    print_(algorithmName, 'Experiment has been finished by', nowStr())
    print_('\nGeneral Test Accuracy = %.3f' % (truePositives / float(predictionCount)))
    print('\nTotal Number of predictions:', predictionCount)
    print('Number of true predictions:  ', truePositives)
    print('Number of false predictions: ', predictionCount-truePositives)
    print_('\nTesting distribution:            ', {genre: testCounts[genre] for genre in genreSet})
    print_('Distribution of true predictions: ', truePositiveCounts)
    falseNegativeCounts = {genre: testCounts[genre]-truePositiveCounts[genre] for genre in genreSet}
    print_('Distribution of false predictions:', falseNegativeCounts, '\n')