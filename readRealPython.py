#!/usr/bin/python3
import cmath
import sys
import csv
import numpy as np
import pandas as pd
import re
np.set_printoptions(threshold=sys.maxsize)

def swap(i, wires):
    if i == 0:
        current = SWAP.copy()
    else:
        current = ID.copy()
    for j in range(1, wires-1):
        if j == i:
            current = np.kron(current, SWAP)
        else:
            current = np.kron(current,ID)
    if i > j:
            current = np.kron(current, SWAP)
    #print(current)
    return current




#Default Matrices
ID = np.array([[1,0],[0,1]])
SWAP = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
CNOT = np.array([[1, 0, 0, 0], [ 0, 1, 0, 0], [ 0, 0, 0, 1], [ 0, 0, 1, 0]])
CCNOT = np.array([[1, 0, 0, 0, 0, 0, 0, 0], [ 0, 1, 0, 0, 0, 0, 0, 0], [ 0, 0, 1, 0, 0, 0, 0, 0], [ 0, 0, 0, 1, 0, 0, 0, 0], [ 0, 0, 0, 0, 1, 0, 0, 0], [ 0, 0, 0, 0, 0, 1, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 1], [ 0, 0, 0, 0, 0, 0, 1, 0]])
CV = np.array([[ 1, 0, 0, 0], [ 0, 1, 0, 0], [ 0, 0, (1+complex(0,1))/2, (1-complex(0,1))/2], [ 0, 0, (1-complex(0,1))/2, (1+complex(0,1))/2]])

filename = sys.argv[1]
outfilename = filename+'.out'

#outfile = open(outfilename, 'w')
#writer = csv.writer(outfile)
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
    gates +=1

outfile = open(outfilename, 'w')
outfile.write(filename)
outfile.write(str(variables))
outfile.close()

# Create all Toffoli gates
matrices = dict()
finals = dict()
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
gates = 0
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
        # create the k-controlled toffoli  and align it with lowest common bit
        for j in range(numvars-size):
            next = np.kron(ID,current)
            current = next
        nominal = variables.copy()
        target = vars[1:]
        diff = numvars - len(target)
        front = np.eye(pow(2,numvars))
        back = np.eye(pow(2,numvars))
        for t in range(len(target)-1,-1,-1):
            if target[t] != nominal[t+diff]:
                indx = nominal.index(target[t])
                swpsnum = abs(t+diff-indx)
                for q in range(0,swpsnum):
                    sw = swap(indx+q, numvars)
                    front = front@sw
                    back = sw@back
                    nominal[indx+q],nominal[indx+q+1] = nominal[indx+q+1],nominal[indx+q]
        current = back@current@front
        outfile = open(outfilename, 'a')
        outfile.write('\nGate number {}, name {}'.format(gates, i))
        outfile.close()
        pd.DataFrame(current).to_csv(outfilename,mode='a', header=None, index=None)
        finals[str(gates)] = current
        gates += 1
    if i.startswith(".begin"):
        flag = 1
final = np.eye(pow(2,numvars))
for i in range(gates-1,-1,-1):
    final = finals[str(i)]@final

outfile = open(outfilename, 'a')
outfile.write('\nFinal Matris Representation\n')
outfile.close()
pd.DataFrame(final).to_csv(outfilename,mode='a', header=None, index=None)

