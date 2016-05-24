
##########################  READING FILE AS LINES #############################

def readTestData(fileName):  
    file = open(fileName, 'rb') 
    [n, m] = file.readline()[:-1].split(' ')
    n, m = int(n), int(m)
    file.readline()
    transitionFunctions = [] 
    for i in range(m): 
        transitionFunction = []
        for j in range(n):
            row = file.readline()[:-1].split('    ')
            transitionFunction.append([float(x) for x in row])
        transitionFunctions.append(transitionFunction)
        file.readline()
    rewards = [float(x) for x in file.readline()[:-1].split('    ')]
    return {'stateNumber': m, 'actionNumber': n, 'transitionFunctions': transitionFunctions, 'rewards': rewards}