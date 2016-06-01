from NaiveBayesClassifier import NaiveBayesClassifier
from CommonTools import getAccuracy, getErrorCount
from Vocabulary import Vocabulary, Sentence
from Dataset import Dataset 
import os.path

##########################  READING vocabulary from file  #####################

def readVocabularyFrom(fileName):  
    file = open(fileName, 'rb') 
    vocabulary = Vocabulary(fileName[:-4]) 
    for line in file:  
        if line[0] != '(': continue
        vocabulary.addSentence(Sentence(line)) 
    file.close()
    print 'Vocabulary has been read from', fileName, '\n' 
    return vocabulary

##########################  generating dataset  ###############################

def generateDataset(fileName):
    vocabulary = readVocabularyFrom(fileName) 
    dataset = Dataset(vocabulary) 
    print 'Dataset has been generated from', fileName + '.\n'
    return dataset

##########################  Pre-processing  ###################################

def preprocessData(trainingFileName, testFileName):  
    trainingDataset = generateDataset(trainingFileName)
    testDataset = generateDataset(testFileName)
    print 'Pre-processing is done.\n'
    return trainingDataset, testDataset

##########################  do classifications  ###############################

def doClassifications(trainingDataset, testDataset):
    print '\n#######################################################################'
    print '#######################################################################\n'

    trainingClassifier = NaiveBayesClassifier(trainingDataset)
    print 'The classifier has been trained on', trainingDataset.label + '.'
    doPredictions(trainingClassifier, trainingDataset)
    doPredictions(trainingClassifier, testDataset)
    
    print '\n#######################################################################'
    print '#######################################################################\n'

    testClassifier = NaiveBayesClassifier(testDataset)
    print 'The classifier has been trained on', testDataset.label + '.'

    doPredictions(testClassifier, testDataset)
    doPredictions(testClassifier, trainingDataset)

    
##########################  Predict all instances  ############################

def doPredictions(classifier, dataset): 
    print '\n############################ Predicting... ############################\n'
    print 'The following dataset will be classified:', dataset.label, '\n'
    print 'Predicting now...\n'
    actualClassLabels = dataset.getClassLabels()
    predictedClassLabels = classifier.getPredictedClassLabels(dataset.sentences)
    accuracy = getAccuracy(actualClassLabels, predictedClassLabels)
    print 'Accuracy:', accuracy, '\n'
    print 'Actual sarcastic sentences number:', actualClassLabels.count(1)
    print 'Number of sentences predicted as sarcastic:', predictedClassLabels.count(1)
    print 'Number of mistakes in total:', getErrorCount(actualClassLabels, predictedClassLabels), '\n'