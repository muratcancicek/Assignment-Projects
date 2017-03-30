from .MlLibHelper import *

def csvLineToLabeledPoint(line, labelIndex = -1):
    return [np.float64(x) for x in line.split()]

def getSparseVectorsAsLabeledPoints(data, labelIndex = -1):
    sv = lambda features: DenseVector(features)#(len(features), enumerate(features))
    #lbl = lambda l: 1 if l == 1 else -1
    getLabeledPoint = lambda vector: LabeledPoint(vector[labelIndex], sv(vector[:labelIndex]))
    return data.map(getLabeledPoint)

def readCSVDataAsSparseVectors(sc, fileName):
    fileName = joinPath(sparkFolder, fileName)
    data = sc.textFile(fileName).map(csvLineToLabeledPoint)
    data = getSparseVectorsAsLabeledPoints(data)
    return data

def getDataAsListFrom(filename, withDummy = True): 
    x = []
    y = []
    housing_train = open(filename, 'rb') 
    for line in housing_train: 
        row = [float(v) for v in line.split()]
        #r = row[:-1]
        if withDummy:
            r.append(1.0)
        x.append(r)
        #y.append(float(row[-1]))
    #return [x, y] 
    return x

def runHousingTutorialWithFM(sc = None):
    if sc == None: sc = SparkContext()
    trainData = readCSVDataAsDenseVectors(sc, 'housing_train.txt')
    testData = readCSVDataAsDenseVectors(sc, 'housing_test.txt')
    testData.foreach(print_)

    # Build the model
    model = LinearRegressionWithSGD.train(trainData)

    # Evaluating the model on testing data
    evaluateModelOnData(model, testData)
