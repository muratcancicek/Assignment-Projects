import math
import numpy as np
from numpy import matrix as npm 

####################  READING DATA  ##################### 
feature_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'Dummy']
def getDataAsDict():
    data = {}
    target = []
    for key in feature_names[:-1]:
        data[key] = []
    housing_train = open('housing_train.txt', 'rb') 
    for line in housing_train: 
        row = str.split(line)
        for index in range(len(data)):
            data[feature_names[index]].append(row[index])
        target.append(row[-1])
    return {'data' : data, 'feature_names' : feature_names[:-1], 'target' : target}

def getDataAsListFrom(filename, withDummy = True): 
    x = []
    y = []
    housing_train = open(filename, 'rb') 
    for line in housing_train: 
        row = [float(v) for v in line.split()]
        r = row[:-1]
        if withDummy:
            r.append(1.0)
        x.append(r)
        y.append(float(row[-1]))
    return [x, y] 

####################    TRAINING    ##################### 
def getWeightVector(withDummy = True, variant = 1, lmbda = 1): 
    [x, y] = getDataAsListFrom('housing_train.txt', withDummy)
    x = np.matrix(x)
    y = np.matrix(y).T 
    xT = x.T
    xTx = xT.dot(x)
    if variant == 1:
        xTxI = xTx.I
    else:
        xTxI = (xTx + lmbda*np.matrix(np.identity(len(xTx)), copy = False)).I
    xTxIxT = xTxI.dot(xT) 
    return xTxIxT.dot(y)

def getWeightList(withDummy = True, variant = 1, lmbda = 1):
    w = getWeightVector(withDummy, variant, lmbda).tolist()
    wl = []
    for c in w:
        wl.append(c[0])
    return wl

################### W VECTOR PRINTER #################### 
def spaces(n):  
    if n > 1:
        digits = int(math.log10(n))+1
    elif n >= 0 and n < 1:
        digits = 1
    elif n > -1 and n < 0:
        digits = 2
    else:
        digits = int(math.log10(-n))+2 
    s = '     '
    return s[digits:]

def printWeightListAsTable(w): 
    print("\n{0:10}{1}{2}\n".format('Features' , spaces(-10), 'Estimated Coefficients'))
    for i in range(len(w)): 
        print("{0:10}{1}{2}".format(feature_names[i], spaces(w[i]), w[i]))
    
#################### SSE CALCULATOR ##################### 
def sseCalculator(x, y, w):
    SSE = 0
    for i in range(len(x)):
        SSE += (y[i] - np.sum([x[i][j]*w[j] for j in range(len(x[i]))]))**2
    return SSE

################## REPORTING W & SSE ####################
def reportW(withDummy = True, wVariant = 1, lmbda = 1):
    if wVariant != 1:
        print('\nWeight Vector [2nd variant] with lambda =', lmbda)
    elif withDummy:
        print('\nWeight Vector with dummy variable')
    else:
        print('\nWeight Vector WITHOUT dummy variable')
    w = getWeightList(withDummy, wVariant, lmbda)
    printWeightListAsTable(w)  
    return w

def reportSSE(withDummy = True, w = None, wVariant = 1, lmbda = 1):
    if w == None:
        w = getWeightList(withDummy, wVariant, lmbda)
    [x, y] = getDataAsListFrom('housing_test.txt', withDummy) 
    SSE = sseCalculator(x, y, w)
    if wVariant != 1:
        print('\nthe SSE on housing_test:', SSE, ' with lambda =', lmbda)
    else:
        print('\nthe SSE on housing_test:', SSE)
    return SSE

def reportWnSSE(withDummy = True, wVariant = 1, lmbda = 1):
    w = reportW(withDummy, wVariant, lmbda)
    sse = reportSSE(withDummy, w, wVariant, lmbda)
    print('#########################################################\n')
    return sse

####################      MAIN      ##################### 
print('\n################# CS434 HW1 by cicekm ###################')

reportWnSSE()
reportWnSSE(withDummy = False)
reportWnSSE(wVariant = 2) 
reportWnSSE(wVariant = 2, lmbda = 0.21) 
lmbdas = [0.01, 0.05, 0.1, 0.21, 0.5, 1, 5] 
sses = [] 
for l in lmbdas:
    sses.append(reportSSE(wVariant = 2, lmbda = l))

    #   FOR OBSERVING WEIGHT VALUES WHEN LAMBDA GETS BIGGER 
#lmbdas = [] 
#for l in range(0, 1001, 200): 
#    lmbdas.append(l)
#    sses.append(reportWnSSE(wVariant = 2, lmbda = l)) 

    #   FOR PLOTTING
#import matplotlib.pyplot as pyplot
#pyplot.plot(lmbdas, sses) 
#pyplot.show()