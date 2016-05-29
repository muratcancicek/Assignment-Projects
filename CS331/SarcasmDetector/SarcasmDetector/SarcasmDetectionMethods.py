from CommonTools import *
from NaiveBayesAlgorithm import *
from Vocabulary import Vocabulary, Sentence
import string 

##########################  READING raw sentences  ############################

def readRawSentencesFrom(fileName):  
    file = open(fileName, 'rb') 
    rawSentences = []
    for line in file:  
        if line[0] != '(': continue
        sentence, classLabel = line[2:-4], int(line[-3])
        rawSentences.append([sentence, classLabel])
    file.close()
    print fileName, 'has been read.\n'
    return rawSentences

##########################  READING vocabulary from file  #####################

def readVocabularyFrom(fileName):  
    file = open(fileName, 'rb') 
    vocabulary = Vocabulary() 
    for line in file:  
        if line[0] != '(': continue
        sentence = Sentence(line)
        vocabulary.addSentence(sentence) 
    file.close()
    print 'Vocabulary has been read from', fileName, '\n' 
    return vocabulary

##########################  forming vocabulary and sentences  #################

def formVocabulary(rawSentences):
    vocabulary, sentences = [], []
    for i in range(len(rawSentences)):
        rawSentences[i][0] = rawSentences[i][0].translate(string.maketrans("",""), string.punctuation)
        rawSentences[i][0] = rawSentences[i][0].split()
        vocabulary.extend(rawSentences[i][0]) 
        sentences.append(rawSentences[i])
    for word in vocabulary:
        count = vocabulary.count(word)
        if count <= 5:
            while word in vocabulary:
                index = vocabulary.index(word)
                vocabulary = vocabulary[:index] + vocabulary[(index+1):]
    vocabulary = list(set(vocabulary))
    vocabulary = sorted(vocabulary, key=lambda s: s.lower())
    count = vocabulary.count(vocabulary[0])
    print 'Vocabulary and the sentences have been formed.\n' 
    return vocabulary, sentences

##########################  generating table  #################################

def generateTable(vocabulary, sentences):
    table = {}
    for word in vocabulary:
        table[word] = [0 for i in range(len(sentences))]
    table['classlabel'] = [0 for i in range(len(sentences))]
    for i in range(len(sentences)):
        for word in sentences[i][0]:
            if word in vocabulary:
                table[word][i] = 1
            if sentences[i][1] == 1:
                table['classlabel'][i] = sentences[i][1]
    print 'Table has been generated.\n' 
    return table

##########################  saving table  #####################################

def saveTable(table, fileName):
    file = open(fileName, 'w') 
    keys = table.keys()
    #keys = sorted(keys, key=lambda s: s.lower())
    # headers 
    for column in range(len(keys)):
        file.write(keys[column])
        if column < len(keys)-1:
            file.write(',')
        else:
            file.write('\n')
    # values 
    for row in range(len(table[keys[0]])):
        column = 0
        for key in keys:
            file.write(str(table[key][row]))
            if column < len(keys)-1:
                file.write(',')
            column += 1
        file.write('\n')
    file.close()
    print fileName, 'has been saved.\n'

##########################  Pre-processing  ###################################

def preprocessData(inputFileName, outputFileName, saveOutput = True):  
    rawSentences = readRawSentencesFrom(inputFileName)
    vocabulary, sentences = formVocabulary(rawSentences)
    table = generateTable(vocabulary, sentences)
    if saveOutput:
        saveTable(table, outputFileName)
    print 'Pre-processing is done.\n'
    return sentences, vocabulary, table

##########################  Pre-processing for assignment  ####################

def getTrainedData(saveOutputs = True):
    data = {}
    sentences, vocabulary, table = preprocessData('training_text.txt', 'preprocessed_training.txt', saveOutputs)
    data['train'] = {'sentences': sentences, 'vocabulary': vocabulary, 'table': table}
    sentences, vocabulary, table = preprocessData('test_text.txt', 'preprocessed_test.txt', saveOutputs)
    data['test'] = {'sentences': sentences, 'vocabulary': vocabulary, 'table': table}
    print 'Data is now ready for the classification.\n' 
    return data

##########################  Predict all instances  ############################

def doPredictions(trainedData, trainingDataKey = 'train', testingDataKey = 'test'): 
    trainedTable = trainedData[trainingDataKey]['table']
    testSentences = trainedData[testingDataKey]['sentences']
    predictedClassLabels = []
    for sentence in testSentences:
        predictedClassLabels.append(predict(trainedTable, sentence))
    print 'Predictions has been generated.\n'
    print w
    return predictedClassLabels