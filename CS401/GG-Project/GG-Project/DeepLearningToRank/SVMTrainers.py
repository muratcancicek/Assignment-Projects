from MainSrc.PythonVersionHandler import *
from paths import *
from Sparker.Logic.LogicTests import *
from Sparker.Logic.Trainer import *
#trainPairWiseData(data) 
def printSeparater(c = 3):
    for n in range(c):
        print_('#' * 88)

from sklearn import svm

def evaluateModelOnData(model, data, dataName = 'Data', modelName = 'Model'):
    labelsAndPreds = data.map(lambda p: (p.label, model.predict(p.features)))
    truePredictionCount = labelsAndPreds.filter(lambda vp: vp[0] == vp[1]).count()
    instanceCount = data.count()
    accuracy = 100 * truePredictionCount / float(instanceCount)
    print_('\n'+modelName, 'has been evaluated on', dataName, 'by', nowStr())
    print_('The result accuracy is %' + '%.3f\n' % (accuracy))
    return labelsAndPreds

def trainPairWiseData(data, dataName = 'Data', modelName = 'Model', evaluate = True):
    print_('Training with SVMWithSGD...')
    model = SVMWithSGD.train(data, iterations=100)
    print_('\n', modelName, 'has been trained on', dataName, 'by', nowStr())##
    print_('The learned weights:\n' + str(model.weights).replace(',', ', ') + '\n')
    if evaluate:
        evaluateModelOnData(model, data, dataName, modelName)
    return model

def runTrainingExperiment(trainData, testData, modelName = 'Model', save = True, outputFolder = Day1_iPhone_6_DataFolder):
    model = trainPairWiseData(trainData, 'trainData', modelName)
    if save:
        modelPath = joinPath(outputFolder, modelName)
        try:
            model.save(sc_(), modelPath)
        except Py4JJavaError:
            pass
        print_(modelPath, 'has been saved successfully by', nowStr())
    return evaluateModelOnData(model, testData, 'testData', modelName)

def evaluateModelOnDataSK(model, data, dataName = 'Data', modelName = 'Model'):
    labelsAndPreds = data.map(lambda p: (p.label, model.predict(p.features)))
    truePredictionCount = labelsAndPreds.filter(lambda vp: vp[0] == vp[1]).count()
    instanceCount = data.count()
    accuracy = 100 * truePredictionCount / float(instanceCount)
    print_('\n'+modelName, 'has been evaluated on', dataName, 'by', nowStr())
    print_('The result accuracy is %' + '%.3f\n' % (accuracy))
    return labelsAndPreds

def trainPairWiseDataSK(data, dataName = 'Data', modelName = 'Model', evaluate = True):
    model = svm.SVC()#kernel =  'poly', degree = 3) #[:size][:size]
    size = 5000
    X =  data.map(lambda p: p.features).collect()
    Y =  data.map(lambda p: p.label).collect()
    print_('Training with SVC...')
    model.fit(X, Y)
    print_('\n', modelName, 'has been trained on', dataName, 'by', nowStr())##
   # print_('The learned weights:\n' + str(model.coef_).replace(',', ', ') + '\n')
    if evaluate:
        evaluateModelOnDataSK(model, data, dataName, modelName)
    return model

def runTrainingExperimentSK(trainData, testData, modelName = 'Model', save = True, outputFolder = Day1_iPhone_6_DataFolder):
    model = trainPairWiseDataSK(trainData, 'trainData', modelName)
    if save:
        modelPath = joinPath(outputFolder, modelName)
        try:
            model.save(sc_(), modelPath)
        except Py4JJavaError:
            pass
        print_(modelPath, 'has been saved successfully by', nowStr())
    return evaluateModelOnDataSK(model, testData, 'testData', modelName)

from DeepLearningToRank.DeepDataHandler import readTrainDataFromPickle
#from DeepLearningToRank.DeepTrainer import *

def featureFilter(trainData):
    return trainData.map(lambda x: LabeledPoint(x.label, list(x.features[1:4]) + list(x.features[5:6]) + list(x.features[7:-2])))

def runExperiment(trainData, modelName = 'Model', classifier = 'SK'):
    printSeparater(1)
    testData, trainData = trainData.randomSplit(weights=[0.3, 0.7])
    #testData, trainData = trainData[:int(30*len(trainData)/100)], trainData[int(30*len(trainData)/100):]SKSK
    if classifier == 'SK':
        runTrainingExperimentSK(trainData, testData, modelName = modelName, save = False)
    else:
        runTrainingExperiment(trainData, testData, modelName = modelName, save = False)
    print_('The experiment for', modelName, 'has finished by', nowStr())
    
def trainPairWiseDataTestKeyword2(keyword, location = 'HDFS', classifier = 'MLLib'):
    printSeparater(2)
    keyword = keyword.replace(' ', '_')
    inputName = 'all_day'
    if location == 'HDFS':
        outputFolder = joinPath(joinPath(textTrainDataFolder, 'HDFS'), 'Day1_' + keyword + '_Data')
        trainDataFile = joinPath(outputFolder, inputName + '_' + keyword + '_TrainData')
        trainData = readTrainDataFromHDFS(trainDataFile)
    if location == 'oneHot':
        outputFolder = joinPath(joinPath(textTrainDataFolder, 'HDFS'), 'Day1_' + keyword + '_Data')
        trainDataFile = joinPath(outputFolder, inputName + '_' + keyword + '_OneHot_TrainData.txt')
        trainData = readTrainDataFromPickle(trainDataFile)
        trainData = sc_().parallelize(trainData)
        trainData = trainData.map(lambda x: LabeledPoint(x[0], x[1]))
    else:
        trainDataFile = joinPath(textTrainDataFolder, inputName + '_' + keyword + '_TrainData.txt')
        trainData = readTrainDataFromPickle(trainDataFile)
        trainData = sc_().parallelize(trainData)
        trainData = trainData.map(lambda x: LabeledPoint(x[0], x[1]))
    print_(trainData.first())
    print_('Data from', location)
    preprocessing = scaleTrainData# normalizeTrainData#
    trainData = preprocessing(trainData)
    runExperiment(trainData, modelName = 'ExtendedModel', classifier = classifier)
    trainData = featureFilter(trainData)
    runExperiment(trainData, modelName = 'FilteredModel')
    printSeparater(2)



