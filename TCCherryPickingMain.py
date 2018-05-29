import sys
import csv
from TCSeqLib import *


###############################1. PARSING############################

def ParseNewick (newickTree):
    done=False
    while (not done) and len(newickTree)>0:
        if newickTree[-1]==' ' or newickTree[-1]==';':
            newickTree=newickTree[:-1]
        else: 
            done = True
    if countCommas(newickTree)==0:
        return newickTree
    bracketCount=0
    previousComma=0
    tree=[]
    for i in range(len(newickTree)):
        if newickTree[i]=='(':
            bracketCount+=1
        elif newickTree[i]==')':
            bracketCount-=1
        elif bracketCount==1 and newickTree[i]==',':
            tree+=[ParseNewick(newickTree[previousComma+1:i])]
            previousComma=i
    tree+=[ParseNewick(newickTree[previousComma+1:-1])]
    if bracketCount==0:
        return tree
    return ['Not a Tree']

def countCommas(newickTree):
    count=0
    for x in newickTree:
        if x==',':
            count+=1
    return count

def TreeToNewick(tree):
    if type(tree)==str:
        return tree
    newick='('
    for t in tree:
        newick+= TreeToNewick(t)+','
    return newick[:-1]+')'


def ParseFile( ):  
    with open(option_f_argument, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='	', quotechar='|')
        treeList=[]
        for row in reader:
            tree= ParseNewick(row[-1])
            if tree==['Not a tree']:
                print( row[0]+' is not a tree')
                return False
            if not IsBinaryTree(tree):
                print( tree)
                print( row[0]+' is not binary')
                return False
            if MULTree(tree):
                print( row[0]+' is not uniquely labeled')
                return False 
            treeList+=[tree]
    return treeList

###############################2. I/O############################


option_f = False
option_f_argument = ""
option_k = False
option_k_argument = 0
option_BF = True
option_DF = False
option_bin = False
option_clu = False
i = 1

while i < len(sys.argv):
    arg= sys.argv[i]
    if arg == "-f":
        option_f = True
        i+=1
        option_f_argument = sys.argv[i]
    if arg == "-k":
        option_k = True
        i+=1
        option_k_argument = int(sys.argv[i])
    if arg == "-BF":
        option_BF = True
    if arg == "-DF":
        option_DF = True
        option_BF = False
    if arg == "-bin":
        option_bin = True
    if arg == "-clu":
        option_clu = True
    i += 1



if option_f:
    treeList= ParseFile()
    if not treeList:
        print( "input contains wrong trees")
    else:
        algorithm=TCSeqBF
        if not option_k:
            print( "no reticulation parameter given, set to number of leaves. Type -k [number] for custom setting")
            option_k_argument = len(TaxaInForest(treeList))
        print( "\n")
        print( "Your list of trees:")
        print( treeList)
        print( "\n")
        if option_BF:
            print("Breadth first")
            if option_bin:
                print( "Binary solution:")
                algorithm = BTCSeqBF
            else: 
                print( "NonBinary solution:")
                algorithm = TCSeqBF
        if option_DF:
            print("Depth first")                
            if option_bin:
                print( "Binary solution:")
                algorithm = BTCSeqDF
            else: 
                print( "NonBinary solution:")
                algorithm = TCSeqDF
        if option_clu:
            print("Using cluster reduction")
            print( TCSeqClusterOpt(treeList,option_k_argument, algorithm))
        else:
            print("NOT Using cluster reduction")
            print( algorithm(treeList,option_k_argument))
            
            



else:
    print( "No input file, type -f [filename]")