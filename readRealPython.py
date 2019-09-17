#!/usr/bin/python3
import cmath
import sys
import numpy as np
import re

def swap(i, wires):
    current = ID
    print(i)
    for j in range(0, wires-2):
        if j == i:
            current = np.kron(current, SWAP)
        else:
            current = np.kron(current,ID)
    if i > j:
            current = np.kron(current, SWAP)
    return current




#Default Matrices
ID = np.array([[1,0],[0,1]])
SWAP = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
CNOT = np.array([[1, 0, 0, 0], [ 0, 1, 0, 0], [ 0, 0, 0, 1], [ 0, 0, 1, 0]])
CCNOT = np.array([[1, 0, 0, 0, 0, 0, 0, 0], [ 0, 1, 0, 0, 0, 0, 0, 0], [ 0, 0, 1, 0, 0, 0, 0, 0], [ 0, 0, 0, 1, 0, 0, 0, 0], [ 0, 0, 0, 0, 1, 0, 0, 0], [ 0, 0, 0, 0, 0, 1, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 1], [ 0, 0, 0, 0, 0, 0, 1, 0]])
CV = np.array([[ 1, 0, 0, 0], [ 0, 1, 0, 0], [ 0, 0, (1+complex(0,1))/2, (1-complex(0,1))/2], [ 0, 0, (1-complex(0,1))/2, (1+complex(0,1))/2]])

filename = sys.argv[1]
with open(filename) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
#content = [x.strip() for x in content]
exp1 = re.compile(".numvars (.*)")
exp2 = re.compile(".variables (.*)")
gates = 0
for i in content:
    if i.startswith(".numvars"):
        result = exp1.search(i)
        numvars = int(result.group(1))
    if i.startswith(".variables"):
        result = exp2.search(i)
        variables = result.group(1).split()
        variables.reverse()
        print(variables)
    gates =+1


# Create all Toffoli gates
matrices = dict()
circuit = np.empty([gates,numvars,numvars])
for i in range(numvars):
    a = np.eye(pow(2,(i+1)))
    #Reverse the bottom NOT
    a[pow(2,i+1)-2][pow(2,i+1)-2] = 0
    a[pow(2,i+1)-1][pow(2,i+1)-1] = 0
    a[pow(2,i+1)-2][pow(2,i+1)-1] = 1
    a[pow(2,i+1)-1][pow(2,i+1)-2] = 1
    matrices['t'+str(i+1)] = a 
    #print(matrices['t'+str(i+1)])

#Process the real array
flag = 0
exp3 = re.compile(".(\d+)")
for i in content:
    if i.startswith(".end"):
        flag = 0
    if flag:
        vars = i.split()
        current = matrices[vars[0]]
        result = exp3.search(vars[0])
        res = result.group(1).split()
        size = int(res[0])
        # create the k-controlled toffoli aligned with bottom bit
        for j in range(numvars-size):
            #print('multiple: %i' %j)
            next = np.kron(ID,current)
            print(next.shape)
            current = next
        nominal = variables
        target = vars[1:]
        print(len(target))
        diff = numvars - len(target)
        print(target)
        print(nominal)
        front = np.eye(pow(2,numvars))
        print(front.shape)
        back = np.eye(pow(2,numvars))
        for t in range(len(target)-1,-1,-1):
            nominal = variables.copy()
            #print(target[t])
            if target[t] != nominal[t+diff]:
                print('orig: {} current {}'.format(nominal[t+diff], target[t]))
                indx = nominal.index(target[t])
                swpsnum = abs(t+diff-indx)
                print('Needs {}'.format(swpsnum))
                for q in range(0,swpsnum):
                    print(indx)
                    sw = swap(indx, numvars)
                    front = front*sw
                    back = sw*back
                    nominal[indx+q],nominal[indx+q+1] = nominal[indx+q+1],nominal[indx+q]
                print(nominal)
        current = back+current*front
    if i.startswith(".begin"):
        flag = 1


