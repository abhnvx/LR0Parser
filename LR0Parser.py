#Importing Necessary Libraries

import os
import time
from collections import Counter
import pyfiglet
import termtables as tt

title = pyfiglet.figlet_format("LR (0) Parsing", font="digital")
print(title)

def addDot(dot):
    addDotVar = dot.replace("->", "->.")
    return addDotVar

def compressedName(name: str):
    compResult = Counter(name)
    comp = ''
    for r in compResult:
        comp += r + str(compResult[r])
    return comp

#Function to Save file
def saveFile(final_string, grammar, name):
    directory = os.path.dirname("stringParsing/" + str(grammar) + "/")
    if not os.path.exists(directory):
        print("Creating this Director......")
        os.makedirs(directory)

    with open("stringParsing/{0}/{1}.txt".format(grammar, name), 'w') as fileParsing:
        fileParsing.write(final_string)

#Function to find closure
def findClosure(gram):
    flag = [gram]
    for i in flag:
        j = i[i.index(".") + 1]
        if j != len(i) - 1:
            for k in productionRules:
                if k[0][0] == j and (addDot(k)) not in flag:
                    flag.append(addDot(k))
        else:
            for k in productionRules:
                if k[0][0] == j and i not in flag:
                    flag.append(i)

    return flag

#Fucntion to Swap Values
def swapValues(newValue, posValue):
    newValue = list(newValue)
    temp = newValue[posValue]
    if posValue != len(newValue):
        newValue[posValue] = newValue[posValue + 1]
        newValue[posValue + 1] = temp
        newFinal = "".join(newValue)
        return newFinal
    else:
        return "".join(newValue)

#go to function
def gotoFunction(var1):
    arr = []
    pos = var1.index(".")
    if pos != len(var1) - 1:
        j = list(var1)
        k = swapValues(j, pos)
        if k.index(".") != len(k) - 1:
            l = findClosure(k)
            return l
        else:
            arr.append(k)
            return arr
    else:
        return var1

def Terminals(inputTerminal):
    terminalSet = set()
    for p in inputTerminal:
        x1 = p.split('->')
        for t in x1[1].strip():
            if not t.isupper() and t != '.' and t != '':
                terminalSet.add(t)

    terminalSet.add('$')

    return terminalSet

#function to store non terminals
def nonTerminals(gram):
    terms = set()
    for p in gram:
        x1 = p.split('->')
        for t in x1[1].strip():
            if t.isupper():
                terms.add(t)
    return terms

def getList(graph, state):
    finalList = []
    for g in graph:
        if int(g.split()[0]) == state:
            finalList.append(g)

    return finalList


productionRules = []
itemSet = []
flag = []

with open("input.txt", 'r') as fp:
    for i in fp.readlines():
        productionRules.append(i.strip())

productionRules.insert(0, "X->.S")

print("Augmented Grammar")
print(productionRules)

prod_num = {}
for i in range(1, len(productionRules)):
    prod_num[str(productionRules[i])] = i

j = findClosure("X->.S")
itemSet.append(j)


state_numbers = {}
dfa_prod = {}
items = 0
while True:
    if len(itemSet) == 0:
        break

    jk = itemSet.pop(0)
    kl = jk
    flag.append(jk)
    state_numbers[str(jk)] = items
    items += 1

    if len(jk) > 1:
        for item in jk:
            jl = gotoFunction(item)
            if jl not in itemSet and jl != kl:
                itemSet.append(jl)
                dfa_prod[str(state_numbers[str(jk)]) + " " + str(item)] = jl
            else:
                dfa_prod[str(state_numbers[str(jk)]) + " " + str(item)] = jl

for item in flag:
    for j in range(len(item)):
        if gotoFunction(item[j]) not in flag:
            if item[j].index(".") != len(item[j]) - 1:
                flag.append(gotoFunction(item[j]))


print("Total States: ", len(flag))
for i in range(len(flag)):
    print(i, ":", flag[i])
