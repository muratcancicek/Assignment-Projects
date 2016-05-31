from math import log
            
class NaiveBayesClassifier(object):
    def __init__(self, dataset):
        self.dataset = dataset
        self.label = dataset.label
        self.probabilityTrue = self.calculateProbability('classlabel', 1)
        self.probabilityFalse = self.calculateProbability('classlabel', 0)
        self.probabilityTrueScore = log(self.probabilityTrue)
        self.probabilityFalseScore  = log(self.probabilityFalse)

    def calculateConditionalWordProbability(self, word, value, conditionalWord, conditionalValue):
        conditionalCount, count = self.dataset.countConditionalValue(word, value, conditionalWord, conditionalValue)
        return (conditionalCount + 1) / float(count + 2)
        
    def calculateProbability(self, word, value):
        return (self.dataset.countWordValue(word, value) + 1) / float(self.dataset.rowNumber + 2)

    def predict(self, sentence):
        trueScore = self.probabilityTrueScore
        falseScore = self.probabilityFalseScore
        for word in self.dataset.words:
            value = int(word in sentence)
            wordTrueProbability = self.calculateConditionalWordProbability(word, value, 'classlabel', 1)
            wordFalseProbability = self.calculateConditionalWordProbability(word, value, 'classlabel', 0)
            if wordTrueProbability != 0: trueScore += log(wordTrueProbability)
            if wordFalseProbability != 0: falseScore += log(wordFalseProbability)
        for word in sentence:
            if not word in self.dataset.words:
                trueScore += log(self.probabilityFalse)
                falseScore += log(self.probabilityFalse)

        return 1 if trueScore > falseScore else 0

    def getPredictedClassLabels(self, sentences = None):
        if sentences == None: sentences = self.dataset.sentences
        predictions = []
        for sentence in sentences:
            predictions.append(self.predict(sentence))
        return predictions 

    def getActualClassLabels(self):
        return self.dataset.getClassLabels()
