from SarcasmDetectionMethods import *

################################  main  #######################################

def main():
    trainingDataset, testDataset = preprocessData('training_text.txt', 'test_text.txt')
    trainingDataset.saveTo('preprocessed_train.txt') 
    testDataset.saveTo('preprocessed_test.txt') 
    print 'Data is now ready for the classification.\n'
    doClassifications(trainingDataset, testDataset)


################################  running scope  ##############################

print ''
main()
print '\nProgram is terminated successfully.\n' 