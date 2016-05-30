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