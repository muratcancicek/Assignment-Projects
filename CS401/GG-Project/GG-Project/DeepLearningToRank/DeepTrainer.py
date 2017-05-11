from MainSrc.PythonVersionHandler import *
from .DeepDataHandler import *
from sklearn import svm
from paths import *

def printSeparater(c = 3):
    for n in range(c):
        print_('#' * 88)

def scaleTrainData(data):
    #scaler = StandardScaler(withMean=True, withStd=True).fit(features)
    return data

def normalizeTrainData(data):
    # Each sample in data1 will be normalized using $L^2$ norm.
    print_(len(data), 'instances have been normalized by', nowStr())
    return data

def evaluateModelOnData(model, testData, dataName = 'Data', modelName = 'Model'):
    preds = zip(t, model.predict(testData['Y']))
    truePredictionCount = len(filter(lambda vp: vp[0] == vp[1], preds))
    instanceCount = len(testData['Y'])
    accuracy = 100 * truePredictionCount / float(instanceCount)
    print_('\n'+modelName, 'has been evaluated on', dataName, 'by', nowStr())
    print_('The result accuracy is %' + '%.3f\n' % (accuracy))
    return labelsAndPreds

def trainPairWiseData(trainData, dataName = 'Data', modelName = 'Model'):
    model = svm.SVC()#kernel =  'poly', degree = 3) #SVMWithSGD.train(data, iterations=100)
    model.fit(trainData['X'], trainData['Y'])
    print_('\n'+modelName, 'has been trained on', dataName, 'by', nowStr())
    print_('The learned weights:\n' + str(model.weights).replace(',', ', ') + '\n')
    return model

def runTrainingExperiment(trainData, testData, modelName = 'Model', save = True, outputFolder = Day1_iPhone_6_DataFolder):
    trainData['X'] = scaleTrainData(trainData['X'])
    model = trainPairWiseData(trainData, 'trainData', modelName)
    return evaluateModelOnData(model, testData, 'testData', modelName)

def splitData(trainData, rate = 30):
    return trainData[int(rate*len(trainData)/100):], trainData[:int(rate*len(trainData)/100)]

def runExperiment(features, labels, modelName = 'Model'):
    printSeparater(1)
    trainDataFeatures, testDataFeatures = splitData(features)
    trainDataLabels, testDataLabels = splitData(labels)  
    trainData = {'X': trainDataFeatures, 'Y': trainDataLabels} 
    testData = {'X': testDataFeatures, 'Y': testDataLabels} 
    runTrainingExperiment(trainData, testData, modelName = modelName, save = False)
    print_('The experiment for', modelName, 'has been completed by', nowStr())
    printSeparater(1)

def unzipData(trainData):    
    features = list(map(lambda x: x[1], trainData))
    labels = list(map(lambda x: x[0], trainData))
    return features, labels

def featureFilter(features):
    return list(map(lambda x: x[1:4] + x[5:6] + list(xx[7:-2]), features))

def trainPairWiseDataTestKeyword2(keyword):
    printSeparater(2)
    keyword = keyword.replace(' ', '_')
    inputName = 'all_day'
    trainDataFile = joinPath(textTrainDataFolder, inputName + '_' + keyword + '_TrainData')
    trainData = readTrainDataFromPickle(trainDataFile+'.txt')
    features, labels = unzipData(trainData)
    runExperiment(features, labels, modelName = 'ExtendedModel')
    filteredFeatures = featureFilter(features)
    runExperiment(filteredFeatures, labels, modelName = 'FilteredModel')
    printSeparater(2)
    
def rankProducts(products, outputFolder, model = None, modelName = 'Model_v04_4'):
    if model == None:
        modelPath = joinPath(outputFolder, modelName)
        model = SVMModel.load(sc_(), modelPath)
    print_(products.first())
    if isinstance(products.first()[1], list):
        products = products.map(lambda x: (x[0], DenseVector(x[1])))
    products = products.map(lambda x: (-x[1].dot(model.weights), (x[0], x[1])))
    #print_(products.take(2))
    products = products.sortByKey()
    #print_(products.take(2))
    products = products.zipWithIndex().map(lambda x: (x[1] + 1, -x[0][0], x[0][1][0], x[0][1][1]))
    print_(products.count(), 'products have been ranked successfully by', nowStr())
    #print_(products.take(2))
    productsPath = joinPath(outputFolder, 'all_day_iphone_6_journey_rankedProducts')
    saveRDDToHDFS(products, productsPath)
    productsList = products.map(lambda x: x[2]).take(50)
    print_(productsList)
    return products
