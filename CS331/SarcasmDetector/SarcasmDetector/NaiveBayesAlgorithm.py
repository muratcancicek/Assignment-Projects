import math

##########################  Probability  ######################################

def p(featureColumn, featureValue = 1, conditionColumn = [], conditionValue = 1):
    if conditionColumn == []:
        #return (featureColumn.count(featureValue))/float(len(featureColumn)) # Uniform Dirichlet Priors
        return (featureColumn.count(featureValue) + 1)/float(len(featureColumn) + 2) # Uniform Dirichlet Priors
    else: 
        conditionCount = 0
        for i in range(len(conditionColumn)):
            if featureColumn[i] == featureValue and conditionColumn[i] == conditionValue:
                conditionCount += 1
        return (conditionCount + 1)/float(conditionColumn.count(conditionValue) + 2) # Uniform Dirichlet Priors

##########################  Inference in Naive Bayes  #########################
w = 0
def prob(trainTable, sentence, conditionKey = 'classlabel', conditionValue = 1): 
    n = p(trainTable[conditionKey], featureValue = conditionValue);
    probability = math.log(n) if n != 0 else 0
    for word in sentence[0]:
        if word in trainTable.keys():
            m = p(trainTable[word], conditionColumn = trainTable[conditionKey], conditionValue = conditionValue)
            probability += math.log(m) if m != 0 else 0
        else:
            global w
            w+=1
    return probability 
        
##########################  prediction  #######################################
 
def predict(trainTable, sentence): 
    trueProbability = prob(trainTable, sentence, conditionValue = 1) 
    falseProbability = prob(trainTable, sentence, conditionValue = 0) 
    if trueProbability > falseProbability:
        return 1
    else:
        return 0
    

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