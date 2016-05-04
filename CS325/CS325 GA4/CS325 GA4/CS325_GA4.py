import csv
from pulp import *
import math
####################  READING DATA  #####################

def getDataAsDict():
    data = {}
    with open('corvallis.csv', 'rb') as csvfile:
         reader = csv.reader(csvfile, delimiter=';', quotechar='|')
         keys = "STATION;DATE;TMAX;TMIN;year;month;day;average;day".split(';')
         dict = {}
         for row in reader:
             for j in range(len(keys)):
                dict[keys[j]] = row[j]
             data[row[1]] = dict.copy()
    return data

def getDataAsList():
    data = [0]*22450
    with open('corvallis.csv', 'rb') as csvfile:
         reader = csv.reader(csvfile, delimiter=';', quotechar='|')   
         for row in reader:
             if row[-1] != "day": 
                     data[int(row[-1])] = float(row[-2])
    return data

####################       MAIN         #####################
a0 = (2*math.pi)/365.25
a1 = (2*math.pi)/(365.25*10.7)
constraintCounter = 0
xs = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5' ]#
def addConstraintsTo(prob, xVars, d, y, z): 
    global a0, a1, constraintCounter 
    factors = { 'x0': 1, 'x1': d,
                'x2': math.cos(a0*d), 'x3': math.sin(a0*d), 
                'x4': math.cos(a1*d), 'x5': math.sin(a1*d) 
                }

# The two constraints are added to 'prob'
    firstMultiplicationList = [y] + [-factors[i]*xVars[i] for i in xs]
    secndMultiplicationList = [-y] + [factors[i]*xVars[i] for i in xs]
    prob += z >= lpSum(firstMultiplicationList), 'Constraint ' + str(constraintCounter); constraintCounter+=1
    prob += z >= lpSum(secndMultiplicationList), 'Constraint ' + str(constraintCounter); constraintCounter+=1
   
# Create the 'prob' variable to contain the problem data
prob = LpProblem("Local Warming", LpMinimize)

# A dictionary called 'x_vars' is created to contain the referenced Variables
xVars = LpVariable.dicts("Xs",xs,0) 
z = LpVariable('z')

# The objective function is added to 'prob' first
prob += lpSum(z), 'Minimize z'
dataList = getDataAsList() 
for d in range(len(dataList)):
    addConstraintsTo(prob, xVars, d, dataList[d], z)

prob.writeLP("Local Warming.lp")  # optional
prob.solve()

print "Status:", LpStatus[prob.status]
for v in prob.variables():
    print v.name, "=", v.varValue 