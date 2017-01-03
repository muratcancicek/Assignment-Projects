from ProductProcesser import *

def generateCommonFieldsValueMap(products = None, fileName = 'commonFieldValueMap.bson', regenerate = False):
    products = readProducts(products)
    statistics = readCommonFieldStatistics(products,regenerate)
    fieldsValueMap = {}
    for field in statistics['fieldList']:
        if statistics['fieldValueTypes'][field] == 'str':
            if not field in ['title','subTitle']:
                valueMap = {}
                count = 1
                for value in statistics['fieldValueSets'][field]:
                    if type(value) is str: 
                        value = value.decode('utf-8') 
                    valueMap[value] = count
                    count += 1
                fieldsValueMap[field] = valueMap
        elif statistics['fieldValueTypes'][field] == 'bool': 
            fieldsValueMap[field] = {False: 1, True: 2}
    writeToBson(fieldsValueMap, fileName)

def generateNotNullCommonFieldValueLists(products = None, fileName = 'commonFieldNotNullValueLists.bson'):
    products = readProducts(products)
    statistics = readCommonFieldStatistics(products)
    fieldsValueLists = {}
    for field in statistics['fieldList']:
        valueList = statistics['fieldValueLists'][field]
        if field in ['cargoInfo_cargoFees_ABROAD_fee', 'cargoInfo_cargoFees_DOMESTIC_fee', 'member_soldCount','member_storeId']:
            fieldsValueLists[field] = [v if v != None else 0 for v in valueList]
        elif field is 'productModifiedDate':
            fieldsValueLists[field] = [product['productModifiedDate'] if product['productModifiedDate'] != None else product['startDate'] for product in products]
        else:
            fieldsValueLists[field] = valueList
    writeToBson(fieldsValueLists,fileName) 

def generateCommonFieldsMeanMap(map, fileName = 'CommonFieldMeanMap.bson'):
    meanMap = {}
    for categoryCode, category in map.items():
        axisMeanMap = {}
        for axisName, axis in category.items():
            sum = 0
            for valueName, value in axis.items():
                 sum += value
            mean = float(sum)/len(axis)
            axisMeanMap[axisName.decode('utf8')] = mean
        meanMap[categoryCode] = axisMeanMap
    writeToBson(meanMap, fileName)

             






