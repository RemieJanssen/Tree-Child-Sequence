ReadMe: RandomTCNetworkSubtrees



Initially, the code generates a random TCnetwork with n leaves and k reticulations.
Then it returns s (or fewer) displayed subtrees 



Input:
input.txt should contain the three elements separated by commas:

number of leaves(n), number of reticulations(k), number of sample size(s)

We require n > k and s <= 2**k.



Output:
There are two outputs.
RandomTCNetworkdescription.txt contains the following information:

- the randomly generated TCnetwork N in unfolded Newick form
- the number of leaves on N
- the number of reticulations on N
- the number of subtrees in RandomTCNetworksubtrees.txt

RandomTCNetworksubtrees.txt displays s (or fewer) subtrees displayed by N.
The number of subtrees may be fewer than s as N does not always display 2**k subtrees.