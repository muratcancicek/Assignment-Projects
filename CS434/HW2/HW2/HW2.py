import numpy as np
import matplotlib.pyplot as plt 

np.seterr(divide='ignore', invalid='ignore', over='ignore')
#execfile('externalSource.py')
#       
####################  READING FILE  #####################
def readFile(fileName):  
    file = open(fileName, 'rb') 
    xs, ys = [], []
    for rawLine in file: 
        rawLine = rawLine.decode('utf-8')
        row = rawLine.split(',') 
        x = []
        for i in range(len(row[:-1])):
            x.append(float(row[i]))
        x.append(1.0)
        xs.append(np.array(x, dtype='float64'))
        ys.append(float(row[-1])) 
    return [xs, ys] 

###################  PRINTING IMAGE  ####################
def  drawImage(image):
    plt.imshow(image.reshape(16, 16).transpose(),  cmap='Greys_r')  
    plt.show()
    
###################    HYPOTHESIS    ####################
def g(x, w):
    return 1.0/(1 + np.e ** -(np.dot(w.transpose(), x)) )

####################      LOSS      ##################### 
def loss(hypothesis, y):
    if y == 1:
        return - np.log2(hypothesis)
    else:
        return - np.log2(1 - hypothesis)
  
####################  COMPACT LOSS  #####################
def compactLoss(hypothesis, y): 
    return - y * np.log(hypothesis) - ( (1 - y) * np.log(1 - hypothesis ) )
    
def lDerivative(hypothesis, y):
    return (y - hypothesis)*x

#################  LEARNING OBJECTIVE  ##################
def L(x, y, w):
    return np.sum([abs(g(x[i], w) - y[i]) for i in range(len(x))]) 

######  GRADIENT DESCENT WITH LOGISTIC REGRESSION  ######
def gradientDescentWithLR(x, y, alpha, iterationNumber):  
    w = np.zeros_like(x[0])  
    for iteration in range(iterationNumber):  
        d = np.zeros_like(x[0]) 
        for i in range(len(x)): 
            hypothesis = g(x[i], w)
            error = y[i] - hypothesis 
            d = d + error * x[i]  
        w = w + alpha * d
    return w

####  GRADIENT DESCENT WITH LOGISTIC REGRESSION L2  ######
def gradientDescentWithLRL2(x, y, alpha, lmbda, iterationNumber):  
    w = np.zeros_like(x[0])  
    for iteration in range(iterationNumber): 
        d = np.zeros_like(x[0]) 
        for i in range(len(x)): 
            hypothesis = g(w, x[i])
            error = y[i] - hypothesis
            d = d + error * x[i] +( (lmbda*1.0) * d  )
        normW = np.linalg.norm(w) 
        w = w + alpha * ( d  ) 
    return w

####################      TEST      #####################
def test(x, y, w): 
    return [g(x[i], w) for i in range(len(x))]

def experienceOn(x, y, experienceCount, initialIterationNumber, initialAlpha, onAlpha):
    iterationNumber = initialIterationNumber
    alpha = initialAlpha 
    experience = [[], [], []]
    for e in range(experienceCount): 
        w = gradientDescentWithLR(x, y, alpha, iterationNumber)
        experience[0].append(w) 
        if onAlpha:
            alpha *= 0.05
            experience[1].append(alpha)
        else:
            iterationNumber *= 10
            experience[1].append(iterationNumber)
        LOSS = L(x, y, w)
        experience[2].append(LOSS)  
        if LOSS == 0: return experience
    return experience
 
def experience(x, y, experienceCount, initialIterationNumber, initialAlpha): 
    iterationNumber = initialIterationNumber
    mainExperience = [[], [], [], []]
    for e in range(experienceCount):
        subExperience = experienceOn(x, y, experienceCount, iterationNumber, initialAlpha, True)
        minLOSS = min(subExperience[2])
        optimalAlpha = subExperience[1][subExperience[2].index(minLOSS)] 
        w = subExperience[0][subExperience[2].index(minLOSS)]
        mainExperience[0].append(w) 
        mainExperience[1].append(iterationNumber)
        mainExperience[2].append(optimalAlpha)
        mainExperience[3].append(minLOSS) 
        plotResults(w, optimalAlpha, iterationNumber, 'exp' + str(e + 1))
        iterationNumber *= 10
        if minLOSS == 0: return mainExperience
    return mainExperience

def getOptimalParameters(x, y):
    mainExperience = experience(x, y, 5, 1, 1) 
    minError = min(mainExperience[3])
    bestExperienceIndex = mainExperience[3].index(minError)
    optimalW = mainExperience[0][bestExperienceIndex] 
    optimalAlpha = mainExperience[2][bestExperienceIndex] 
    optimalIterationNumber = mainExperience[1][bestExperienceIndex]  
    return optimalW, optimalIterationNumber, optimalAlpha

def removezeros(number):
    number = '%.15f' % number
    while len(number):
        if number[::-1][0] == '0':
            number = number[:-1]
        elif number[::-1][0] == '.':
            number = number[:-1]
            break
        else:
            break
    return number

def plotResultsWith(filename, w, fig, plot, alpha, iterationNumber, lmbda = -1):  
    [x, y] = readFile(filename)  
    hypothesises = test(x, y, w)   
    ax = fig.add_subplot(plot)
    plot1 = ax.plot(y, '.g', markersize=20)
    plot2 = ax.plot(hypothesises, '.r',markersize=6)
    plt.xlim(0, len(hypothesises)+50)
    ymin, ymax = plt.ylim()
    plt.ylim(ymin-0.2, ymax+0.2)  
    plt.title(filename[:-4])
    plt.xlabel('Instances')
    plt.ylabel('Is digit 9?')
    if lmbda == -1:
        ax.legend(["Actual Data", "hypothesises with \na = {0} iN = {1}".format(removezeros(alpha), iterationNumber)], loc='best', numpoints=1)
    else:
        ax.legend(["Actual Data", "hypothesises with \nLamda = {0}".format(removezeros(lmbda))], loc='best', numpoints=1)
    fig.tight_layout()
    return hypothesises 

def plotResults(w, alpha, iterationNumber, filename, lmbda = -1):  
    fig = plt.figure() 
    plotResultsWith('usps-4-9-train.csv', w, fig, 211, alpha, iterationNumber, lmbda)
    plotResultsWith('usps-4-9-test.csv', w, fig, 212, alpha, iterationNumber, lmbda)
    fig.savefig(filename, bbox_inches='tight')
    plt.close()
    #plt.show() 

def experienceLambdaValues(minPower, maxPower, optimalAlpha, optimalIterationNumber): 
    experience = [[], [], []]
    for lambdaPower in range(minPower, maxPower): 
        lmbda = 10 ** lambdaPower  
        w = gradientDescentWithLRL2(x, y, optimalAlpha, lmbda, optimalIterationNumber)
        experience[0].append(w) 
        experience[1].append(lmbda)
        LOSS = L(x, y, w)
        experience[2].append(LOSS)  
        plotResults(w, optimalAlpha, optimalIterationNumber, 'expWithLambda' + str(lambdaPower-minPower+1), lmbda)
        #if LOSS == 0: return experience
    0
####################      MAIN      #####################

[x, y] = readFile('usps-4-9-train.csv')  
optimalIterationNumber, optimalAlpha = 1000, 0.05
#runningExperiments = False # True # Takes time and return 1000, 0.05 for usps-4-9-train.csv
#if runningExperiments: 
#    optimalW, optimalIterationNumber, optimalAlpha = getOptimalParameters(x, y)
#    print optimalIterationNumber, optimalAlpha
#else: 
optimalW = gradientDescentWithLRL2(x, y, optimalAlpha, 0.0001, optimalIterationNumber)  
print('OPTIMAL W:')
print(optimalW.shape)
print('CHANGE THE CODE FOR THE PLOTS')

[tx, ty] = readFile('usps-4-9-test.csv') 
testP = test(tx, ty, optimalW)

a = 1.0 
for i in range(len(testP)):
    if testP[i] == ty[i]: a += 1

print(' accuracy', a/len(testP))
#plotResults(optimalW)  
#experienceLambdaValues(-5, 2, optimalAlpha, optimalIterationNumber)