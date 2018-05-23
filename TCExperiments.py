from TCSeqLib import *
from RandomTCNetworkSubtrees import *
from timeit import default_timer as timer
import sys
import csv


def intTreeToStrTree(tree):
    if type(tree)==int:
        return str(tree)
    return map(intTreeToStrTree,tree)


def TimedRandomTrees(n,k,s):
    start = timer()
    trees = RandomSubtrees(GenerateTCNetwork(n, k), s)[0]
    elapsed= timer()-start
    return trees,elapsed

def TimedAlgo(treeList,k):
    start = timer()
    seq = TCSeqCluster(treeList,k)
    elapsed= timer()-start
    return seq, elapsed 



noOfLeaves = 10
noOfTrees  = 3
MaxNoOfRetics = 5
StepNoOfRetics = 1

with open('output'+'n='+str(noOfLeaves)+'_'+'s='+str(noOfTrees)+'.csv', 'w') as csvfile:
    fieldnames = ['k','trees','timeNetwork','seq','timeSeq']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for k in range(0,MaxNoOfRetics,StepNoOfRetics):
        trees, timeNetwork = TimedRandomTrees(noOfLeaves,k,noOfTrees)
        trees = map(intTreeToStrTree, trees)
        seq, timeSeq = TimedAlgo(trees,k+1)
        writer.writerow({'k': k,'trees' : trees,'timeNetwork': timeNetwork,'seq' : seq,'timeSeq': timeSeq})


