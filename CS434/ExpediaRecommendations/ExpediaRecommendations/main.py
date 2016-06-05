from KaggleTutorial import * 
from CommonTools import *
from Algorithms import *
from myScript import *
import pandas as pd

#    execfile('main.py')

################################  main  #######################################

def main():
    indices = [i for i in range(10)]
    #runAlgorithm(logisticRegressionMethod, 'fakeTrain2.csv', 'fakeTest2.csv', 'sampledSubmissionBinary.csv')
    runAlgorithm(linearRegressionMethod, 'sampledTrain6.csv', 'sampledTest6.csv', 'sampledSubmissionBinary.csv', indices, indices, True)
    #runAlgorithm(logisticRegressionMethod, 'sampledTrain4.csv', 'sampledTest4.csv', 'sampledSubmissionBinary.csv')
    
    #runAlgorithm(randomForestMethod, 'sampledTrain.csv', 'sampledTest.csv', 'sampledSubmission.csv')
    #runAlgorithm(randomForestMethod, 'fakeTrain.csv', 'fakeTest.csv', 'fakedSampledSubmission.csv'h
    #writeNewTrain('train.csv', 'sampledTrian3.csv', 'sampledTest3.csv')

    #trainIndices = [0, 5, 7, 16, 20, 21, 22, 23]
    #testIndices = [1, 6, 8, 17, 19, 20, 21]
    #runAlgorithm(randomForestMethod, 'sampledTrain.csv', 'sampledTest.csv', 'sampledSubmission.csv')
 
    #runAlgorithm(linearRegressionMethod, 'sampledTrain2.csv', 'sampledTest2.csv', 'sampledSubmission2.csv')
  
def hideComments():
    #predictions = np.arange(5).reshape(5, 1)
    #predictedRankings = [[int(v), int(v)+1, int(v)-1, int(v)+2, int(v)-2] for v in predictions]

    #linearRegressionMethod('fakeTrain.csv', 'fakeTest.csv', trainIndices, testIndices)
    #linearRegressionMethod('trian.csv', 'test.csv', trainIndices, testIndices)
    #makeAKaggleSubmissionFile(

    #linearRegressionMethod('sampledTrian.csv', 'sampledTest.csv')

    #writeNewTrain('train.csv', 'sampledTrian2.csv', 'sampledTest2.csv')

    #Columns = getColumnDict()
    #counts = valueCounter(Columns['user_id'], 'train.csv')
    #for value in sorted(counts.keys()):
    #    printSave(value, counts[value])

    #data = pd.read_csv('train.csv', dtype = getDType())
    #printSave(data['hotel_cluster'].value_counts())
    #doDownsampling(count = 5000000)
    #t1, t2 = readDownsampledDataAsPanda()
    #accuracy, t2, full_preds = predictBasedOnTopClusters()
    #preds = run_my_solution('selectedTrain.csv', 'selectedTest.csv') 
    #makeAKaggleSubmissionFile(t2, full_preds)
    a
    
################################  running scope  ##############################


printSave('\n###############################################################################\n')
printSave('\nProgram starts...\n')
main()
printSave('\nProgram is terminated successfully.\n')
printSave('\n###############################################################################\n')