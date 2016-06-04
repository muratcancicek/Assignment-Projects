from numpy import *

################################  Predictions  ################################

def yP(w,x):
    sums = [x[i]*w[i] for i in range(len(x))]
    result = 0
    for s in sums:
        result += s
    return result 

################################  LP(P)  ######################################

def lp(x, y, w):
    yp = np.dot(np.transpose(w),x)
    
################################  pmb1  #######################################

def pmb1(size, stepLengthScale, bufferSize):
    w = [ndarray(size)]
    e = 0
    while True:
        b = readNRows(bufferSize)
        stepLength = 1 if e == 0 else float(stepLengthScale)/np.sqrt(e)
        wNext = projectOnto(w, w[e] + stepLength * deltaW * lp(b, w[e]))
        w.append(wNext)
        e += 1
    summ
    return