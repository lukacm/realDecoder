#!/usr/bin/python3
import cmath
import sys
import numpy as np
import re

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
        variables = np.flip(result.group(1).split(), axis=0)
        print(variables)
    gates =+1


# Create all Toffoli gates
matrices = dict()
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
for i in content:
    if i.startswith(".end"):
        flag = 0
    if flag:
        vars = i.split()
        current = matrices[vars[0]]
        for j in range(numvars-int(vars[0][1])):
            print('multiple: %i' %j)
            next = np.kron(ID,current)
            print(next)
            #current = next
    if i.startswith(".begin"):
        flag = 1

