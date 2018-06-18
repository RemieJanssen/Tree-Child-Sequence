from functools import reduce
from collections import deque

#Changes from v2.0:
# IsTrivialCherry(treeList,cherry) had a mistake. it checked whether cherry[0] was in a tree twice, now it checks both elements of the cherry 
# IsTrivialCherry(treeList,cherry) is not needed anymore: there was too much redundancy
# New functions TNFCherries and TNFCherriesBinary
# 
#

#1. PARSING#############################################
#2. TREE INFO###########################################
#3. Cherries ###########################################
#4. Cherry reductions###################################
#5. CONSTRUCTIONS ALGORITHMS############################
#6. CLUSTERS############################################
#7. Check Sequences################################################


###############################1. PARSING############################



def IsBinaryTree(tree):
    if type(tree)==str:
        return True
    elif len(tree)!=2:
        return False
    else:
        return IsBinaryTree(tree[0]) and IsBinaryTree(tree[1])


#==============================================================================
# #Remove empty trees from a list of trees
# def CleanTreeList(treeList):
#     lijst=[]
#     for tree in treeList:       
#         if not EmptyTree(tree):
#             lijst+=tree
#     return lijst
#==============================================================================

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
    if len(tree)==2 and type(tree)!=str:
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

#==============================================================================
# # Makes a sublist of nonforbidden cherries
# #Input: a list of cherries and a set of forbidden leaves for the second element
# #Output: a list of non-forbidden cherries
# def NonForbiddenCherries(cherryList, forbiddenLeaves):
#     nonForbiddenList=[]
#     for c in cherryList:
#         if c[1] not in forbiddenLeaves:
#             nonForbiddenList+=[c]
#     return nonForbiddenList
# 
# # Makes a sublist of nonforbidden cherries for the Binary algorithm: each leaf can be the first element at most 2 times, and each leaf used as a first element cannot be used as a second element anymore
# #Input: a list of cherries, a set of forbidden leaves for the second element, a set of forbidden leaves for the first element of the cherry
# #Output:a list of non-forbidden cherries
# def BinaryNonForbiddenCherries(cherryList, forbiddenLeaves, forbiddenBinary):
#     nonForbiddenList=[]
#     for c in cherryList:
#         if c[1] not in forbiddenLeaves and c[0] not in forbiddenBinary:
#             nonForbiddenList+=[c]
#     return nonForbiddenList
#==============================================================================
    
#==============================================================================
# # Checks whether a cherry is trivial for a given set of trees (given that it is a cherry for some tree)
# #Input: list of trees and a cherry
# #Output: False if the cherry is nontrivial (i.e. there is a tree with both leaves of the cherry, but not the cherry itself), True if the cherry is trivial
# def IsTrivialCherry(treeList,cherry):
#     for t in treeList:
#         if (cherry not in CherryListTree(t)) and (cherry[0] in TaxaInTree(t)) and (cherry[1] in TaxaInTree(t)):
#             #if cherry is not a cherry in t but both elements of cherry are in t
#             return False
#     return True
# 
# # Makes a sublist of trivial cherries in given the set of trees from a set of cherries present in the trees
# #Input: list of trees and a list of cherries
# #Output: list of trivial cherries
# def TrivCherryList(treeList,cherryList):
#     newList=[]
#     for c in cherryList:
#         if IsTrivialCherry(treeList,c):
#             newList+=[c]
#     return newList
#==============================================================================


# Makes a list of nonforbidden trivial cherries
#Input: a list of cherries and a set of forbidden leaves for the second element
#Output: a list of non-forbidden cherries
def TNFCherries(treeList, forbiddenLeaves):
    cherriesLists = map(CherryListTree, treeList)
    taxaLists = map(TaxaInTree, treeList)
    taxaAndCherries = zip(taxaLists,cherriesLists)
    allCherries= [item for sublist in cherriesLists for item in sublist]
    #make a list of the NF cherries in the first tree 
    potentialTNFCherries = filter(lambda x: x[1] not in forbiddenLeaves, allCherries)
    #filter the list of potential cherries to be trivial
    #the reduction checks whether one cherry is trivial
    TNFCherryList= filter(lambda x: all(map(lambda v: not(x not in v[1] and x[0] in v[0] and x[1] in v[0]) ,taxaAndCherries)), potentialTNFCherries)
    return CleanList(TNFCherryList)


# Makes a list of nonforbidden trivial cherries Binary case
#Input: a list of cherries and a set of forbidden leaves for the second element and a set of forbidden leaves for the first element
#Output: a list of non-forbidden cherries
def TNFCherriesBinary(treeList, forbiddenLeaves, forbiddenBinary):
    cherriesLists = map(CherryListTree, treeList)
    taxaLists = map(TaxaInTree, treeList)
    taxaAndCherries = zip(taxaLists,cherriesLists)
    allCherries= [item for sublist in cherriesLists for item in sublist]
    
    #make a list of the NF cherries in the first tree 
    potentialTNFCherries = filter(lambda x: x[1] not in forbiddenLeaves and x[0] not in forbiddenBinary, allCherries)
    #filter the list of potential cherries to be trivial
    #the reduction checks whether one cherry is trivial
    TNFCherryList= filter(lambda x: all(map(lambda v: not(x not in v[1] and x[0] in v[0] and x[1] in v[0]) ,taxaAndCherries)), potentialTNFCherries)
    return CleanList(TNFCherryList)




    

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
    tnfCherries = TNFCherries(currentTrees,currentForbidden)
    while len(tnfCherries)>0:
        for reducedCherry in tnfCherries:
            if reducedCherry[1] not in currentForbidden:
                newSeq+=[reducedCherry]
                currentForbidden+=[reducedCherry[0]]
                currentTrees=ReduceCherryForest(currentTrees,reducedCherry)
        tnfCherries = TNFCherries(currentTrees,currentForbidden)
    return newSeq, currentTrees, currentForbidden

def ReduceTrivialCherriesBinary( treeList , forbidden , forbiddenBinary):
    newSeq=[]
    currentForbidden=forbidden[:]
    currentForbiddenBinary=forbiddenBinary[:]
    currentTrees=treeList[:]
    tnfCherries = TNFCherriesBinary(currentTrees,currentForbidden,currentForbiddenBinary)
    while len(tnfCherries)>0:
        for reducedCherry in tnfCherries:
            if reducedCherry[1] not in currentForbidden and reducedCherry[0] not in currentForbiddenBinary:
                newSeq+=[reducedCherry]
                currentForbidden+=[reducedCherry[0]]
                if reducedCherry[0] in currentForbidden:
                    currentForbiddenBinary+=[reducedCherry[0]]
                currentTrees=ReduceCherryForest(currentTrees,reducedCherry)
        tnfCherries = TNFCherriesBinary(currentTrees,currentForbidden,currentForbiddenBinary)
    return newSeq, currentTrees, currentForbidden, currentForbiddenBinary

################################5. CONSTRUCTIONS ALGORITHMS#####################




#==============================================================================
# #TreeChildSequence(treeList,k), takes a list of trees, a number k and a set of forbidden leaves. Outputs a TC sequence for treelist with at most k retics if it exists and forbidden leaves do not occur as second of the pair
# def TreeChildSequence(treeList,k,kCurrent,forbidden):
#     if k<0:
#         return False
#     S1, currentTrees, currentForbidden = ReduceTrivialCherries( treeList , forbidden )
#     nfCherries = filter(lambda x: x[1] not in currentForbidden, CherryListForest(currentTrees))
#     taxa=TaxaInForest(currentTrees)
#     n=len(taxa)
#     if n==1:#only one taxon left in all trees, so they are all the same one-leaf tree
#         return S1+[[taxa[0],'-']]
#     #if the algorithm reaches this part, then there are no trivial cherries in nfCherries, so they are all nonTrivial and nonForbidden
#     if len(nfCherries) > 8*k :
#         return False
#     if kCurrent<1:
#         return False
#     #check if this works, we just need that any TC sequence for trees with n leaves in total need at most n+k+2 cherries (I think 2n should be fine already) 
#     for c in nfCherries:#for all non-forbidden cherries 
#         newTreeList=ReduceCherryForest(currentTrees,c)
#         forbidden2=currentForbidden+[c[0]]
#         newSeq=TreeChildSequence(newTreeList,k,kCurrent-1,forbidden2)
#         if type(newSeq)==list:
#             return S1+[c]+newSeq
#     return False
#             
# 
# #same as before, but now can only delete each leaf at most
# def BinaryTreeChildSequence(treeList,k,kCurrent,forbidden,forbiddenBinary):
#     if k<0:
#         return False
#     S1, currentTrees, currentForbidden, currentForbiddenBinary = ReduceTrivialCherriesBinary( treeList , forbidden , forbiddenBinary)
#     nfCherries = filter(lambda x: x[0] not in currentForbiddenBinary and x[1] not in currentForbidden, CherryListForest(currentTrees))
#     taxa=TaxaInForest(currentTrees)
#     n=len(taxa)
#     if n==1:#only one taxon left in all trees, so they are all the same one-leaf tree
#         return S1+[[taxa[0],'-']]
#     #if the algorithm reaches this part, then there are no trivial cherries in nfCherries, so they are all nonTrivial and nonForbidden
#     if len(nfCherries) > 8*k :
#         return False
#     if kCurrent==0:
#         return False
#     #check if this works, we just need that any TC sequence for trees with n leaves in total need at most n+k+2 cherries
#     for c in nfCherries:
#         newTreeList=ReduceCherryForest(currentTrees,c)
#         forbidden2=list(currentForbidden+[c[0]])
#         forbiddenBinary2=list(currentForbiddenBinary)
#         if c[0] in currentForbidden:
#             forbiddenBinary2+=[c[0]]
#         newSeq=BinaryTreeChildSequence(newTreeList,k,kCurrent-1,forbidden2,forbiddenBinary2)
#         if type(newSeq)==list:
#             return S1+[c]+newSeq
#     return False
#==============================================================================


#==============================================================================
# #Find optimal by looking for solutions with increasing reticulation number 
# #BINARY
# def BTCSeqInc(treeList,k):
#     i=0
#     while i<k+1:
#         print('k='+str(i))
#         S=BinaryTreeChildSequence(treeList,i,i,[],[])
#         if S:
#             print(S)
#             return S
#         print('does not work')
#         i+=1
#     else:
#         return False
# 
# #Find optimal by looking for solutions with increasing reticulation number 
# #Non-BINARY
# def TCSeqInc(treeList,k):
#     i=0
#     while i<k+1:
#         print( 'k='+str(i))
#         S=TreeChildSequence(treeList,i,i,[])
#         if S:
#             print(S)
#             return S
#         print( 'does not work')
#         i+=1
#     else:
#         print('done')
#         return False
# 
#==============================================================================



####################################NON-BINARY


#TreeChildSequence(treeList,k), takes a list of trees, a number k and a set of forbidden leaves. Outputs a TC sequence for treelist with at most k retics if it exists and forbidden leaves do not occur as second of the pair
#Returns: Prune by feasibility?, Prune by optimality?, sequence, forbidden,  trees
def TreeChildSequenceContinue(treeList,k,kLeft,forbidden):
    if k<0 or kLeft<0:
        return True, False, [],[] ,[],[]
    S1, currentTrees, currentForbidden = ReduceTrivialCherries( treeList , forbidden )
    nfCherries = filter(lambda x: x[1] not in currentForbidden, CherryListForest(currentTrees))
    taxa=TaxaInForest(currentTrees)
    n=len(taxa)
    if n<=1:#only one taxon left in all trees, so they are all the same one-leaf tree
        return False, True, S1+[[taxa[0],'-']], [],[],[]
    #if the algorithm reaches this part, then there are no trivial cherries in nfCherries, so they are all nonTrivial and nonForbidden
    if len(nfCherries) > 8*k :
        return True, False, [], [],[],[]
    if kLeft<1:
        return True, False, [], [],[],[]
    return False, False, S1 , nfCherries ,currentForbidden, currentTrees




#Find optimal by Depth first
#Non-BINARY
def TCSeqDF(treeList,k):
    open_problems=[]
    noOfTaxa=len(TaxaInForest(treeList))
    currentBest=k+1
    root=(treeList,0,[],[])#trees, number of retics already used,forbidden nodes, sequence
    open_problems.append(root)
    bestS='noSolution'
    while not open_problems==[]:
        subtree_root=open_problems.pop()
        if len(TaxaInForest(subtree_root[0]))+len(subtree_root[3]) < noOfTaxa+currentBest:
            pruneFeasible, pruneOpt, S, nfCherries,currentForbidden, currentTrees =TreeChildSequenceContinue(subtree_root[0],currentBest,currentBest-subtree_root[1],subtree_root[2])
            if not pruneFeasible and not pruneOpt:
                #add problems to open_problems
                for c in nfCherries:
                    open_problems.append((ReduceCherryForest(currentTrees,c),subtree_root[1]+1,currentForbidden+[c[0]],subtree_root[3]+S+[c]))
#            elif pruneFeasible and not pruneOpt:
                #do not do anything
            elif not pruneFeasible and pruneOpt:
                #update best found retic number, remember this problem
                kNewS=len(subtree_root[3])+len(S)-noOfTaxa
                if kNewS<currentBest:
                    currentBest=kNewS
                    bestS=subtree_root[3]+S
#                    print('length of current best Sequence: '+str(len(bestS)))
#                    print( bestS)
#                    print( currentBest)
    return bestS
            
            
    
#Find optimal by Breadth first
#Non-BINARY
def TCSeqBF(treeList,k):
    open_problems=deque()
    noOfTaxa=len(TaxaInForest(treeList))
    currentBest=k+1
    root=(treeList,0,[],[])#trees, number of retics already used,forbidden nodes, sequence
    open_problems.append(root)
    bestS='noSolution'
    while not len(open_problems)==0:
        subtree_root=open_problems.popleft()
        if len(TaxaInForest(subtree_root[0]))+len(subtree_root[3]) < noOfTaxa+currentBest:
            pruneFeasible, pruneOpt, S, nfCherries,currentForbidden, currentTrees =TreeChildSequenceContinue(subtree_root[0],currentBest,currentBest-subtree_root[1],subtree_root[2])
            if not pruneFeasible and not pruneOpt:
                #add problems to open_problems
                for c in nfCherries:
                    open_problems.append((ReduceCherryForest(currentTrees,c),subtree_root[1]+1,currentForbidden+[c[0]],subtree_root[3]+S+[c]))
    #        elif pruneFeasible and not pruneOpt:
                #do not do anything
            elif not pruneFeasible and pruneOpt:
                #update best found retic number, remember this problem
                kNewS=len(subtree_root[3])+len(S)-noOfTaxa
                if kNewS<currentBest:
                    currentBest=kNewS
                    bestS=subtree_root[3]+S
                    print('length of current best Sequence: '+str(len(bestS)))
                    print( bestS)
                    print( currentBest)
    return bestS




####################################BINARY


#TreeChildSequence(treeList,k), takes a list of trees, a number k and a set of forbidden leaves. Outputs a TC sequence for treelist with at most k retics if it exists and forbidden leaves do not occur as second of the pair
#Returns: Prune by feasibility?, Prune by optimality?, sequence, forbidden,forbiddenBinary,  trees,
def BTreeChildSequenceContinue(treeList,k,kLeft,forbidden,forbiddenBinary):
    if k<0 or kLeft<0:
        return True, False, [],[] ,[],[],[]
    S1, currentTrees, currentForbidden, currentForbiddenBinary = ReduceTrivialCherriesBinary ( treeList , forbidden ,forbiddenBinary)
    nfCherries = filter(lambda x: x[0] not in currentForbiddenBinary and x[1] not in currentForbidden, CherryListForest(currentTrees))
    taxa=TaxaInForest(currentTrees)
    n=len(taxa)
    if n==1:#only one taxon left in all trees, so they are all the same one-leaf tree
        return False, True, S1+[[taxa[0],'-']], [],[],[],[]
    #if the algorithm reaches this part, then there are no trivial cherries in nfCherries, so they are all nonTrivial and nonForbidden
    if len(nfCherries) > 8*k :
        return True, False, [], [],[],[],[]
    if kLeft<1:
        return True, False, [], [],[],[],[]
    return False, False, S1 , nfCherries ,currentForbidden, currentForbiddenBinary, currentTrees


#Find optimal by Depth first
#BINARY
def BTCSeqDF(treeList,k):
    open_problems=[]
    noOfTaxa=len(TaxaInForest(treeList))
    currentBest=k+1
    root=(treeList,0,[],[],[])#trees, number of retics already used,forbidden nodes, forbiddenBinary, sequence
    open_problems.append(root)
    bestS='noSolution'
    while not open_problems==[]:
        subtree_root=open_problems.pop()
        if len(TaxaInForest(subtree_root[0]))+len(subtree_root[4]) < noOfTaxa+currentBest:
            pruneFeasible, pruneOpt, S, nfCherries,currentForbidden,currentForbiddenBinary, currentTrees =BTreeChildSequenceContinue(subtree_root[0],currentBest,currentBest-subtree_root[1],subtree_root[2],subtree_root[3])
            if not pruneFeasible and not pruneOpt:
                #add problems to open_problems
                for c in nfCherries:
                    if c[0] in currentForbidden:
                        forbiddenBinary2=currentForbiddenBinary+[c[0]]
                    else:
                        forbidden2=currentForbidden+[c[0]]
                        forbiddenBinary2=currentForbiddenBinary
                    open_problems.append((ReduceCherryForest(currentTrees,c),subtree_root[1]+1,forbidden2,forbiddenBinary2,subtree_root[4]+S+[c]))
    #        elif pruneFeasible and not pruneOpt:
                #do not do anything
            elif not pruneFeasible and pruneOpt:
                #update best found retic number, remember this problem
                kNewS=len(subtree_root[4])+len(S)-noOfTaxa
                if kNewS<currentBest:
                    currentBest=kNewS
                    bestS=subtree_root[4]+S
                    print('length of current best Sequence: '+str(len(bestS)))
                    print( bestS)
                    print( currentBest)
    return bestS
            
            
    
#Find optimal by Breadth first
#BINARY
def BTCSeqBF(treeList,k):
    open_problems=deque()
    noOfTaxa=len(TaxaInForest(treeList))
    currentBest=k+1
    root=(treeList,0,[],[],[])#trees, number of retics already used,forbidden nodes, forbiddenBinary, sequence
    open_problems.append(root)
    bestS='noSolution'
    while not len(open_problems)==0:
        subtree_root=open_problems.popleft()
        if len(TaxaInForest(subtree_root[0]))+len(subtree_root[4]) < noOfTaxa+currentBest :
            pruneFeasible, pruneOpt, S, nfCherries,currentForbidden,currentForbiddenBinary, currentTrees =BTreeChildSequenceContinue(subtree_root[0],currentBest,currentBest-subtree_root[1],subtree_root[2],subtree_root[3])
            if not pruneFeasible and not pruneOpt:
                #add problems to open_problems
                for c in nfCherries:
                    if c[0] in currentForbidden:
                        forbiddenBinary2=currentForbiddenBinary+[c[0]]
                    else:
                        forbidden2=currentForbidden+[c[0]]
                        forbiddenBinary2=currentForbiddenBinary
                    open_problems.append((ReduceCherryForest(currentTrees,c),subtree_root[1]+1,forbidden2,forbiddenBinary2,subtree_root[4]+S+[c]))
    #        elif pruneFeasible and not pruneOpt:
                #do not do anything
            elif not pruneFeasible and pruneOpt:
                #update best found retic number, remember this problem
                kNewS=len(subtree_root[4])+len(S)-noOfTaxa
                if kNewS<currentBest:
                    currentBest=kNewS
                    bestS=subtree_root[4]+S
                    print('length of current best Sequence: '+str(len(bestS)))
                    print( bestS)
                    print( currentBest)
    return bestS







#==============================================================================
# 
# #Find optimal by looking for increasingly good solutions, i.e. find solution with retic number $i<k$, then run the algorithm looking for solution with at most $i-1$ retisulations
# #BINARY
# def BTCSeqDec(treeList,k):
#     noOfTaxa=len(TaxaInForest(treeList))
#     Done=False
#     i=1
#     currOpt='No solution'
#     currOptRetics=k+1
#     while not Done:
#         print( 'iteration: ' + str(i) +'kB='+ str(currOptRetics))
#         S=BinaryTreeChildSequence(treeList,currOptRetics-1,currOptRetics-1,[],[])
#         if S:
#             print( S)
#             currOpt=S
#             currOptRetics=len(S)-noOfTaxa
#             i+=1
#         else:
#             Done = True
#     return currOpt
# 
# 
# #Find optimal by looking for increasingly good solutions, i.e. find solution with retic number $i<k$, then run the algorithm looking for solution with at most $i-1$ retisulations
# #NON-BINARY
# def TCSeqDec(treeList,k):
#     noOfTaxa=len(TaxaInForest(treeList))
#     Done=False
#     i=1
#     currOpt='No solution'
#     currOptRetics=k+1
#     while not Done:
#         print( 'iteration: ' + str(i) +'k='+ str(currOptRetics))
#         S=TreeChildSequence(treeList,currOptRetics-1,currOptRetics-1,[])
#         if S:
#             print( S)
#             currOpt=S
#             currOptRetics=len(S)-noOfTaxa
#             i+=1
#         else:
#             Done = True
#     return currOpt
# 
#==============================================================================


#==============================================================================
# #Find solution where each cluster has at most k retics
# def TCSeqCluster(treeList,k):
#     allLeaves=TaxaInForest(treeList)
#     leavesLeft=[]
#     seq=[]
#     clusters=MaximumCommonClusters(treeList)
#     clustersTaxa=map(TaxaInTree,clusters)
#     
#     #The following adds all leaves that are nog in a cluster to leavesLeft
#     for l in allLeaves:
#         inACluster=False
#         for c in clustersTaxa:
#             if l in c:
#                 inACluster=True
#         if not inACluster:
#             leavesLeft+=[l]
#             
#             
#     newTreeLists = RestrictForest(treeList, clustersTaxa)
#     for tl in newTreeLists:
#         newSeq=TreeChildSequence(tl,k,k,[])
#         seq+=newSeq[:-1]
#         leavesLeft+=[newSeq[-1][0]]
#     
#     lastPart=TreeChildSequence(RestrictForest(treeList,[leavesLeft])[0],k,k,[])
#     return seq+lastPart
#==============================================================================
        
    

#Find optimal solution using cluster reduction, for each cluster we use algorithm
#
## ISSUES!
#
#does not seem to give the right answer every time yet!

def TCSeqClusterOpt(treeList,k, algorithm):
    allLeaves=TaxaInForest(treeList)
    leavesLeft=[]
    seq=[]
    clusters=MaximumCommonClusters(treeList)
    clustersTaxa=map(TaxaInTree,clusters)
    totalUsedK=0
    #The following adds all leaves that are nog in a cluster to leavesLeft
    for l in allLeaves:
        inACluster=False
        for c in clustersTaxa:
            if l in c:
                inACluster=True
        if not inACluster:
            leavesLeft+=[l]
            
    print(clustersTaxa)
    newTreeLists = RestrictForest(treeList, clustersTaxa)
    currK=k
    for i,tl in enumerate(newTreeLists):
        print('-----------------------------------------------------')
        print(currK)
        print(totalUsedK)
        print('-----------------------------------------------------')
        print(tl)
        print(clustersTaxa[i])
        noOfTaxa=len(clustersTaxa[i])
        newSeq=algorithm(tl,min(currK,noOfTaxa))
        usedK=len(newSeq)-noOfTaxa
        currK-=usedK
        totalUsedK+=usedK
        seq+=newSeq[:-1]
        print(newSeq)
        leavesLeft+=[newSeq[-1][0]]
    
    print('-----------------------------------------------------')
    print(currK)
    print
    print('-----------------------------------------------------')    
    lastForest=RestrictForest(treeList,[leavesLeft])[0]
    print(lastForest)
    print(leavesLeft)
    noOfTaxa=len(leavesLeft)
    lastPart=algorithm(lastForest,min(currK,noOfTaxa))
    if type(lastPart)!=list:
        return('no solution')
    print('-----------------------------------------------------')    

    print(len(seq+lastPart)-len(allLeaves))
    return seq+lastPart



#Find optimal solution using cluster reduction, for each cluster we use algorithm
#Uses all clusters, from small to large,
#
## ISSUES!
#
#does not seem to give the right answer every time yet!
def TCSeqClusterTotalOpt(treeList,k, algorithm):
    allLeaves=TaxaInForest(treeList)
    seq=[]
    clusters=CommonClusters(treeList)
    clustersTaxa=sorted(map(TaxaInTree,clusters),key=len)+[allLeaves]
    totalUsedK=0
    currentTrees=treeList[:]

#    print('the clusters are:')
#    print(clustersTaxa)
#    print('\n')


#    newTreeLists = RestrictForest(treeList, clustersTaxa)

    currK=k
    
    for i,clu in enumerate(clustersTaxa):
#        print('-----------------------------------------------------')
#        print(currK)
#        print(totalUsedK)
#        print(clu)
        tlClu = RestrictForest(currentTrees,[clu])[0] 
#        print(tlClu)
#        print('-----------------------------------------------------')
        currentTaxa=TaxaInForest(tlClu)
        noOfTaxa=len(currentTaxa)
        newSeq=algorithm(tlClu,min(currK,noOfTaxa))
        usedK=len(newSeq)-noOfTaxa
        currK-=usedK
        totalUsedK+=usedK
        seq+=newSeq[:-1]
#        print(newSeq)
        currentTrees=RemoveLeavesForest(currentTrees,clu,[newSeq[-1][0]])
    seq+=newSeq[-1:]
    print('-----------------------------------------------------')
#    print(currK)
#    print(totalUsedK)
#    print('')
    print(seq)
    print('-----------------------------------------------------')    
    
    return seq

        





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



def RemoveLeavesTree(tree,removed):
    if type(tree)==str:
        if tree in removed:
            return []
        return tree
    part0 = RemoveLeavesTree(tree[0],removed)
    part1 = RemoveLeavesTree(tree[1],removed)
    if part0==[] and part1==[]:
        return[]
    elif part0==[]:
        return part1
    elif part1==[]:
        return part0
    return [part0,part1]



def RemoveLeavesForest(treeList,removed,exceptions):
    removed1=set()
    if exceptions!=[]:
        for x in removed:
            if x not in exceptions:
                removed1.add(x)
    else:
        removed1=set(removed)
    return map(lambda x: RemoveLeavesTree(x,removed1),treeList)



# Returns a list of all leaves in the tree/network.

def Leaves(tree, leaves):
    if isinstance(tree, str):
        if tree not in leaves:
            leaves.append(tree)
        return leaves
    else:
        Leaves(tree[0], leaves)
        Leaves(tree[1], leaves)
        return leaves

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
                if sorted(Leaves(item1,[])) == sorted(Leaves(item2, [])):
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
            if set(sorted(Leaves(item,[]))).issubset(set(sorted(Leaves(item2,[])))) and item != item2:
                copyclusters.remove(item)
                break
    return copyclusters







#########################7. MAIN################################################

def CheckSeqForbidden(seq):
    forbidden=set()
    for c in seq:
        if c[1] in seq:
            return False
        forbidden.add(c[0])
    return True

def ReducesTrees(treeList,seq):
    currentTrees=treeList
    for c in seq[:-1]:
        currentTrees = ReduceCherryForest(currentTrees,c)
    for t in currentTrees:
        if t!=seq[-1][0]:
            return False
    return True

def TestTCseq(treeList,seq):
    if CheckSeqForbidden(seq):
        if ReducesTrees(treeList,seq):
            return True
        else:
            return False, 'does not reduce forest'
    else: 
        return False, 'forbidden cherries'
