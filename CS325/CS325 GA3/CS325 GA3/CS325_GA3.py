from operator import itemgetter
import timeit, functools
####################   WRITING INPUTS   #####################
def readInput(fileName): 
    arrs = []
    anss = []
    fileO = open(fileName)
    for line in fileO:
        end = str.find(line, "]") 
        arrs.append(list(map(int, str.split(line[1:end],", "))))
        if(line[end+1] == ","):
            anss.append(list(map(int, str.split(line[(end+2):-1],",")))) 
    if anss != []:
        return [arrs, anss]
    else:
        return [arrs]


####################     ALGORITHMS     #####################
def closest(arr):
    m = arr[0]
    for x in arr:
        if abs(x[0]) < abs(m[0]):
            m = x
    return m


def sumsOfArray(arr): 
    sum = 0
    if arr == None:
        return []
    for x in arr:
        sum += x
    sums = [sum] 
    for x in arr[:-1]:
        sum -= x
        sums.append(sum)
    return sums

def getSumsArrays(left, right, start, middle):
    leftSums = sumsOfArray(left)    
    for i in range(len(leftSums)):
        leftSums[i] = [leftSums[i], start+i, middle-1];
    right.reverse()
    rightSums = sumsOfArray(right)
    rightSums.reverse()
    for i in range(len(rightSums)):
        rightSums[i] = [rightSums[i], middle, middle+i];
    return [leftSums, rightSums]

def getKey(item):
        return item[0]

####################     METHOD 1     #####################

def method1(left, right, start, middle):
    sumsArrays = getSumsArrays(left, right, start, middle)
    leftSums = sumsArrays[0]
    rightSums = sumsArrays[1] 
    closestSum = [float("inf"), middle-1, middle]  
    for i in range(len(leftSums)):
        for j in range(len(rightSums)): 
            if abs(leftSums[i][0] + rightSums[j][0]) < closestSum[0]:
                closestSum = [abs(leftSums[i][0] + rightSums[j][0]), leftSums[i][1], rightSums[j][2]]
    return closestSum
        
####################     METHOD 2     #####################

def method2(left, right, start, middle):
    sumsArrays = getSumsArrays(left, right, start, middle)
    leftSums = sumsArrays[0]
    rightSums = sumsArrays[1]   
    sortedLeftSums = leftSums
    sortedRightSums = rightSums
    sortedLeftSums.sort()
    sortedRightSums.sort()
    closestSum = [float("inf"), middle-1, middle]   
    if sortedLeftSums[0][0] < 0:
        for i in range(len(sortedLeftSums)): 
            for j in range(len(sortedRightSums)): 
                if abs(sortedLeftSums[i][0] + sortedRightSums[-j][0]) < closestSum[0]:
                    closestSum = [abs(sortedLeftSums[i][0] + sortedRightSums[-j][0]), sortedLeftSums[i][1], sortedRightSums[-j][2]] 
    elif sortedRightSums[0][0] < 0:
        for i in range(len(sortedRightSums)): 
            for j in range(len(sortedLeftSums)): 
                if abs(sortedLeftSums[-j][0] + sortedRightSums[i][0]) < closestSum[0]:
                    closestSum = [abs(sortedLeftSums[-j][0] + sortedRightSums[i][0]), sortedLeftSums[-j][1], sortedRightSums[i][2]]
    return closestSum

###################     METHOD 3     #####################

def method3(left, right, start, middle):
    sumsArrays = getSumsArrays(left, right, start, middle) 
    leftSums = sumsArrays[0]
    rightSums = sumsArrays[1]  
    negativeRightSums = rightSums 
    for i in range(len(negativeRightSums)):
        negativeRightSums[i][0] *= -1;
    if left != None: 
        allSums = leftSums
    else:
        allSums = negativeRightSums
    if len(negativeRightSums[0]) != 0: 
        allSums.extend(negativeRightSums)
    allSums = sorted(allSums, key = itemgetter(0))
    closestSum = [float("inf"), middle-1, middle]  
    for i in range(len(allSums[:-1])): 
        if abs(allSums[i][0] + -allSums[i+1][0]) <= closestSum[0]:
            if allSums[i][1] < allSums[i+1][2]:
                closestSum = [abs(allSums[i][0] + -allSums[i+1][0]), allSums[i][1], allSums[i+1][2]]
            else:
                closestSum = [abs(allSums[i][0] + -allSums[i+1][0]), allSums[i+1][1], allSums[i][2]] 
    return closestSum

###################     METHOD 4     #####################

def method4(array):  
    allSums = [[array[0],0]]
    for i in range(1, len(array)):
        allSums.append([allSums[i-1][0]+array[i], i])
    allSums = sorted(allSums, key = itemgetter(0))
    closestSum = [float("inf"), 0]  
    for i in range(len(allSums[:-1])): 
        if abs(allSums[i][0] + -allSums[i+1][0]) <= closestSum[0]:
            if allSums[i][1] < allSums[i+1][1]:
                closestSum = [abs(allSums[i][0] + -allSums[i+1][0]), allSums[i][1]+1, allSums[i+1][1]]
            else:
                closestSum = [abs(allSums[i][0] + -allSums[i+1][0]), allSums[i+1][1]+1, allSums[i][1]] 
    closestSum = closest([allSums[0], allSums[len(allSums)-1], closestSum])
    return closestSum

#####################   RECURRENCE    #####################

def closestSubArrayToZero(arr, start, end, method):  
    if method == 4:
        return method4(arr)
    half = (int)(len(arr)/2)
    if len(arr) == 1:
        return [arr[0], start, end]
    else:
        leftResult = closestSubArrayToZero(arr[:half], start, start+half-1, method)
        if 2*half < len(arr):
            rightResult = closestSubArrayToZero(arr[half:], end-half, end, method)
        else:
            rightResult = closestSubArrayToZero(arr[half:], end-half+1, end, method) 
#        Method Selection  
        if method == 1:
            appendedResult = method1(arr[:half], arr[half:], start, start+half)
        elif method == 2:
            appendedResult = method2(arr[:half], arr[half:], start, start+half)
        else:
            appendedResult = method3(arr[:half], arr[half:], start, start+half)
        closestResult = closest([leftResult, rightResult, appendedResult]) 
        return closestResult

####################       TEST         #####################

cache = [] 

def testMethod(fileName, method):
    file = readInput(fileName) 
    arrays = file[0]
    for testCase in range(len(arrays)):
        array = arrays[testCase] 
        result = closestSubArrayToZero(array, 0, len(array)-1, method)
        runtime = timeit.Timer(functools.partial(closestSubArrayToZero, array, 0, len(array)-1, method))
        runtime = runtime.timeit(1)
        #runtime = timeit.Timer('closestSubArrayToZero(array, 0, len(array)-1, method)', "from __main__ import closestSubArrayToZero(array, 0, len(array)-1, method)",).timeit()
        if len(file) > 1:
            answers = file[1]
            if result == answers[testCase]:
                print "Mthd", method, "works for Case", testCase+1, "of 1th txt in", runtime, "Result =", result 
            else:
                print "Mthd", method, "DOES NOT work for Case", testCase+1, "of 1th txt in", runtime, "found =", result, "instead of", answers[testCase]
        else:
           print "Mthd", method, "found Case", testCase+1, "size=", len(array), "of 2th txt in", runtime, "as", result 
           if len(cache) < 20:
               cache.append(str(result[0]) + '\t' + str(result[1]) + '\t' + str(result[2]) + '\n')
def testAllMethodsFor(fileName):
    for method in range(1, 5):
        print "\n###################     METHOD", method, "    #####################\n" 
        testMethod(fileName, method)

####################       MAIN         #####################

testAllMethodsFor("test_cases_with_solutions.txt")
testAllMethodsFor("test_cases_without_solutions.txt")  
ans = open("answers.txt", 'w')
for l in cache:  
    ans.write(l) 