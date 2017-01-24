
def regenerateOutputs(): 
    generateSpecsStatistics()
    preprocessData()
    
def getLearnableData(fileName = 'ProductVector.csv'):
    productVector, labels = readProductVectorCSV(fileName)
    trainData = {'data': [], 'labels': []}
    testData = {'data': [], 'labels': []}
    for index in range(len(productVector)):
        if index % 10 < 7:
            trainData['data'].append(productVector[index])
            trainData['labels'].append(labels[index])
        else:
            testData['data'].append(productVector[index])
            testData['labels'].append(labels[index])
    return trainData, testData

def learnCategories():
    trainData, testData = getLearnableData()
    runKmaens(trainData, testData)
