from CommonFieldQuantizer import *


def generateStandardizedProducts(products = None, fileName = 'standardizedProducts.json', regenerate = False):
    products = readProducts(products)
    info = readStandardizedFieldsDetails(products, regenerate)
    standardizedProductList = []
    specsValueMap = evalBson('SpecsZ_ScoredValueMap.bson') 
    for product in products:
        standardizedProduct = {}
        for field, value in product.items():
            if info['fieldValueTypes'][field] in ['str', 'bool']:
                if not field in ['title','subTitle']:
                    standardizedProduct[field] = info['fieldsZ_ScoredValueMap'][field][str(value)]
            elif field == 'specs':
                standardizedSpecs = {}
                #for spec, specValue in value.items():
                #    standardizedSpecs[spec] = specsValueMap[product['category_code']][spec][specValue]
                #standardizedProduct[field] = standardizedSpecs
            else:
                if value is None: value=0
                standardizedProduct[field] = calculateZ_ScoredValue(value, info['fieldsMeanMap'][field], info['fieldsSDMap'][field])
        standardizedProductList.append(standardizedProduct)
    writeToBson(standardizedProductList, fileName)

def readStandardizedProducts(fileName = 'standardizedProducts.json'):
    return evalBson(fileName)

def generateProductVector(products = None, fileName = 'ProductVector.json', regenerate = False):
    standardizedProducts = readStandardizedProducts()
    productVector = [product.values() for product in standardizedProducts]
    writeToBson(productVector, fileName)
    
def readProductVector(fileName = 'ProductVector.json'):
    return evalBson(fileName)