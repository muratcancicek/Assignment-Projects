from FeatureProcesser.GenreAnalyzer import *
from paths import *
import numpy as np
   
genres = {'hipHop': hipHopGenreKeywords(), 'PopRock': popRockGenreKeywords(), 'Classical': classicalGenreKeywords(), 
          'Jazz': jazzGenreKeywords(), 'Pop': popularGenreKeywords()}
#genres = {'hipHop': hipHopGenreKeywords()}
#genres = {'Classical': classicalGenreKeywords()}
#genres = {'POP': popularGenreKeywords()}
#genres = {'PopRock': popRockGenreKeywords()}
#genres = {'Classical': classicalGenreKeywords(), 'PopRock': popRockGenreKeywords()}
#genres = {'hipHop': hipHopGenreKeywords(), 'Classical': classicalGenreKeywords(), 'PopRock': popRockGenreKeywords()}
genreSet =  ['hipHop', 'Jazz', 'PopRock', 'Classical', 'Pop']#list(genres.keys())
 
def getFeaturesLabel(features):
    for genreKey in genreSet:
        if isGenre(features, genres[genreKey]):
           return genreSet.index(genreKey)
    return len(genreSet)-1

def getFeaturesPoint(features):
    point = [] 
    def addFeature(v):
        if isinstance(v, float) or isinstance(v, int):
            point.append(v)
    for k, v in features.items():
        if k == 'rhythm_beats_position':
            addFeature(len(v))
        elif isinstance(v, list):
            if len(v) == 1:
                 addFeature(v[0])
            else:
                for f in v:
                    addFeature(f)
    return point

class LabeledPoint(object):
    def __init__(self, features):
        self.point = getFeaturesPoint(features)#.reshape((1, -1))
        self.label = getFeaturesLabel(features)
        self.genre = genreSet[self.label]
        self.fileName = features['metadata_tags_file_name']

def generateTrainData(featuresList, trainDataRate = 0.7):
    labeledPoints = []
    keywords = []
    for genreKeywords in genreSet: keywords.extend(genres[genreKeywords])
    for features in featuresList:
        if isGenre(features, keywords):
            labeledPoints.append(LabeledPoint(features))
        #    raise IndexError
    classes = {genre: [] for genre in genreSet}
    for point in labeledPoints:
        classes[point.genre].append(point)
    sepIndex = lambda ls: int(len(ls)*trainDataRate)
    trainDataPoints = []
    testDataPoints = []
    trainCounts = {}
    testCounts = {}
    for genre, points in classes.items():
        sepI = sepIndex(points)
        trainCounts[genre] = sepI
        testCounts[genre] = len(points) - sepI
        #print_(genre, len(points), sepI)
        trainDataPoints.extend(points[:sepI])
        testDataPoints.extend(points[sepI:])
    trainData = {'X': np.array([point.point for point in trainDataPoints]), 
                 'Y': [point.label for point in trainDataPoints]}
    testData = {'X': np.array([point.point for point in testDataPoints]), 
                'Y': [point.label for point in testDataPoints]}
    print_('\nLearnable data has been generated successfully by', nowStr())
    print('Summary of the generated data:')
    print('Total Number of instances:   ', len(trainDataPoints+testDataPoints))
    print('Number of training instances:', len(trainDataPoints))
    print('Number of testing instances: ', len(testDataPoints))
    print('The training data rate over the all data: %' + str(trainDataRate*100))
    print('\nNumber of Classes:', len(genreSet))
    print('Classes:', genreSet)
    print('General distribution: ', {genre: len(points) for genre, points in classes.items()})
    print('Training distribution:', trainCounts)
    print('Testing distribution: ', testCounts)
    print()
    return trainData, testData, testCounts