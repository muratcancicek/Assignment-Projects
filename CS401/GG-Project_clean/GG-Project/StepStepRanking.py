
def findProducts_ById(i, path):
    import Trainer, SparkLogFileHandler
    if isinstance(i, list):
        ids = SparkLogFileHandler.sc_().parallelize([int(j) for j in i])
    else:
        ids = SparkLogFileHandler.sc_().parallelize([int(i)])
    products = Trainer.getProducts(ids, path)
    if products.isEmpty():
        import paths
        products = Trainer.getProducts(ids, paths.newProductVectorFolder)
        if products.isEmpty():
            import PythonVersionHandler
            PythonVersionHandler.print_('Products cannot be found in the database.')
    return products


def findProductById(i, path):
    products = findProducts_ById(i, path)
    if not products.isEmpty():
        return products.collect()[0]
    
def findPairById(i1, i2, path):
    import Trainer
    pairs = Trainer.readLabeledPairs(path)
    pairs = pairs.filter(lambda p: (i1, i2) == p[0])
    import PythonVersionHandler
    PythonVersionHandler.print_(pairs.count(), 'Instances have been found for this pair.')
    pairsP = pairs.filter(lambda p: 1 == p[1])
    PythonVersionHandler.print_(pairsP.count(), 'Positive instances have been found for this pair.')
    pairsN = pairs.filter(lambda p: 0 == p[1])
    PythonVersionHandler.print_(pairsN.count(), 'Negative instances have been found for this pair.')
    
def mmmm(i, path):
    import Trainer
    pairs = Trainer.readLabeledPairs(path)
    data1 = pairs.map(lambda p: p[0][0])
    data1 = Trainer.getProducts(data1, path)
    data2 = pairs.map(lambda p: p[0][1])
    data2 = Trainer.getProducts(data2, path)
    label = pairs.map(lambda p: p[1])