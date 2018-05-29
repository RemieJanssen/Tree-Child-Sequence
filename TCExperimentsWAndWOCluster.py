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
    print(nw)
    trees = RandomSubtrees(nw, s)[0]
    elapsed= timer()-start
    return trees,elapsed, nw

def TimedAlgoClu(treeList,k,algorithm):
    elapsed=0
#    if len(treeList)==1:
#        seq=treeList[0]
#    else:
    start = timer()
    seq = TCSeqClusterOpt(treeList,k,algorithm)
    elapsed= timer()-start
    return seq, elapsed 

def TimedAlgo(treeList,k,algorithm):
    elapsed=0
#    if len(treeList)==1:
#        seq=treeList[0]
#    else:
    start = timer()
    seq = algorithm(treeList,k)
    elapsed= timer()-start
    return seq, elapsed 


noOfLeaves = 10
noOfTrees  = 3
MaxNoOfRetics = 9
StepNoOfRetics = 1
repeats = 10
algo = [TCSeqBF,TCSeqDF]
name=map(lambda x: x.__name__ , algo)

if not os.path.exists('./outputWAndWOClu/'):
    os.makedirs('./outputWAndWOClu/')


with open('./outputWAndWOClu/algo='+str(name)+'_'+'n='+str(noOfLeaves)+'_'+'s='+str(noOfTrees)+'.csv', 'w') as csvfile:
    fieldnames = ['kNw', 'network', 'timeNetwork','trees']
    for a in algo:
        nA=a.__name__
        fieldnames+=['kFound'+nA,'timeSeq'+nA,'seq'+nA]+['ClukFound'+nA,'ClutimeSeq'+nA,'Cluseq'+nA]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for k in range(0,MaxNoOfRetics,StepNoOfRetics):
        for r in range(repeats):
            print('\n')
            print(k)
            trees, timeNetwork, nw = TimedRandomTrees(noOfLeaves,k,noOfTrees)
            trees2 = map(intTreeToStrTree, trees)
            print(trees2)
            print(timeNetwork)
            
            newRow = {'kNw': k,'timeNetwork' : timeNetwork,'trees' : trees2, 'network' : nw, }

            for a in algo:
                nA=a.__name__
                print(nA)
                print('no clu')
                seq, timeSeq = TimedAlgo(trees2,noOfLeaves,a)
                print(seq)
                print(timeSeq)
                newRow['kFound'+nA]= len(seq)-noOfLeaves
                newRow['timeSeq'+nA] = timeSeq
                newRow['seq'+nA] = seq
                
                print(nA)
                print('clu')
                seq, timeSeq = TimedAlgoClu(trees2,noOfLeaves,a)
                print(seq)
                print(timeSeq)
                newRow['ClukFound'+nA]= len(seq)-noOfLeaves
                newRow['ClutimeSeq'+nA] = timeSeq
                newRow['Cluseq'+nA] = seq
            writer.writerow(newRow)


