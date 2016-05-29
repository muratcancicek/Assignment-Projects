from math import log, exp
            
class Table(MyObject):
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary
        self.sentences = vocabulary.sentences 
        self.headers = vocabulary.words.values()
        self.initialiseTable()
        self.buildTable() 
            
    def initialiseHeaders(self):
        classLabelWord = Word('classlabel')
        for sentence in self.sentences:
            if sentence.classLabel == 1:
                classLabelWord.increaseCount()  
        self.headers.sort()
        self.headers.append(classLabelWord)

    def initialiseTable(self):
        self.initialiseHeaders()
        emptyRow = [0] * self.rowNumber()
        self.table = {}
        for word in self.headers:
            word.setFalseCount(self.rowNumber())
            self.table[word.string] = list(emptyRow)

    def buildTable(self):
        rowIndex = 0
        for sentence in self.sentences:
            for word in sentence:
                word.increaseCount()
                self.table[word.string][rowIndex] = 1
            self.table['classlabel'][rowIndex] = sentence.classLabel 
            rowIndex += 1
        
    def getSubTableIndices(self, value):
        return  [i for i in range(self.rowNumber()) if self.table['classlabel'][i] == value]

    def getValueCountOfWord(self, word, value, indices):
        column = self.table[word.string]
        column = [column[i] for i in indices]
        return column.count(value)

    def calculateProbability(self, sentence, value):
        probability = 0
        indices = self.getSubTableIndices(value)
        ind = len(indices)
        for word in self.headers[:-1]:
            if word in sentence:
                #probability += log((self.getValueCountOfWord(word, 1, indices)) / float(len(indices)))
                probability += log((self.getValueCountOfWord(word, 1, indices) + 1) / float(len(indices) + 2))
            else:
                #probability += log((self.getValueCountOfWord(word, 0, indices)) / float(len(indices)))
                probability += log((self.getValueCountOfWord(word, 0, indices) + 1) / float(len(indices) + 2))
        return probability

    def predict(self, sentence):
        classLabel = self.headers[-1] 
        #probabilityTrue = log((classLabel.trueCount) / float(self.rowNumber())) 
        probabilityTrue = log((classLabel.trueCount + 1) / float(self.rowNumber() + 2))
        #probabilityTrue = log((trueCount + 1) / float(self.rowNumber() + 2)) 
        probabilityTrue += self.calculateProbability(sentence, 1)
        probabilityTrue = exp(probabilityTrue)

        #probabilityFalse = log((classLabel.falseCount) / float(self.rowNumber())) 
        probabilityFalse = log((classLabel.falseCount + 1) / float(self.rowNumber() + 2)) 
        #probabilityFalse = log((falseCount + 1) / float(self.rowNumber() + 2)) 
        probabilityFalse += self.calculateProbability(sentence, 0)
        probabilityFalse = exp(probabilityFalse)
        return 1 if probabilityTrue > probabilityFalse else 0

    def getPredictedClassLabels(self, sentences = None):
        if sentences == None: sentences = self.sentences
        predictions = []
        for sentence in sentences:
            predictions.append(self.predict(sentence))
        return predictions 

    def getClassLabels(self):
        return self.table[self.headers[-1].string]

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
