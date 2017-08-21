
def findProductById(i, path):
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
            PythonVersionHandler.print_('Products cannot be found in the database')
    return products