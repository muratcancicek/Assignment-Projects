
class Dataset:
    def __init__(self, vocabulary):
        self.sentences = vocabulary.sentences
        self.label = vocabulary.label
        self.rowNumber = len(self.sentences)
        self.words = sorted([word for word in vocabulary.words])
        self.headers = self.words + ['classlabel']
        self.columnNumber = len(self.headers)
        self.buildMatrix()    
        self.trueRows = self.getRows('classlabel', 1)
        self.trueCount = len(self.trueRows)
        self.falseRows = self.getRows('classlabel', 0)
        self.falseCount = len(self.falseRows)

    def initialiseWordIndices(self):
        self.wordIndices = {}
        for index in range(self.columnNumber):
            self.wordIndices[self.headers[index]] = index

    def buildMatrix(self):
        self.initialiseWordIndices()
        self.table, count = [], 0
        for sentenceIndex in range(len(self.sentences)):
            self.table.append([])
            for word in self.words:
                wordIndex = self.words.index(word)
                self.table[sentenceIndex].append(int(self.words[wordIndex] in self.sentences[sentenceIndex]))
            self.table[sentenceIndex].append(self.sentences[sentenceIndex].classLabel)
            
    def getClassLabels(self):
        return self.getColumn('classlabel')

    def getRow(self, index):
        return self.table[index] 

    def getColumn(self, word, table = []):
        table = self.table if table == [] else table
        return [row[self.wordIndices[word]] for row in table]

    def countWordValue(self, word, value, table = []):
        if word == 'classlabel': return self.trueCount if value else self.falseCount
        return self.getColumn(word, table).count(value)

    def getRows(self, word, value): 
        column = self.getColumn(word)
        return [self.getRow(i) for i in range(len(column)) if column[i] == value]

    def condition(self, row, word, value, conditionalWord, conditionalValue): 
        return row[self.wordIndices[word]] == value and row[self.wordIndices[conditionalWord]] == conditionalValue

    def getConditionalRows(self, word, value, conditionalWord, conditionalValue): 
        return [row for row in self.table if self.condition(row, word, value, conditionalWord, conditionalValue)] 

    def countConditionalValue(self, word, value, conditionalWord, conditionalValue): 
        table = self.trueRows if conditionalValue else self.falseRows
        return self.countWordValue(word, value, table), len(table)

    def saveTo(self, fileName):
        file = open(fileName, 'w') 
        for word in self.words: file.write(word + ',')
        file.write('classlabel\n')
        for rowIndex in range(self.rowNumber):
            counter = 0
            for value in self.getRow(rowIndex):
                file.write(str(value) + (',' if counter < (self.columnNumber - 1) else '\n'))
        file.close()
        print fileName, 'has been saved.\n'