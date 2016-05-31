from SarcasmDetectionMethods import *

################################  main  #######################################

def main():
    trainingDataset, testDataset = preprocessData('training_text.txt', 'test_text.txt')
    saveDataset(trainingDataset,'preprocessed_train.txt') 
    saveDataset(testDataset,'preprocessed_test.txt') 
    print 'Data is now ready for the classification.\n'
    doClassifications(trainingDataset, testDataset)


################################  running scoce  ##############################

print ''
main()
print '\nProgram is terminated successfully.\n' 