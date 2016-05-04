from CommonTools import *
import operator
  
##############################  GETTING NEIGHBORS  ############################

def getNeighbors(trainingExamples, newExample, k, lebelIndex = DEFAULT_LABEL_INDEX):
	distances = []
	for i in range(len(trainingExamples)):
		featuresOfNewExample = newExample[lebelIndex+1:]
		featuresOfTrainingExample = trainingExamples[i][lebelIndex+1:] 
		singleDistance = euclideanDistance(featuresOfNewExample, featuresOfTrainingExample)
		distances.append((trainingExamples[i], singleDistance))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for i in range(k):
		neighbors.append(distances[i][0])
	return neighbors 

################################  PREDICTION  #################################

def predict(neighbors, lebelIndex = DEFAULT_LABEL_INDEX):
	lebels = {}
	for i in range(len(neighbors)):
		prediction = neighbors[i][lebelIndex]
		if prediction in lebels:
			lebels[prediction] += 1
		else:
			lebels[prediction] = 1
	sortedVotes = sorted(lebels.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

#############################  KNN ALGORITHM  #################################
def getPredictionsBy_KNN_Algorithm(trainingData, testData, k):
	predictions = []
	for i in range(len(testData)):
		neighbors = getNeighbors(trainingData, testData[i], k)
		prediction = predict(neighbors)
		predictions.append(prediction)
	return predictions