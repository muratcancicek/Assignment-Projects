from MainSrc.PythonVersionHandler import *
from .BsonIO import *
from paths import *

def getCategories(filename):
    categoriesData = readBson("categories.bson")
    categories = categoriesData['data']['categories'] 
    print_(len(categories))
    deepestCategories = [c for c in categories if c['deepest'] == 'Y']
    print_(len(deepestCategories))
    sortedCategories = sorted(deepestCategories, key=lambda k: k['productCount'], reverse = True)
    #print sortedCategories[0]['productCount']
    return sortedCategories, [c['categoryCode'] for c in sortedCategories]

def getCrowdedCategories(filename = "categories.bson", n = 100):
    sortedCategories = getCategories(filename, n)
    finalCategories = sortedCategories[:n]
    return finalCategories, [c['categoryCode'] for c in finalCategories]

def getCategoryCodes(codes):
    line = '('
    for code in codes[:-1]:
        line += '\"' + code + '\", '
    line += '\"' + codes[-1] + '\")'
    print_(line)
    
def readCodeLines():
    codesText = open('codes.txt', "rb")
    codeLines = codesText.read().split('\n')
    codeLists = [l[1:-1].replace(', ', ',').split(',') for l in codeLines]
    for lis in codeLists: 
        print_(len(lis)) 
    return codeLists

def getCategoriesFromProducts(filename):
    products = readBson(filename)
    print_('Product Count:', len(products))
    codes = [p['category']['code'].encode("utf-8") for p in products]
    uniqueCodes = set(codes)
    return list(uniqueCodes)

def summarizeProducts(filename, countPerCategory = 10): 
    uniqueCodes = getCategoriesFromProducts(filename)
    counts = {}
    for code in uniqueCodes:
        counts[code] = codes.count(code)
    print_('Product Count per Category:', counts)
    storedCodes = [k for k, v in counts.iteritems() if v == countPerCategory]
    print_('Stored Product Count:', len(storedCodes))
    return storedCodes, uniqueCodes, counts 

def getremainingCodes(total, storedFile):
    storedCodes, uniqueCodes, counts = summarizeProducts(storedFile)
    crowdedCategories, crowdedCodes = getCrowdedCategories(total + len(uniqueCodes))
    unstoredCodes = [c for c in crowdedCodes if not c in storedCodes]
    print_('Unstored Product Count:', len(unstoredCodes))
    intersectionCodes = [c for c in crowdedCodes if c in storedCodes]
    print_('Intersection Product Count:', intersectionCodes)
    finalCodes = unstoredCodes[:total-len(storedCodes)] 
    print_('Final Product Count:', len(finalCodes))
    intersectCodes = [c for c in finalCodes if c in storedCodes]
    print_('Intersection Product Count:', len(intersectCodes))
    return finalCodes

def getProducts(filename):
    return readBson(filename)

def getProductsByCategoryCode(productList):
    codes = [p['category']['code'] for p in productList]
    uniqueCodes = set(codes)
    categoryList = list(uniqueCodes)
    productDict = {}
    for category in categoryList:
        productDict[category] = []
    for product in productList: 
        productDict[product['category']['code']].append(product)
    return productDict

def getExpandedProductsByCategoryCode(productList, code):
    return [product for product in productList if product['category_code'] == code] 

def mergeProducts():
    product230 = evalBson('products230.bson')
    product780 = evalBson('products780.bson')
    product230Dict = getProductsByCategoryCode(product230)
    product230Dict.pop('rc',0)
    product780Dict = getProductsByCategoryCode(product780)
    #productDict = product230Dict + product780Dict 
    productDict = {}
    productDict = product230Dict.copy()
    productDict.update(product780Dict)
    return productDict

def fixQuotesOnProduct(product):
    if '\"' in  product['title']:
        product['title'] = fixQuotes(product['title'])
    if product['subTitle'] != None:
        if '\"' in  product['subTitle']:
            product['subTitle'] = fixQuotes(product['subTitle'])
    for spec in product['specs']:
        if '\"' in  spec['values'][0]:
            spec['values'][0] = fixQuotes(spec['values'][0])
    return product

def generateGroupedProductsList(readingFileName = 'products.bson', writingFileName = 'groupedProducts.bson'):
    unorderedProductList = evalBson(readingFileName, decoding = 'unicode-escape')
    categoryProductsMap = getProductsByCategoryCode(unorderedProductList)
    orderedProductList = []
    categoryCodes = []
    for categoryCode in categoryProductsMap.keys():
        categoryCodes.append(categoryCode)
    categoryCodes.sort()
    for categoryCode in categoryCodes:
        orderedProductList.extend(categoryProductsMap[categoryCode])
    writeToBson(orderedProductList, writingFileName, decoding = 'unicode-escape', printText = True)
    print_('WARNING: Encoding Error')    

def generateCategoryCodeNameMap():
    categories = evalBson('categories.bson')
    cd = getCategoriesFromProducts('products.bson')
    map = {}
    for c in categories['data']['categories']:
        if c['categoryCode'] in cd:
            map[c['categoryCode']] = c['categoryName']
    writeToBson(map, commonFolder + 'categoryCodeNames.json') 

def readProducts(products = None, fileName = commonFolder + 'products.json', decoding = 'utf-8'):
    return evalBson(fileName) if products == None else products 

def readExpandedProducts(products = None, fileName = commonFolder + 'expandedProducts.bson', decoding = 'utf-8'):
    return readProducts(products, fileName, decoding)
