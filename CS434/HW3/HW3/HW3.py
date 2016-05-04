from CommonTools import *
from KNN_Algorithm import *

DEFAULT_LABEL_INDEX = 0  

##############################  GETTING NEIGHBORS  ############################

def testKNN_Algorithm(startingK, endingK = -1, step = 2):
    trainingData = readDataset('knn_train.csv')
    testData = readDataset('knn_test.csv')
    if endingK == -1:
        endingK = startingK
    k = startingK
    results = []
    print 'In', len(testData), 'examples:' 
    while k <= endingK:
        if k%2 == 0: k += 1 # Avoiding ties 
        predictions = getPredictionsBy_KNN_Algorithm(trainingData, testData, k)
        errorCount = getErrorCount(testData, predictions)
        accuracy = (100-percentage(testData, errorCount))
        print '\tFor k =', str(k)+':', '# of mistakes =', errorCount, '| Accuracy =', accuracy
        results.append([k, errorCount, accuracy])
        k += step
    return results
    
################################  MAIN FUNCTION  ##############################

def main():
    results = testKNN_Algorithm(1, 15)

    
################################  RUNNING SCOPE  ##############################

main()