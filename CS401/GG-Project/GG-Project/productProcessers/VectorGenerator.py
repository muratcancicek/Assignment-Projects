from MainSrc.PythonVersionHandler import *
from .CommonFieldQuantizer import *
from paths import *
import csv

def generateStandardizedProducts(products = None, fileName = commonFolder + 'standardizedProducts.json', regenerate = False):
    products = readExpandedProducts(products)
    info = readStandardizedFieldsDetails(products, regenerate)
    standardizedProductList = []
    #specsValueMap = evalBson('SpecsZ_ScoredValueMap.bson') 
    for product in products:
        standardizedProduct = {}
        for field, value in product.items():
            if field == 'specs':
                pass
            elif info['fieldValueTypes'][field] in ['str', 'bool']:
                    #standardizedSpecs = {}
                if not field in ['title','subTitle']:
                    standardizedProduct[field] = info['fieldsZ_ScoredValueMap'][field][str(value)]
                #for spec, specValue in value.items():
                #    standardizedSpecs[spec] = specsValueMap[product['category_code']][spec][specValue]
                #standardizedProduct[field] = standardizedSpecs
            else:
                if value is None: value=0
                standardizedProduct[field] = calculateZ_ScoredValue(value, info['fieldsMeanMap'][field], info['fieldsSDMap'][field])
        standardizedProductList.append(standardizedProduct)
    writeToBson(standardizedProductList, fileName)

def readStandardizedProducts(fileName = commonFolder + 'standardizedProducts.json'):
    return evalBson(fileName)

def generateProductVector(products = None, fileName = commonFolder + 'ProductVector.json', regenerate = False):
    standardizedProducts = readStandardizedProducts()
    productVector = [product.values() for product in standardizedProducts]
    writeToBson(productVector, fileName) 
    
def readProductVector(fileName = commonFolder + 'ProductVector.json'):
    return evalBson(fileName)

def generateProductVectorCSV(products = None, fileName = commonFolder + 'ProductVector.csv', regenerate = False):
    products = readExpandedProducts()
    categoryCodeValueMap = readCommonFieldValueMap()['category_code']
    standardizedProducts = readStandardizedProducts()
    productVector = ''
    for index in range(len(standardizedProducts)):
        standardizedProduct = standardizedProducts[index]
        line = ''
        for key, value in standardizedProduct.items():
            if key != 'category_code':
                line += str(value) + ','
        labels = categoryCodeValueMap[products[index]['category_code']]
        productVector += line + str(labels) + '\n'
    f = open(fileName, 'wb')
    f.write(productVector) 
    f.close() 
    
def readProductVectorCSV(fileName = commonFolder + 'ProductVector.csv'):
    with open(fileName, 'rb') as csvfile:
        productVector = []
        labels = []
        vector = csv.reader(csvfile)
        for row in vector:
            row = [float(value) for value in row]
            productVector.append(row[:-1])
            labels.append(row[-1])
        return productVector, labels

def generateProductVectorFromExpandedProducts():
    generateFieldsExpandedProducts(printing = False)
    products = readProducts(fileName = commonFolder + 'expandedProducts.bson', decoding = None)
    #generateCommonFieldList(products = products)
    #checkCommonFieldsCount(products)
    generateCommonFieldStatistics(products)
    generateCommonFieldsValueMap(products, regenerate = False)
    generateCommonFieldValueLists(products = products,printing = False)
    generateNotNullCommonFieldValueLists(products = products)
    generateCommonFieldsMeanMap()
    generateCommonFieldsSDMap()
    generateCommonFieldsZ_ScoredMap()
    generateCommonFieldsZ_ScoredValueMap()
    generateStandardizedProducts(products)
    generateProductVector()
    generateProductVectorCSV()
