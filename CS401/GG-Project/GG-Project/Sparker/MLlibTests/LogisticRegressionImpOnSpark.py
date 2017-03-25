from .MlLibHelper import *

def fm_gradient_sgd_trick(X, y, W, regParam):
    """
    Computes the gradient for one instance using Rendle FM paper (2010) trick (linear time computation)
    """
    xa = np.array([X])
    x_matrix = xa.T.dot(xa)

    VX =  xa.dot(W)
    VX_square = (xa*xa).dot(W*W)
    phi = 0.5*(VX*VX - VX_square).sum()

    expnyt = np.exp(-y*phi)
    np.fill_diagonal(x_matrix,0)
    result = (-y*expnyt)/(1+expnyt)* (np.dot(x_matrix, W))
    return regParam*W + result

    
def subSGD(train_X, train_Y, w, iter_sgd, alpha, regParam):
    N = len(train_X)
    wsub = w
    G=np.ones(w.shape)
    for i in range(iter_sgd):
        np.random.seed(int(time.time())) 
        random_idx_list = np.random.permutation(N)
        for j in range(N):
            idx = random_idx_list[j]
            X = train_X[idx]
            y = train_Y[idx]
            grads = fm_gradient_sgd_trick(X, y, wsub, regParam)
            G += grads * grads
            wsub -= alpha * grads / np.sqrt(G)
    return wsub
# Train with non-parallel sgd

def trainFM_parallel_sgd(sc, data, iterations=50, iter_sgd= 5,\
    alpha=0.01, regParam=0.01, factorLength=1,\
                verbose=False, savingFilename = None, evalTraining=None):

    train =data.persist(StorageLevel.MEMORY_ONLY_SER)

    # glom() allows to treat a partition as an array rather as a single row at time
    train_Y = train.map(lambda row: row.label).glom()
    train_X = train.map(lambda row: row.features).glom()
    train_XY = train_X.zip(train_Y).persist(StorageLevel.MEMORY_ONLY_SER)
    #train_XY = train_X.zip(train_Y).cache()

    nrFeat = len(train_XY.first()[0][0])
    np.random.seed(int(time.time())) 
    w =  np.random.ranf((nrFeat, factorLength))
    w = w / np.sqrt((w*w).sum())

    for i in range(iterations):
        wb = sc.broadcast(w)
        wsub = train_XY.map(lambda p: subSGD(p[0], p[1], wb.value, iter_sgd, alpha, regParam))
        w = wsub.mean()
    return w 

def trainFM_sgd(data, iterations=300, alpha=0.01, regParam=0.01, factorLength=1):
	# data is labeledPoint RDD
	train_Y = np.array(data.map(lambda row: row.label).collect())
	train_X = np.array(data.map(lambda row: row.features).collect())
	(N, dim) = train_X.shape
	w =  np.random.ranf((dim, factorLength))
	w = w / np.sqrt((w*w).sum())
	G=np.ones(w.shape)
	for i in myXrange(iterations):
		np.random.seed(int(time.time()))
		random_idx_list = np.random.permutation(N)
		for j in myXrange(N):
		    idx = random_idx_list[j]
		    X = train_X[idx]
		    y = train_Y[idx]
		    grads = fm_gradient_sgd_trick(X, y, w, regParam)
		    G += grads * grads
		    w -= alpha * grads / np.sqrt(G)
	return w

def runLogisticRegressionImplementationOnSpark(sc = None):
    if sc == None: sc = SparkContext()
    trainData = readCSVDataAsSparseVectors(sc, trainUSPSFileName)
    testData = readCSVDataAsSparseVectors(sc, testUSPSFileName)
    
    optimalW = trainFM_parallel_sgd(sc, trainData, iterations=1, evalTraining=False)
    evaluateFM_SGD(testData, optimalW)
    
    optimalW = trainFM_sgd(trainData, iterations=1)
    evaluateFM_SGD(testData, optimalW)
