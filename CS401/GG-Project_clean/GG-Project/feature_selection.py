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
    return list.index(min(getAbsValuedList(list)))

def isImportant(weights, threshold = 0.47):
    index = getMinimumValuedWeightIndex(weights)
    if weights[index] > threshold: # Similarity issue is ignored. Working on it.
        return True
    else: return False

def getExtractedWeights(weights):
    return getMinimumValuedWeightIndex(weights), weights.pop(getMinimumValuedWeightIndex(weights))

def selectWeights(weights):
    index, rfe_weights = getExtractedWeights(weights)
    return index, rfe_weights

def eliminate(weights, features):
    index, _ = selectWeights(weights)
    features.pop(index)
    return features

def getTrainedWeights(keyword):
    import paths, PythonVersionHandler, FinalizedRunners, Trainer, ReadyTests
    keyword = keyword.replace(' ', '_')
    folder = paths.joinPath(paths.joinPath(paths.HDFSRootFolder, 'weekAugust'), keyword)
    FinalizedRunners.trainForKeyword(keyword, folder, saving = False)
    return Trainer.lastWeights

def selectFeaturesForKeyword(keyword):
    import Trainer
    featureList = Trainer.featuresList
    weights = getTrainedWeights(keyword)
    while not isImportant(weights):
        featureList = eliminate(weights, featureList)
        Trainer.setFeatureVector(featureList)
        weights = getTrainedWeights(keyword)
    print('Keyword: ' + keyword)
    print('Selected features: ' + featureList)

def selectFeaturesForAllKeywords():
    import  ReadyTests2 as rt
    keywords = rt.get27Keywords()[:23] # todo for all keywords case,
    for keyword in keywords:
        selectFeaturesForKeyword(keyword)