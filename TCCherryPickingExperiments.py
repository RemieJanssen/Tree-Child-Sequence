from TCSeqLib import *
from RandomTCNetworkSubtrees import *
from timeit import default_timer as timer
import sys
import csv
import os


def intTreeToStrTree(tree):
    if type(tree)==int:
        return str(tree)
    return map(intTreeToStrTree,tree)


def TimedRandomTrees(n,k,s):
    start = timer()
    nw=GenerateTCNetwork(n, k)
#    print(nw)
    trees = RandomSubtrees(nw, s)[0]
    elapsed= timer()-start
    return trees,elapsed, nw

def TimedAlgo(treeList,k,algorithm):
    elapsed=0
#    if len(treeList)==1:
#        seq=treeList[0]
#    else:
    start = timer()
    seq = TCSeqClusterTotalOpt(treeList,k, algorithm)
    elapsed= timer()-start
    return seq, elapsed 






noOfLeaves = 10

MinNoOfTrees  = 1
MaxNoOfTrees  = 15
StepNoOfTrees  = 1

MinNoOfRetics = 1
MaxNoOfRetics = 1
StepNoOfRetics = 1

repeats = 1

algo = []
name=map(lambda x: x.__name__ , algo)

i = 1
while i < len(sys.argv):
    arg= sys.argv[i]

    if arg == "-k":
        i+=1
        MinNoOfRetics = int(sys.argv[i])
        MaxNoOfRetics = int(sys.argv[i])
    if arg == "-kmax":
        i+=1
        MaxNoOfRetics = int(sys.argv[i])    
    if arg == "-kstep":
        i+=1
        StepNoOfRetics = int(sys.argv[i])
    if arg == "-BF":
        algo += [TCSeqBF]
    if arg == "-DF":
        algo += [TCSeqDF]
    if arg == "-r":
        i+=1
        repeats = int(sys.argv[i])
    if arg == "-n":
        i+=1
        noOfLeaves = int(sys.argv[i])    
    if arg == "-t":
        i+=1
        MinNoOfTrees = int(sys.argv[i])
        MaxNoOfTrees = int(sys.argv[i])
    if arg == "-tmax":
        i+=1
        MaxNoOfTrees = int(sys.argv[i])    
    if arg == "-tstep":
        i+=1
        StepNoOfTrees = int(sys.argv[i])
    i += 1
if algo==[]:
    algo=[TCSeqDF]





if not os.path.exists('./outputNoOFtrees/'):
    os.makedirs('./outputNoOFtrees/')
fieldnames = ['kNw', 'network', 'timeNetwork','trees','noOfTrees']
for a in algo:
    nA=a.__name__
    fieldnames+=['kFound'+nA,'timeSeq'+nA,'seq'+nA]
with open('./outputNoOFtrees/algo='+str(name)+'_'+'n='+str(noOfLeaves)+'.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

for noOfTrees in range(MinNoOfTrees,MaxNoOfTrees+1,StepNoOfTrees):
    for k in range(MinNoOfRetics,MaxNoOfRetics+1,StepNoOfRetics):
        for r in range(repeats):
            print('\n')
            print('#trees,#reticulations,repeat')
            print(noOfTrees,k,r+1)
            trees, timeNetwork, nw = TimedRandomTrees(noOfLeaves,k,noOfTrees)
            trees2 = map(intTreeToStrTree, trees)
#            print(trees2)
#            print(timeNetwork)
            
            newRow = {'kNw': k,'timeNetwork' : timeNetwork,'trees' : trees2, 'network' : nw,'noOfTrees':len(trees2) }

            for a in algo:
#                print(nA)
                nA=a.__name__
                seq, timeSeq = TimedAlgo(trees2,k,a)
#                print(seq)
                print(timeSeq)
                print('network k, found k')
                print(k,len(seq)-noOfLeaves)
                print('succes?')
                print(TestTCseq(trees2,seq))
                newRow['kFound'+nA]= len(seq)-noOfLeaves
                newRow['timeSeq'+nA] = timeSeq
                newRow['seq'+nA] = seq
                with open('./outputNoOFtrees/algo='+str(name)+'_'+'n='+str(noOfLeaves)+'.csv', 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow(newRow)


