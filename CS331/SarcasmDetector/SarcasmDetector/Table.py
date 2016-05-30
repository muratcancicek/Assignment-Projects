from math import log, exp
from NaiveBayesAlgorithm import *
from Vocabulary import *
            
class Table(MyObject):
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary
        self.sentences = vocabulary.sentences 
        self.headers = vocabulary.words.values()
        self.initialiseTable()
        self.buildTable() 
        self.classLabels = self.getClassLabels()
        self.trueProbability = p(self.classLabels, 1)
        self.falseProbability = p(self.classLabels, 0)
            
    def initialiseClassLabels(self):
        classLabelWord = Word('classlabel')
        for sentence in self.sentences:
            if sentence.classLabel == 1:
                classLabelWord.increaseCount()  
        self.headers.sort()
        self.headers.append(classLabelWord)

    def initialiseTable(self):
        self.initialiseClassLabels()
        emptyRow = [0] * self.rowNumber()
        self.table = {}
        for word in self.headers:
            word.setFalseCount(self.rowNumber())
            self.table[word.string] = list(emptyRow)

    def initialiseClusterIndices(self):
        self.positiveClusterIndices, self.negativeClusterIndices = [], []
        for i in range(self.rowNumber()):
            if self.table['classlabel'][i] == 1:
                self.positiveClusterIndices.append(i)
            else:
                self.negativeClusterIndices.append(i)

    def buildTable(self):
        rowIndex = 0
        for sentence in self.sentences:
            for word in sentence:
                word.increaseCount()
                self.table[word.string][rowIndex] = 1
            self.table['classlabel'][rowIndex] = sentence.classLabel 
            rowIndex += 1
        self.initialiseClusterIndices()

    def getValueCountOfWord(self, word, value, indices):
        column = self.table[word.string]
        column = [column[i] for i in indices]
        return column.count(value)

    def getFilteredColumn(self, word, conditionValue):
        filteredIndices = self.positiveClusterIndices if conditionValue == 1 else self.negativeClusterIndices
        return [self.table[word][i] for i in filteredIndices]

    def calculateProbability(self, sentence, conditionValue):
        probability = log(self.trueProbability if conditionValue else self.falseProbability)
        count = 0
        for word in self.headers[:-1]:
            wordCondition = 0
            if word in sentence.words:
                wordCondition = 1
                count += 1  
            filteredColumn = self.getFilteredColumn(word.string, conditionValue)
            pro = p(filteredColumn, wordCondition)
            #if wordCondition == 1:
            #    print conditionValue, wordCondition, pro
            if pro:
                probability += log(pro) # if prob != 0 else 0
            #probability += log(p(self.table[word][i], wordCondition, self.getClassLabels(), conditionValue))
        return exp(probability) #probability #

    def predict(self, sentence):
        probabilityTrue = self.calculateProbability(sentence, 1)
        probabilityFalse = self.calculateProbability(sentence, 0)
        #difference = int(probabilityTrue - probabilityFalse) 
        #print difference
        #if abs(difference) > 17:
        #    return 1
        return 1 if probabilityTrue > probabilityFalse else 0

    def getPredictedClassLabels(self, sentences = None):
        if sentences == None: sentences = self.sentences
        predictions = []
        for sentence in sentences:
            predictions.append(self.predict(sentence))
        return predictions 

    def getClassLabels(self):
        return self.table['classlabel']

    def writeCell(self, file, value, columnIndex):
        file.write(str(value))
        if columnIndex < self.columnNumber()-1:
            file.write(',')
        else:
            file.write('\n')

    def saveTable(self, fileName):
        file = open(fileName, 'w') 
        # headers 
        for columnIndex in range(self.columnNumber()):
            self.writeCell(file, self.headers[columnIndex].string, columnIndex)
        # values 
        for rowIndex in range(self.rowNumber()):
            columnIndex = 0
            for word in self.headers:
                self.writeCell(file, self.table[word.string][rowIndex], columnIndex)
                columnIndex += 1
        file.close()
        print fileName, 'has been saved.\n'

    def columnNumber(self):
        return len(self.headers)

    def rowNumber(self):
        return len(self.sentences) 
