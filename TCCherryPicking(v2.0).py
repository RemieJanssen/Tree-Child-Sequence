import sys
import csv

#1. PARSING#############################################
#2. TREE INFO###########################################
#3. Cherries ###########################################
#4. Cherry reductions###################################
#5. CONSTRUCTIONS ALGORITHMS############################
#6. CLUSTERS############################################
#7. MAIN################################################


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


def IsBinaryTree(tree):
    if type(tree)==str:
        return True
    elif len(tree)!=2:
        return False
    else:
        return IsBinaryTree(tree[0]) and IsBinaryTree(tree[1])


#Remove empty trees from a list of trees
def CleanTreeList(treeList):
    lijst=[]
    for tree in treeList:       
        if not EmptyTree(tree):
            lijst+=tree
    return lijst

#List to Unique list
def Clean(lijst):
    return list(set(lijst))

#Makes all elements of a list unique
#Input: a list possibly with double entries
#Output: a list without double entries
def CleanList(cherries):
    cleanList=[]
    for c in cherries:
        if c not in cleanList:
            cleanList+=[c]
    return cleanList





#################################2. TREE INFO###############################



#return a list of all taxa in the tree
def TaxaInTree (tree):
    if type(tree)==str:
        return [tree]
    return TaxaInTree(tree[0])+TaxaInTree(tree[1])

#return a list of all taxa in the forest
def TaxaInForest (forest):
    lijst=[]
    for tree in forest:
        lijst+=TaxaInTree(tree)
    return Clean(lijst)

#returns True if tree is an empty tree, and False otherwise
def EmptyTree(tree):
    if type(tree)==str:
        return False
    if len(tree)==0:
        return True
    if len(tree)==1:
        return EmptyTree(tree[0])
    return False

#returns True iff tree is a MUL tree
def MULTree(tree):
    lijst=[]
    for x in TaxaInTree(tree):
        if x in lijst:
            return True
        lijst+=[x]
    return False

#returns True iff forest contains a MUL tree
def ContainsMULTree(forest):
    for tree in forest:
        if MULTree(tree):
            return True
    return False




###########################3. Cherries ###############################

#
#Input:
#Output:
def CherryListTree( tree ):
    if len(tree)==2:
        if type(tree[0])==str and type(tree[1])==str:
            return [[tree[0],tree[1]],[tree[1],tree[0]]]
        elif type(tree)==list:
            return CherryListTree(tree[0]) +CherryListTree(tree[1])
    else:
        return []
        
#Makes a list of all cherries in a set of trees
#Input: a set of trees: forest
#Output: a list of cherries    
def CherryListForest(forest):
    cherriesUnformatted=[]
    for t in forest:
        cherriesUnformatted+=CherryListTree(t)
    return CleanList(cherriesUnformatted)

# Makes a sublist of nonforbidden cherries
#Input: a list of cherries and a set of forbidden leaves for the second element
#Output: a list of non-forbidden cherries
def NonForbiddenCherries(cherryList, forbiddenLeaves):
    nonForbiddenList=[]
    for c in cherryList:
        if c[1] not in forbiddenLeaves:
            nonForbiddenList+=[c]
    return nonForbiddenList

# Makes a sublist of nonforbidden cherries for the Binary algorithm: each leaf can be the first element at most 2 times, and each leaf used as a first element cannot be used as a second element anymore
#Input: a list of cherries, a set of forbidden leaves for the second element, a set of forbidden leaves for the first element of the cherry
#Output:a list of non-forbidden cherries
def BinaryNonForbiddenCherries(cherryList, forbiddenLeaves, forbiddenBinary):
    nonForbiddenList=[]
    for c in cherryList:
        if c[1] not in forbiddenLeaves and c[0] not in forbiddenBinary:
            nonForbiddenList+=[c]
    return nonForbiddenList
    
# Checks whether a cherry is trivial for a given set of trees (given that it is a cherry for some tree)
#Input: list of trees and a cherry
#Output: False if the cherry is nontrivial (i.e. there is a tree with both leaves of the cherry, but not the cherry itself), True if the cherry is trivial
def IsTrivialCherry(treeList,cherry):
    for t in treeList:
        if (cherry not in CherryListTree(t)) and (cherry[0] in TaxaInTree(t)) and (cherry[0] in TaxaInTree(t)):
            #if cherry is not a cherry in t but both elements of cherry are in t
            return False
    return True

# Makes a sublist of trivial cherries in given the set of trees from a set of cherries present in the trees
#Input: list of trees and a list of cherries
#Output: list of trivial cherries
def TrivCherryList(treeList,cherryList):
    newList=[]
    for c in cherryList:
        if IsTrivialCherry(treeList,c):
            newList+=[c]
    return newList



    

################################4. Cherry reductions#################

#Reduces the cherry `cherry' in the tree `tree'
#Input: a phylogenetic tree, and a cherry
#Output: a phylogenetic tree
def ReduceCherryTree(tree,cherry):
    if type(tree)==str:
        return tree
    if tree==cherry:
        return cherry[1]
    if tree==[cherry[1],cherry[0]]:
        return cherry[1]
    return [ReduceCherryTree(tree[0],cherry),ReduceCherryTree(tree[1],cherry)]
        

#Reduces cherry in each tree in treeList
#Input: a list of trees and a cherry
#Output: a list of trees         
def ReduceCherryForest(treeList,cherry):
    newList=[]
    for t in treeList:
        newList+=[ReduceCherryTree(t,cherry)]
    return newList

    
def ReduceTrivialCherries( treeList , forbidden ):
    newSeq=[]
    currentTrees=treeList[:]
    currentForbidden=forbidden[:]
    cherries = CherryListForest(currentTrees)    
    nfCherries = NonForbiddenCherries(cherries, forbidden)
    tnfCherries = TrivCherryList(currentTrees,nfCherries)
    while len(tnfCherries)>0:
        for reducedCherry in tnfCherries:
            if reducedCherry[1] not in currentForbidden:
                newSeq+=[reducedCherry]
                currentForbidden+=[reducedCherry[0]]
                currentTrees=ReduceCherryForest(currentTrees,reducedCherry)
        cherries = CherryListForest(currentTrees)    
        nfCherries = NonForbiddenCherries(cherries, currentForbidden)
        tnfCherries = TrivCherryList(currentTrees,nfCherries)
    return newSeq, currentTrees, nfCherries, currentForbidden

def ReduceTrivialCherriesBinary( treeList , forbidden , forbiddenBinary):
    newSeq=[]
    currentForbidden=forbidden[:]
    currentForbiddenBinary=forbiddenBinary[:]
    currentTrees=treeList[:]
    cherries = CherryListForest(currentTrees)    
    nfCherries = BinaryNonForbiddenCherries(cherries, forbidden,forbiddenBinary)
    tnfCherries = TrivCherryList(currentTrees,nfCherries)
    while len(tnfCherries)>0:
        for reducedCherry in tnfCherries:
            if reducedCherry[1] not in currentForbidden and reducedCherry[0] not in currentForbiddenBinary:
                newSeq+=[reducedCherry]
                currentForbidden+=[reducedCherry[0]]
                if reducedCherry[0] in currentForbidden:
                    currentForbiddenBinary+=[reducedCherry[0]]
                currentTrees=ReduceCherryForest(currentTrees,reducedCherry)
        cherries = CherryListForest(currentTrees)    
        nfCherries = BinaryNonForbiddenCherries(cherries, currentForbidden,currentForbiddenBinary)
        tnfCherries = TrivCherryList(currentTrees,nfCherries)
    return newSeq, currentTrees, nfCherries, currentForbidden, currentForbiddenBinary

################################5. CONSTRUCTIONS ALGORITHMS#####################




#TreeChildSequence(treeList,k), takes a list of trees, a number k and a set of forbidden leaves. Outputs a TC sequence for treelist with at most k retics if it exists and forbidden leaves do not occur as second of the pair
def TreeChildSequence(treeList,k,kCurrent,forbidden):
    S1, currentTrees, nfCherries, currentForbidden = ReduceTrivialCherries( treeList , forbidden )
    taxa=TaxaInForest(currentTrees)
    n=len(taxa)
    if n==1:#only one taxon left in all trees, so they are all the same one-leaf tree
        return S1+[[taxa[0],'-']]
    #if the algorithm reaches this part, then there are no trivial cherries in nfCherries, so they are all nonTrivial and nonForbidden
    if len(nfCherries) > 8*k :
        return False
    if kCurrent==0:
        return False
    #check if this works, we just need that any TC sequence for trees with n leaves in total need at most n+k+2 cherries (I think 2n should be fine already) 
    for c in nfCherries:#for all non-forbidden cherries 
        newTreeList=ReduceCherryForest(currentTrees,c)
        forbidden2=currentForbidden+[c[0]]
        newSeq=TreeChildSequence(newTreeList,k,kCurrent-1,forbidden2)
        if type(newSeq)==list:
            return S1+[c]+newSeq
    return False
            

#same as before, but now can only delete each leaf at most
def BinaryTreeChildSequence(treeList,k,kCurrent,forbidden,forbiddenBinary):
    S1, currentTrees, nfCherries, currentForbidden, currentForbiddenBinary = ReduceTrivialCherriesBinary( treeList , forbidden , forbiddenBinary)
    taxa=TaxaInForest(currentTrees)
    n=len(taxa)
    if n==1:#only one taxon left in all trees, so they are all the same one-leaf tree
        return S1+[[taxa[0],'-']]
    #if the algorithm reaches this part, then there are no trivial cherries in nfCherries, so they are all nonTrivial and nonForbidden
    if len(nfCherries) > 8*k :
        return False
    if kCurrent==0:
        return False
    #check if this works, we just need that any TC sequence for trees with n leaves in total need at most n+k+2 cherries
    for c in nfCherries:
        newTreeList=ReduceCherryForest(currentTrees,c)
        forbidden2=list(currentForbidden+[c[0]])
        forbiddenBinary2=list(currentForbiddenBinary)
        if c[0] in currentForbidden:
            forbiddenBinary2+=[c[0]]
        newSeq=BinaryTreeChildSequence(newTreeList,k,kCurrent-1,forbidden2,forbiddenBinary2)
        if type(newSeq)==list:
            return S1+[c]+newSeq
    return False


#Find optimal by looking for solutions with increasing reticulation number 
#BINARY
def BTCSeqInc(treeList,k):
    i=0
    while i<k+1:
        print 'k='+str(i)
        S=BinaryTreeChildSequence(treeList,i,i,[],[])
        if S:
            return S
        print 'does not work'
        i+=1
    else:
        return False

#Find optimal by looking for solutions with increasing reticulation number 
#Non-BINARY
def TCSeqInc(treeList,k):
    i=0
    while i<k+1:
        print 'k='+str(i)
        S=TreeChildSequence(treeList,i,i,[])
        if S:
            return S
        print 'does not work'
        i+=1
    else:
        return False


#Find optimal by looking for increasingly good solutions, i.e. find solution with retic number $i<k$, then run the algorithm looking for solution with at most $i-1$ retisulations
#BINARY
def BTCSeqDec(treeList,k):
    noOfTaxa=len(TaxaInForest(treeList))
    Done=False
    i=1
    currOpt='No solution'
    currOptRetics=k
    while not Done:
        print 'iteration: ' + str(i)
        S=BinaryTreeChildSequence(treeList,currOptRetics-1,currOptRetics-1,[],[])
        if S:
            print S
            currOpt=S
            currOptRetics=len(S)-noOfTaxa
            i+=1
        else:
            Done = True
    return currOpt


#Find optimal by looking for increasingly good solutions, i.e. find solution with retic number $i<k$, then run the algorithm looking for solution with at most $i-1$ retisulations
#NON-BINARY
def TCSeqDec(treeList,k):
    noOfTaxa=len(TaxaInForest(treeList))
    Done=False
    i=1
    currOpt='No solution'
    currOptRetics=k
    while not Done:
        print 'iteration: ' + str(i)
        S=TreeChildSequence(treeList,currOptRetics-1,currOptRetics-1,[])
        if S:
            print S
            currOpt=S
            currOptRetics=len(S)-noOfTaxa
            i+=1
        else:
            Done = True
    return currOpt



#Find solution where each cluster has at most k retics
def TCSeqCluster(treeList,k):
    allLeaves=TaxaInForest(treeList)
    leavesLeft=[]
    seq=[]
    clusters=MaximumCommonClusters(treeList)
    clustersTaxa=map(TaxaInTree,clusters)
    
    #The following adds all leaves that are nog in a cluster to leavesLeft
    for l in allLeaves:
        inACluster=False
        for c in clustersTaxa:
            if l in c:
                inACluster=True
        if not inACluster:
            leavesLeft+=[l]
            
            
    newTreeLists = RestrictForest(treeList, clustersTaxa)
    for tl in newTreeLists:
        newSeq=TreeChildSequence(tl,k,k,[])
        seq+=newSeq[:-1]
        print newSeq
        leavesLeft+=[newSeq[-1][0]]
    
    lastPart=TreeChildSequence(RestrictForest(treeList,[leavesLeft])[0],k,k,[])
    return seq+lastPart
        
    
        





#########################6. CLUSTERS################################################


#restrict a tree to a set of species
def RestrictTree(tree, species):
    if type(tree)==str:
        if tree in species:
            return tree
        return []
    parts=list(RestrictTree(t,species) for t in tree)
    if parts[0]==[]:
        if parts[1]==[]:
            return []
        return parts[1]
    if parts[1]==[]:
        return parts[0]
    return parts


# retrict a tree to each part of the partition of the species
def RestrictTreeToPartition( tree, speciesLists ):
    restricted=[]
    for s in speciesLists:
        restricted+=[RestrictTree(tree,s)]
    return restricted

    
# restrict each of the trees in the list to each part of the partition
def RestrictForest(treeList, speciesLists):
    list1=[]
    for spList in speciesLists:
        list2=[]
        for tree in treeList: 
            list2+=[RestrictTree(tree,spList)]
        list1+=[list2]
    return list1



## TreeClusterSet(tree,m)
## Input:  list representing a tree, e.g. [[[1, [4, [3, 2]]], 5], [6, [[9, 7], 10]]];, m = [tree]
## Output: list of clusters it contains

def TreeClusterSet(tree, m):
    A = tree[0]
    B = tree[1]

    if isinstance(A,str) and isinstance(B,str):
        return m
    elif isinstance(A,str):
        m.append(B)
        TreeClusterSet(B, m)
        return m
    elif isinstance(B,str):
        m.append(A)
        TreeClusterSet(A, m)
        return m
    else:
        m.extend((A,B))
        TreeClusterSet(A, m)
        TreeClusterSet(B, m)
        return m



## MultipleClusterSet(trees)
## Input:  list of trees
## Output: list of all cluster lists of trees

def MultipleClusterSet(trees):
    n = []
    for i in range(len(trees)):
        n.append(TreeClusterSet(trees[i], [trees[i]]))
    return n



## CommonClusters(trees)
## Input:  list of trees
## Output: list of all common clusters in all trees. Essentially takes the intersection of all lists in MultipleClusterSet(trees)

def CommonClusters(trees):
    commonclusters = []
    n = MultipleClusterSet(trees)
    for item1 in n[0]:
        count = 0
        for i in range(1,len(n)):
            for item2 in n[i]:
                if set(','.join(str(j) for j in item1)) == ((set(','.join(str(j) for j in item2)))):
                    count += 1
        if count == len(n)-1:
            commonclusters.append(item1)
    return commonclusters



## MaximumCommonClusters(trees)
## Input:  list of trees
## Output: Maximal common clusters between trees

def MaximumCommonClusters(trees):
    clusters = CommonClusters(trees)
    copyclusters = clusters[:]
    for item in clusters:
        for item2 in clusters:
            if set(','.join(str(i) for i in item)).issubset(set(','.join(str(i) for i in item2))) and item != item2:
                copyclusters.remove(item)
                break
    return copyclusters








#########################7. MAIN################################################

def ParseFile( ):  
    with open(option_f_argument, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='	', quotechar='|')
        treeList=[]
        for row in reader:
            tree= ParseNewick(row[-1])
            if tree==['Not a tree']:
                print row[0]+' is not a tree'
                return False
            if not IsBinaryTree(tree):
                print tree
                print row[0]+' is not binary'
                return False
            if MULTree(tree):
                print row[0]+' is not uniquely labeled'
                return False 
            treeList+=[tree]
    return treeList


option_f = False
option_f_argument = ""
option_k = False
option_k_argument = 0
option_inc = False
option_dec = False
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
    if arg == "-inc":
        option_inc = True
    if arg == "-dec":
        option_dec = True
    if arg == "-bin":
        option_bin = True
    if arg == "-clu":
        option_clu = True
    i += 1


if option_f:
    if not option_k:
        print "no reticulation parameter given, set to 0. Type -k [number]"
    treeList= ParseFile()
    if not treeList:
        print "input contains wrong trees"
    else:
        if option_clu:
            print "\n"
            print "Your list of trees:"
            print treeList
            print "\n"
            print "Non-Binary Maybe non-optimal solution:"
            print TCSeqCluster(treeList,option_k_argument)
        else:
            if not option_inc and not option_dec:
                print "\n"
                print "Your list of trees:"
                print treeList
                print "\n"
                if option_bin:
                    print "Binary solution:"
                    print BinaryTreeChildSequence(treeList,option_k_argument,option_k_argument,[],[])
                else: 
                    print "NonBinary solution:"
                    print TreeChildSequence(treeList,option_k_argument,option_k_argument,[])
            if option_inc:
                print "\n"
                print "Your list of trees:"
                print treeList
                print "\n"
                if option_bin:
                    print "Binary solution:"
                    print BTCSeqInc(treeList,option_k_argument)
                else: 
                    print "NonBinary solution:"
                    print TCSeqInc(treeList,option_k_argument)
            if option_dec:
                print "\n"
                print "Your list of trees:"
                print treeList
                print "\n"
                if option_bin:
                    print "Binary solution:"
                    print BTCSeqDec(treeList,option_k_argument)
                else: 
                    print "NonBinary solution:"
                    print TCSeqDec(treeList,option_k_argument)
else:
    print "No input file, type -f [filename]"