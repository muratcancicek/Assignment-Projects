from MainSrc.PythonVersionHandler import *
from .ProductReader import *
from .BsonIO import *
from paths import *

def nullCargoInfo(product, field):
    product[field + '_' + "shippingDate"] = None
    product[field + '_' + "shippingTime"] = None
    product[field + '_' + "feeType"] = None
    product['cargoInfo_cargoFees_ABROAD_fee'] = None
    product['cargoInfo_cargoFees_ABROAD_firmCode'] = None
    product['cargoInfo_cargoFees_DOMESTIC_fee'] = None
    product['cargoInfo_cargoFees_DOMESTIC_firmCode'] = None
    return product 

def expandCargoFees(product):
    cargoFees = product['cargoInfo']['cargoFees']
    if len(cargoFees) != 0:
        for fee in cargoFees:
            if fee['direction'] == 'ABROAD':
                product['cargoInfo_cargoFees_ABROAD_fee'] = fee['fee']
                product['cargoInfo_cargoFees_ABROAD_firmCode'] = fee['firmCode']
            else:
                product['cargoInfo_cargoFees_DOMESTIC_fee'] = fee['fee']
                product['cargoInfo_cargoFees_DOMESTIC_firmCode'] = fee['firmCode']
    else:
        product['cargoInfo_cargoFees_ABROAD_fee'] = None
        product['cargoInfo_cargoFees_ABROAD_firmCode'] = None
        product['cargoInfo_cargoFees_DOMESTIC_fee'] = None
        product['cargoInfo_cargoFees_DOMESTIC_firmCode'] = None
    return product 

def expandProductField(product, field):
    if product == None: print_(field, 'Trouble')
    if field == 'cargoInfo' and product[field] == None: 
        product.pop(field)
        return nullCargoInfo(product, field)
    else:
        fieldMap = product[field]
        for k, v in fieldMap.items():
            if k == 'store':
                product[field + '_storeId'] = v['storeId'] if v != None else None
            if k == 'cargoFees':
                product = expandCargoFees(product)
            elif not k in ['caddeFeature', 'mostSoldFeature', 'campaigns', 'store', 'cargoFees', 'nick', 'name']:
                product[field + '_' + k] = v
        product.pop(field)
        return product

def expandSpecs(product):
    specMap = {}
    for spec in product['specs']:
        specMap[spec['description']] = spec['values'][0]
    product['specs'] = specMap
    return product 

def generateFieldsExpandedProducts(fileName = commonFolder + 'expandedProducts.bson',  products = None, printing = False):
    products = readProducts(products)
    for product in products:
        product = fixQuotesOnProduct(product)
        product.pop('_id')
        product.pop('categories')
        product.pop('catalog')
        product.pop('impressionScore')
        product.pop('productCatalogs')
        product.pop('collapseHash')
        product.pop('productId')  
        product.pop('marketPrice')  
        product = expandProductField(product, 'feature')
        product = expandProductField(product, 'category')
        product = expandProductField(product, 'cargoInfo')
        product = expandProductField(product, 'member')
        product = expandSpecs(product)
    writeToBson(products, fileName, printText = printing)

def checkCommonFieldsCount(products = None):
    products = readProducts(products)
    length = len(products[0])
    print_(length)
    for product in products:
        if length != len(product):
            for k in product.keys():
                if not k in products[0].keys():
                    print_(k)

def generateCommonFieldList(fileName = commonFieldFolder + 'commonFieldList.bson', products = None, printing = False):
    products = readExpandedProducts(products)
    commonFieldList = products[0].keys()
    commonFieldList.remove("specs")
    writeToBson(commonFieldList, fileName, printing)
    return commonFieldList

def readCommonFieldList(fileName = commonFieldFolder + 'commonFieldList.bson'):
    return evalBson(fileName)

def generateCommonFieldValueLists(fileName = valuesFolder + 'commonFieldValueLists.bson',  products = None, printing = False):
    products = readExpandedProducts(products)
    commonFieldList = readCommonFieldList()
    commonFieldValueLists = {}
    for field in commonFieldList:
        commonFieldValueLists[field] = []
    for product in products:
        for field in commonFieldList:
            commonFieldValueLists[field].append(product[field])
    writeToBson(commonFieldValueLists, fileName, printText = printing, sort = False)

def readCommonFieldValueLists(fileName = valuesFolder + 'commonFieldValueLists.bson'):
    return evalBson(fileName)

def containsType(l, t):
    for e in l:
        if t == None:
            if e == None:
                return True
        elif isinstance(e, t):
            return True
        return False

def setWithNone(l):
    li = [e for e in l if e != None]
    li.append(None)
    return li

def getTypeOfListElement(l):
    li = setWithNone(l)
    if len(li) == 0:
        return type(None).__name__
    else:
        return type(li[0]).__name__

def generateCommonFieldValueTypes(fileName = valuesFolder + 'commonFieldValueTypes.bson',  products = None, printing = False):
    products = readExpandedProducts(products)
    commonFieldValueLists = readCommonFieldValueLists()
    commonFieldValueTypes = {}
    for field, fieldList in commonFieldValueLists.items():
            commonFieldValueTypes[field] = getTypeOfListElement(fieldList)
    writeToBson(commonFieldValueTypes, fileName, printText = printing)

def readCommonFieldValueTypes(fileName = valuesFolder + 'commonFieldValueTypes.bson'):
    return evalBson(fileName)

def generateCommonFieldValueTypeCounts(fileName = valuesFolder + 'commonFieldValueTypeCounts.bson',  products = None, printing = False):
    commonFieldValueTypes = readCommonFieldValueTypes()
    typeCounts = {}
    typeList = commonFieldValueTypes.values()
    typeSet = list(set(typeList))
    for type in typeSet:
        typeCounts[type] = typeList.count(type)
    writeToBson(typeCounts, fileName, printText = printing)

def generateCommonFieldValueSets(fileName = valuesFolder + 'commonFieldValueSets.bson',  products = None, printing = False):
    products = readExpandedProducts(products)
    commonFieldValueLists = readCommonFieldValueLists()
    commonFieldValueSets = {}
    originalSets = evalBson(valuesFolder + 'commonFields_Values.json')
    for field, fieldList in commonFieldValueLists.items():
        if containsType(fieldList, None):
            fieldList = setWithNone(fieldList)
        if not (containsType(fieldList, dict) or containsType(fieldList, list)):
            fieldList = list(set(fieldList))
        if field in originalSets.keys():
            fieldList.extend([value for value in originalSets[field] if not value in fieldList])
        commonFieldValueSets[field] = fieldList

    writeToBson(commonFieldValueSets, fileName, printText = printing)
    
def readCommonFieldValueSets(fileName = valuesFolder + 'commonFieldValueSets.bson'):
    return evalBson(fileName)

def generateCommonFieldValueCounts(fileName = valuesFolder + 'commonFieldValueCounts.bson',  products = None, printing = False):
    commonFieldValueSets = readCommonFieldValueSets()
    valueCounts = {}
    for k, v in commonFieldValueSets.items():
        valueCounts[k] = len(v)
    writeToBson(valueCounts, fileName, printText = printing)

def readCommonFieldValueCounts(fileName = valuesFolder + 'commonFieldValueCounts.bson'):
    return evalBson(fileName)

def generateCommonFieldStatistics(products = None, printing = False):
    products = readExpandedProducts(products)
    generateCommonFieldList(products = products, printing = printing)
    generateCommonFieldValueLists(products = products, printing = printing)
    generateCommonFieldValueTypes(products = products, printing = printing)
    generateCommonFieldValueSets(products = products, printing = printing)
    generateCommonFieldValueCounts(products = products, printing = printing)
    generateCommonFieldValueTypeCounts(products = products, printing = printing)

def readCommonFieldStatistics(products = None, regenerate = False):
    if regenerate:
         products = readProducts(products)
         generateCommonFieldStatistics(products)
    statistics = {}
    statistics["fieldList"] = readCommonFieldList()
    statistics["fieldValueLists"] = readCommonFieldValueLists()
    statistics["fieldValueSets"] = readCommonFieldValueSets()
    statistics["fieldValueTypes"] = readCommonFieldValueTypes()
    statistics["fieldValueCounts"] = readCommonFieldValueCounts()
    return statistics 




     

