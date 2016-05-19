import numpy as np

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
