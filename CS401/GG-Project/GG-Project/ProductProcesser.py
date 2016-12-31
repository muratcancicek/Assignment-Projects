from ProductReader import *
from BsonIO import *

def readProducts(products = None, fileName = 'products.json',  decoding = 'unicode-escape'):
    return evalBson(fileName, decoding) if products == None else products 

def checkCommonFieldsCount(products = None):
    products = readProducts(products)
    length = len(products[0])
    print length
    for product in products:
        if length != len(product):
            print len(product)

def generateCommonFieldList(fileName = 'commonFieldList.bson', products = None, printing = False):
    products = readProducts(products)
    commonFieldList = products[0].keys()
    writeToBson(commonFieldList, fileName, printing)
    return commonFieldList

def readCommonFieldList(fileName = 'commonFieldList.bson'):
    return evalBson(fileName)

def generateCommonFieldValueLists(fileName = 'commonFieldValueLists.bson',  products = None, printing = False):
    products = readProducts(products)
    commonFieldList = readCommonFieldList()
    commonFieldValueLists = {}
    for field in commonFieldList:
        commonFieldValueLists[field] = []
    for product in products:
        for field in commonFieldList:
            commonFieldValueLists[field].append(product[field])
    writeToBson(commonFieldValueLists, fileName, printText = printing, decoding = 'unicode-escape')

def readCommonFieldValueLists(fileName = 'commonFieldValueLists.bson'):
    return evalBson(fileName, decoding = 'unicode-escape')

def generateCommonFieldValueTypes(fileName = 'commonFieldValueType.bson',  products = None, printing = False):
    products = readProducts(products)
    commonFieldValueLists = readCommonFieldValueLists()
    commonFieldValueTypes = {}
    for field, fieldList in commonFieldValueLists.items():
            commonFieldValueTypes[field] = type(fieldList[0]).__name__
    writeToBson(commonFieldValueTypes, fileName, printText = printing, decoding = 'unicode-escape')

def readCommonFieldValueTypes(fileName = 'commonFieldValueType.bson'):
    return evalBson(fileName, decoding = 'unicode-escape')

def generateCommonFieldValueTypeCounts(fileName = 'commonFieldValueTypeCounts.bson',  products = None, printing = False):
    commonFieldValueTypes = readCommonFieldValueTypes()
    typeCounts = {}
    typeList = commonFieldValueTypes.values()
    typeSet = list(set(typeList))
    for type in typeSet:
        typeCounts[type] = typeList.count(type)
    writeToBson(typeCounts, fileName, printText = printing, decoding = 'unicode-escape')
    



def generateCommonFieldValueSets(fileName = 'commonFieldValueSets.bson',  products = None, printing = False):
    products = readProducts(products)
    commonFieldValueLists = readCommonFieldValueLists()
    commonFieldValueSets = {}
    for field, fieldList in commonFieldValueLists.items():
        if not (isinstance(fieldList[0], dict) or isinstance(fieldList[0], list) or fieldList[0] == None):
            commonFieldValueSets[field] = list(set(fieldList))
        else:
            commonFieldValueSets[field] = fieldList
    writeToBson(commonFieldValueSets, fileName, printText = printing, decoding = 'unicode-escape')

def expandProductFeatureField(product):
    featureMap = product['feature']
    for k, v in featureMap.items():
        product['feature_' + k] = v
    product.pop('feature')

def expandProductCategoryField(product):
    categoryMap = product['category']
    for k, v in categoryMap.items():
        product['category_' + k] = v
    product.pop('')

def generateFieldsExpandedProducts(fileName = 'fieldsExpandedProducts.bson',  products = None, printing = False):
    products = readProducts(products)

