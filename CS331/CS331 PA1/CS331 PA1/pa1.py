import sys
import Queue 

ID_DFS_MAX_DEPTH = 30
####################  READING FILE  ##################### 
def readFile(fileName):  
    file = open(fileName, 'rb') 
    lines = []
    for rawLine in file: 
        line = str.split(rawLine[:-1], ',')
        for i in range(len(line)):
            line[i] = int(line[i])
        lines.append(line)
    return lines[:2]

###################  READING PROBLEM  ####################
mode = ''
outputFile = None   

def getProblemFromInputs():
    return {'initialState': readFile(sys.argv[1]), 'goalState': readFile(sys.argv[2]), 'mode': sys.argv[3], 'output': sys.argv[4]}
  
             
######################  PRINT STATE  ####################
def printState(state): 
    text = ''
    if isBoatOnLeftAt(state):
        text = str(state[0][0]) + ' M ' + str(state[0][1]) + ' C ' + '_\\--/______________ ' + str(state[1][0]) + ' M ' + str(state[1][1]) + ' C '
    else:
        text = str(state[0][0]) + ' M ' + str(state[0][1]) + ' C ' + '______________\\--/_ ' + str(state[1][0]) + ' M ' + str(state[1][1]) + ' C '
    myPrint(text)

####################  PRINT ACTION  ##################### 
def getActionText(action):
    actionTexts = {'[1, 0]': 'Put one missionary in the boat',
                   '[2, 0]': 'Put two missionaries in the boat',
                   '[0, 1]': 'Put one cannibal in the boat',
                   '[1, 1]': 'Put one cannibal and one missionary in the boat',
                   '[0, 2]': 'Put two cannibals in the boat'}
    return actionTexts[str(action[:2])]

#######################  ACTIONS  #######################
def getActions():
    return [[0, 1], [0, 2], [1, 1], [2, 0], [1, 0]]

##################  GETTING SUCCESSORS  #################
def isBoatOnLeftAt(state):
    return state[0][2] == 1
 
def getSuccessorState(state, action):
    if isBoatOnLeftAt(state):
        return [[state[0][0]-action[0], state[0][1]-action[1], 0], [state[1][0]+action[0], state[1][1]+action[1], 1]]
    else:
        return [[state[0][0]+action[0], state[0][1]+action[1], 1], [state[1][0]-action[0], state[1][1]-action[1], 0]]
    
###################  STATE VALIDATION  ##################
def isStateValid(state):
    [currentBank, oppositeBank] = [1, 0]
    if isBoatOnLeftAt(state):
        [currentBank, oppositeBank] = [0, 1]
    [missionariesOnCurrentBank, cannibalsOnCurrentBank] = [state[currentBank][0], state[currentBank][1]]
    [missionariesOnNextBank, cannibalsOnNextBank] = [state[oppositeBank][0], state[oppositeBank][1]]
    if missionariesOnCurrentBank < 0 or cannibalsOnCurrentBank < 0 or missionariesOnNextBank < 0 or cannibalsOnNextBank < 0:
         return False
    if missionariesOnCurrentBank > 0 and cannibalsOnCurrentBank > 0 and missionariesOnNextBank > 0 and cannibalsOnNextBank > 0:
         return missionariesOnCurrentBank >= cannibalsOnCurrentBank and missionariesOnNextBank >= cannibalsOnNextBank
    elif missionariesOnCurrentBank == 0: 
         return missionariesOnNextBank >= cannibalsOnNextBank
    elif cannibalsOnCurrentBank == 0: 
         return missionariesOnNextBank == 0 or missionariesOnNextBank >= cannibalsOnNextBank
    elif missionariesOnNextBank == 0: 
         return missionariesOnCurrentBank >= cannibalsOnCurrentBank
    elif cannibalsOnNextBank == 0:
         return missionariesOnCurrentBank == 0 or missionariesOnCurrentBank >= cannibalsOnCurrentBank
     
######################  HEURISTIC  ######################
def heuristic(node):
    state = node['state']
    [missionariesOnLeftBank, cannibalsOnLeftBank] = [state[0][0], state[0][1]]
    [missionariesOnRightBank, cannibalsOnRightBank] = [state[1][0], state[1][1]]
    return missionariesOnRightBank - missionariesOnLeftBank + cannibalsOnRightBank   

######################  EXPANDING  ######################
def expand(fringe, currentNode): 
    actions = getActions() 
    for action in actions:
        successorState = getSuccessorState(currentNode['state'], action) 
        if isStateValid(successorState):
            successorNode = {'parent': currentNode, 'action': action, 'state': successorState, 'depth': currentNode['depth']+1}
            global mode
            if mode =='astar':
                fringe.put((heuristic(successorNode), successorNode))
            else:
                fringe.append(successorNode) 
    return fringe

##################  GETTING SOLUTION  ################### 
def getSolution(node):
    solution = [] 
    while not node['parent'] == None:
        solution.append([node['action'], node['state']])
        node = node['parent']
    solution.reverse()
    return solution 

###################  REMOVING NODES  ################### 
def removeFrom(fringe, currentDepth):  
    global mode
    if mode == 'astar':
        return [fringe.get()[1], fringe]
    if mode == 'dfs':
        return [fringe.pop(), fringe]
    if mode == 'iddfs':  
        if not currentDepth == 0:
            if ID_DFS_MAX_DEPTH%currentDepth == 0:
                return [fringe.pop(0), fringe] 
            else:
                return [fringe.pop(), fringe]
        else:
            return [fringe.pop(), fringe]
    else:        #      the default is breath-first search
        return [fringe.pop(0), fringe] 
    
####################  MY PRINT  #####################
def myPrint(*args):
    line = ''
    for arg in args:
        line += str(arg) + ' ' 
    print line
    global outputFile
    if not outputFile == None:
        outputFile.write(line+'\n')

####################  GRAPH SEARCH  #####################
def graphSearch(problem): 
    initialNode = {'parent': None, 'action': None, 'state': problem['initialState'], 'depth': 0} 
    fringe = [initialNode] 
    if problem['mode'] == 'astar':
        fringe = Queue.PriorityQueue()
        fringe.put((heuristic(initialNode), initialNode))
    closed = [] 
    expandedNodesNumber = 0
    currentDepth = initialNode['depth'] 
    while True:
        if fringe == []:
            myPrint('no solution found')
            return [None, None] 
        [node, fringe] = removeFrom(fringe, currentDepth)
        if node['state'] == problem['goalState']:
            return [getSolution(node), expandedNodesNumber]
        if node['parent'] == None:
            closed.append([None, node['action'], node['state']]) 
            expandedNodesNumber += 1
            currentDepth = node['depth']+1
            fringe = expand(fringe, node)
        elif not [node['parent']['state'], node['action'], node['state']] in closed:
            closed.append([node['parent']['state'], node['action'], node['state']]) 
            expandedNodesNumber += 1
            currentDepth = node['depth']+1
            fringe = expand(fringe, node) 
            
###################  PRINT SOLUTION  ####################
def printSolution(solution):
    for step in solution:
        myPrint(getActionText(step[0]), '\n')
        if not isStateValid(step[1]):
            myPrint('\nInvalid state: ')
            printState(step[1])
            myPrint('\nNo solution found')
            break
        else:
            printState(step[1])
            
###################  PRINT SOLUTION  ####################
def solve(problem):
    global mode
    mode = problem['mode']
    [solution, expandedNodesNumber] = graphSearch(problem)
    if not solution == []:
        myPrint('Solution found by', mode, '!')
        myPrint('Number of nodes the solution path contains:', len(solution)+1)
        myPrint('Number of the expanded nodes:', expandedNodesNumber, '\n')
        printState(problem['initialState']) 
        printSolution(solution)
        print '\nSolution saved into', problem['output'], 'successfully.'
        
##################  PROBLEM VALIDATION  #################
def isProblemValid(problem):
    if not problem['initialState'][0][0] + problem['initialState'][1][0] == problem['goalState'][0][0] + problem['goalState'][1][0]:
       return False
    if not problem['initialState'][0][1] + problem['initialState'][1][1] == problem['goalState'][0][1] + problem['goalState'][1][1]:
       return False
    elif not problem['initialState'][1][0] >= problem['initialState'][1][1]:
       return False
    elif not problem['goalState'][0][0] >= problem['goalState'][0][1]:
        return False
    else:
        return True

####################      MAIN      #####################

problem = getProblemFromInputs() 

if isProblemValid(problem):
    if outputFile == None:
        outputFile = open(problem['output'], "w+") 
    solve(problem) 
    if not outputFile == None:
        outputFile.close()
else:
    print 'Invalid problem, no solution found!'
    
####################    FOR FUN    #####################

#def solve(problem):
#    global mode
#    mode = problem['mode']
#    [solution, expandedNodesNumber] = graphSearch(problem)
#    if not solution == []:
#        myPrint('Solution found by', mode, '!')
#        myPrint('Number of nodes the solution path contains:', len(solution)+1)
#        myPrint('Number of the expanded nodes:', expandedNodesNumber, '\n')

#def runAllSearches(problem):
#    myPrint(problem['initialState'], problem['initialState'], '\n')    
    
#    problem['mode'] = 'astar'
#    solve(problem)

#    problem['mode'] = 'iddfs'
#    solve(problem)

#    problem['mode'] = 'dfs'
#    solve(problem)

#    problem['mode'] = 'bfs'
#    solve(problem)

#def solveAllProblems():
#    global outputFile
#    if outputFile == None:
#        outputFile = open('outputAll.txt', "w+") 
#    problems = [{'initialState': [[0, 0, 0], [3, 3, 1]], 'goalState': [[3, 3, 1], [0, 0, 0]], 'mode': 'astar', 'output': 'output.txt'}, 
#    {'initialState': [[0, 0, 0], [7, 6, 1]], 'goalState': [[7, 6, 1], [0, 0, 0]], 'mode': 'iddfs', 'output': 'output.txt'},
#    {'initialState': [[0, 0, 0], [88, 80, 1]], 'goalState': [[88, 80, 1], [0, 0, 0]], 'mode': 'bfs', 'output': 'output.txt'}
#    ]
#    for problem in problems:
#        runAllSearches(problem)
#        myPrint('')
#    if not outputFile == None:
#        outputFile.close()

#solveAllProblems()