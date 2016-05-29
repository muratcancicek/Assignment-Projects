from CommonTools import *
from SarcasmDetectionMethods import *
from Vocabulary import Table

#    execfile('SarcasmDetector.py') 

################################  main  #######################################

def main():
    trainVocabulary = readVocabularyFrom('training_text.txt')
    trainTable = Table(trainVocabulary)

    testVocabulary = readVocabularyFrom('test_text.txt')
    testTable = Table(testVocabulary)

    actualClassLabels = testTable.getClassLabels()
    predictedClassLabels = trainTable.getPredictedClassLabels(testTable.sentences)
    accuracy = getAccuracy(actualClassLabels, predictedClassLabels)
    print 'Accuracy:', accuracy
    print actualClassLabels.count(1), predictedClassLabels.count(1)
    print getErrorCount(actualClassLabels, predictedClassLabels)
    #table.saveTable('new_preprocessed_train.txt') 
    #data = getTrainedData(saveOutputs = False)
    #actualClassLabels = data['test']['table']['classlabel']
    #predictedClassLabels = doPredictions(data)
    #accuracy = getAccuracy(actualClassLabels, predictedClassLabels)
    #print 'Accuracy:', accuracy
    #print actualClassLabels.count(1), predictedClassLabels.count(1)
    #print getErrorCount(actualClassLabels, predictedClassLabels)


################################  running scoce  ##############################

main()
print '\nProgram is terminated successfully.\n' 