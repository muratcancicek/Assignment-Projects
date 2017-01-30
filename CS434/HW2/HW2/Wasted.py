import numpy as np
import matplotlib.pyplot as plt
#np.seterr(divide='ignore', invalid='ignore', over='ignore')
#execfile('externalSource.py')
#       execfile('HW2.py')
####################  READING FILE  #####################
def readFile(fileName):  
    file = open(fileName, 'rb') 
    images = []
    for rawLine in file: 
        row = str.split(rawLine, ',')
        image = {'matrix': [], 'digitBit': float(row[-1])}
        rawImage = []
        for i in range(len(row[:-1])):
            rawImage.append(float(row[i]))
        rawImage.append(1.0)
        image['matrix'] = np.array(rawImage, dtype='float64')
        images.append(image) 
    return images 

###################  PRINTING IMAGE  ####################
def  drawImage(image):
    plt.imshow(image['matrix'][:-1].reshape(16, 16).transpose(),  cmap='Greys_r')  
    plt.show()
    
###################    HYPOTHESIS    ####################
def h(x, theta):  
    return np.dot(theta.transpose(), x)

####################  LOSS J(theta)  ####################
def j(theta, x, y):
    return -np.sum([( (h(x[i], theta) - y[i]) ** 2 ) / 2 for i in range(len(x))]) / len(x)

def jDerivative(theta, x, y):
    return np.array([ ( y - h(x, theta) ) * x[j] ], dtype='float64')

#######  GRADIENT DESCENT WITH LINEAR REGRESSION  #######
def gradientDescentWithLinearRegression(x, y, alpha, iterationNumber):  
    theta = np.ones_like(x[0], dtype='float64') 
    xTranspose = x.transpose()
    for iteration in range(iterationNumber):  
        for i in range(len(x)):
            loss = h(x[i], theta) - y[i]
            print np.sum(loss ** 2) / (2 * len(x))
            hypothesis = h(x[i], theta)
            gradient = np.dot(x[i].transpose(), loss) / len(x)
            theta = theta - alpha * gradient
    return theta

####################    SIGMOID      ####################
def simgoid(z):
    return 1.0/(1 + np.e ** -z)

def simgoidDerivative(z):
    return simgoid(z)*(1 - simgoid(z))

def g(x, theta):
    return simgoid(np.dot(theta.transpose(), x))

####################      LOSS      #####################
def costForlogisticRegression(x, y, theta):  
    return - (g(x, theta) ** y) * ( (1 - g(x, theta) ) ** (1 - y) ) / len(x)

def loss(gx, y):
    if y == 1:
        return - np.log(gx)
    else:
        return - np.log(1 - gx)
  
####################  COMPACT LOSS  #####################
def compactLoss(x, y, theta): 
    return - y * np.log(g(theta, x)) - ( (1 - y) * np.log(1 - g(theta, x) ) )
    
def lDerivative(x, y, theta):
    return (y - g(theta, x))*x

#################  LEARNING OBJECTIVE  ##################
def L(x, y, theta):
    return np.sum([l(h(x[i], theta), y[i]) for i in range(len(x))]) 

    
######  GRADIENT DESCENT WITH LOGISTIC REGRESSION  ######
def gradientDescentWithLogisticRegression(x, y, alpha, iterationNumber):  
    theta = np.zeros_like(x[0]) 
    for iteration in range(iterationNumber):  
        d = np.zeros_like(x[0]) 
        for i in range(len(x)): 
            hypothesis = g(theta, x[i])
            error = y[i] - hypothesis
            print error 
            d = d + error * x[i]  
        theta = theta + alpha * d
    return theta
####################      MAIN      #####################

trainImages = readFile('usps-4-9-train.csv') 
#drawImage(trainImages[-1]) 
x, y = [], []
for i in trainImages:
    x.append(i['matrix'])
    y.append(i['digitBit'])
x = np.array(x)
alpha = 0.0005
iterationNumber = 1000
theta = np.zeros_like(x[0])
#print costForlogisticRegression(x, y, theta)
#theta = gradientDescentWithLinearRegression(x, y, alpha, iterationNumber) 
theta = gradientDescentWithLogisticRegression(x, y, alpha, iterationNumber) 

print theta
#from sklearn.linear_model import SGDClassifier 
#>>> clf = SGDClassifier(loss="hinge", penalty="l2")
#>>> clf.fit(X, y)
#SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
#       eta0=0.0, fit_intercept=True, l1_ratio=0.15,
#       learning_rate='optimal', loss='hinge', n_iter=5, n_jobs=1,
#       penalty='l2', power_t=0.5, random_state=None, shuffle=True,
#       verbose=0, warm_start=False)
#for i in trainImages:
#    x = i['matrix'] 
#    print h(x, theta), g(x, theta), simgoid(np.dot(theta.transpose(), x))