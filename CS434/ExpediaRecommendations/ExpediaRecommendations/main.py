from KaggleTutorial import * 
from script import *
from myScript import *
#    execfile('main.py')

################################  main  #######################################

def main():
    #doDownsampling(count = 5000000)
    #t1, t2 = readDownsampledDataAsPanda()
    #accuracy, t2, full_preds = predictBasedOnTopClusters()
    #makeAKaggleSubmissionFile(t2, full_preds)
    #preds = run_my_solution('selectedTrain.csv', 'selectedTest.csv') 
    t2 = pd.read_csv('selectedTest.csv')
    preds = pd.read_csv('submission_2016-05-18-02-03.csv')
    predictions = []
    for p in preds['hotel_cluster']:
        p  = p.split()
        predictions.append([int(i) for i in p])
    t = t2['hotel_cluster'].tolist()
    actuals = [[l] for l in t]
    accuracy = ap.mapk(actuals, predictions, k=5)
    print 'Accuracy:', accuracy
    
################################  running scope  ##############################

print ''
main()
print '\nProgram is terminated successfully.\n' 