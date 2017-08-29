def getAllWeights():
    import pandas as pd
    weights = pd.read_csv('//PATH OF OUTPUTTABLE5 EXCEL FILE')
    return weights # todo?? that's all ?Weights
    # weights >> [(keyword1), (weights_for_keyword1),...]
    # example: [('besiktas', (1.0, 20.0, 99.0, 100.0, 1.0, 0.0,....)),
    #           ('kolsaati', (1.0, 10.0, 100.0, 230.0, 0.0, 1.0,...)),
    #           ...]

def getWeightsForKeyword(weights, keyword):
    weights_for_keyword = []
    for feature in weights:
        if feature[0] == keyword:
            weights_for_keyword = feature[1]
            break
    return weights_for_keyword

def getWeights(keyword):
    all_weights = getAllWeights()
    weights_for_keyword = getWeightsForKeyword(all_weights, keyword)
    return weights_for_keyword

def getAbsValuedList(list):
    new_list = [abs(number) for number in list]
    return new_list

def getMinimumValuedWeightIndex(list):
    v = min(getAbsValuedList(list)) 
    return list.index(v) if v in list else list.index(-v)

def isImportant(weights, threshold = 0.47):
    index = getMinimumValuedWeightIndex(weights)
    if weights[index] > threshold or -weights[index] > threshold: # Similarity issue is ignored. Working on it.
        return True
    else: return False

def getExtractedWeights(weights):
    i = getMinimumValuedWeightIndex(weights)
    return i, weights.pop(i)

def selectWeights(weights):
    index, rfe_weights = getExtractedWeights(weights)
    return index, rfe_weights

def eliminate(weights, features):
    index, _ = selectWeights(weights)
    removedFeature = features.pop(index)
    return index, features, removedFeature

def getTrainedWeights(keyword):
    import paths, PythonVersionHandler, FinalizedRunners, Trainer, ReadyTests
    keyword = keyword.replace(' ', '_')
    folder = paths.joinPath(paths.joinPath(paths.HDFSRootFolder, 'weekAugust'), keyword)
    #folder = 'C:\\Users\\Muratcan\\Desktop'
    trainData, testData, model, accuracy = FinalizedRunners.trainForKeyword(keyword, folder, saving = False)
    return trainData, testData, list(model.weights), accuracy

def selectFeaturesForKeyword(keyword, threshold = 0.223):
    import Trainer, PythonVersionHandler
    from pyspark.mllib.regression import LabeledPoint
    featureList = Trainer.featuresList[:-2]
    Trainer.setFeatureVector(featureList)
    trainData, testData, weights, accuracy = getTrainedWeights(keyword)
    removedFeatures = []
    accuracies = [accuracy]
    weightsRow = list(weights)
    while (not isImportant(weights, threshold = threshold)) and len(weights) > 1:
        index, featureList, removedFeature = eliminate(weights, featureList)
        removedFeatures.append(removedFeature)
        Trainer.setFeatureVector(featureList)
        def getReducedVector(lp):
            newFeatures = list(lp.features)
            newFeatures.pop(index)
            return LabeledPoint(lp.label, newFeatures)
        trainData = trainData.map(getReducedVector)
        testData = testData.map(getReducedVector)
        model = Trainer.trainPairWiseData(trainData, dataName = 'TrainData')
        accuracy = Trainer.evaluateModelOnData(model, testData, dataName = 'TestData')
        accuracies.append(accuracy)
        weights = list(model.weights)
        weightsRow.append('X')
        weightsRow.extend(weights)
    PythonVersionHandler.print_('Keyword: ' + keyword)
    PythonVersionHandler.print_('Selected features: ' + str(featureList))
    PythonVersionHandler.print_('Following features have reduced by order: ' + str(removedFeatures))
    PythonVersionHandler.print_('Accuracies from each step: ' + str(accuracies))
    row = [keyword]
    row.extend(featureList)
    row.append('X')
    row.extend(removedFeatures)
    row.extend(accuracies)
    return row, weightsRow

def getOutputTable(outputTable):
    s = ''
    for r in outputTable:
        s += str(r).replace('\'', '')[1:-1] + '\n'
    return s

def saveFeaturesTable(outputTable):
    import os, paths
    c = 0
    fileName = paths.joinPath(paths.joinPath('outputs', 'feature_selection'), 'feature_selectionTable' + str(c) + '.csv')
    while os.path.isfile(fileName):
        c += 1
        fileName = paths.joinPath(paths.joinPath('outputs', 'feature_selection'), 'feature_selectionTable' + str(c) + '.csv')
    f = open(fileName, 'w')
    f.write(getOutputTable(outputTable))
    f.close()
    import PythonVersionHandler
    PythonVersionHandler.print_(fileName, 'has been saved successfully by', PythonVersionHandler.nowStr())

def selectFeaturesForAllKeywords():
    outputTable = []
    import PythonVersionHandler, ReadyTests2 as rt
    keywords = rt.get27Keywords()
    for keyword in keywords:
        row, weightsRow = selectFeaturesForKeyword(keyword)
        outputTable.append(row)
        outputTable.append(weightsRow)
    saveFeaturesTable(outputTable)
    PythonVersionHandler.print_(getOutputTable(outputTable))
