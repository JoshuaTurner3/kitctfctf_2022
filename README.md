# Writeup for KITCTF 2022 'Prime Guesser 1' and 'Prime Guesser 2' Challenges
## Introduction
  This is a brief explanation of the process that I went through in order to solve the 'Prime Guesser 1' and 'Prime Guesser 2' challenges for KITCTF 2022. The explanation is simplified and does not discuss all the different tangents I went down to solve these challenges; however, a majority of the work is preserved in the various files of './crypto_prime_guesser_1/' if you would like to explore those yourself. The three "solution" files are working versions of the code solved local, using process, and using remote. Coincidentally, Prime Guesser 1 & 2 have a solution that is the same between them and so my solution for Prime Guesser 1 allowed me to solve Prime Guesser 2 by changing 4 characters between the "solution_remote.py" of each challenge. I'm new to CTFs and this challenge took me a while but it was fun to get through and rewarding at the end, especially whenever the solution applied to both.

## Prime Guesser 1
### Introduction
  This challenge prompts the user for an option in a menu of three choices (0, 1, 2):
  
0. Prompts the user for a number and encrypts it
1. Prompts the user for two parts of an encrypted message and returns whether or not the first digit is 0
2. Exits the menu and prompts the user for a guess at te factors of a number
    
### The Beginning
  As with every CTF challenge, I started Prime Guesser 1 by downloading the relevant server file code and reading it relentllessly to understand what was ocurring in the program. Typically, this is pretty straightforward; however, for this challenge there were a lot of components to keep track of and I spent a while trying to understand each indivdual part in excrutiating detail. There were 6 important global and constant variables that I found immediately:
  
* n [Power of 2]
* q [Power of 2]
* t [Power of 2]
* poly_mod [List of size n, filled with 0's except for the first and last element being 1]
* pk [List of two lists]
* sk [List of size n of random 1's or 0's]

After noticing this, I looked at the encryption function that they were used in and found the following:
  ```mermaid
graph TD
    classDef default fill:#5978cf,stroke:#000,color:#000
    classDef input fill:#64c452,stroke:#000,color:#000
    classDef function fill:#c97038,stroke:#000,color:#000

    size:::input--> m
    pt:::input--> m

    q:::input-->delta
    t:::input-->delta

    m --> scaled_m
    delta --> scaled_m
    q:::input--> scaled_m


    size --> gen_normal_poly
    size --> gen_binary_poly
    gen_normal_poly:::function --> e1
    gen_normal_poly:::function --> e2
    gen_binary_poly:::function --> u

    pko:::input --> ct0
    u --> ct0
    q --> ct0
    poly_mod:::input --> ct0
    e1 --> ct0
    scaled_m --> ct0

    pk1:::input --> ct1
    u --> ct1
    q --> ct1
    poly_mod -->ct1
    e2 --> ct1
  ```
  Now, this looks quite complicated, and that's because it is. However, this is not even the beginning of the pain that I went through, because in order to calculate ct0 and ct1 three important functions were called: polymul, polydiv, and, polyadd. These functions are almost normal in that they are named after polynomial multiplication, polynomial division, and polynomial addition; however, their implementation is not so simple, and what is even more confusing is that polydiv is *called* in polymul and polyadd. Why is this? I have no clue, and I never did find out why. However, what I did start to attempt was writing down the encryption equations to see if they were solvable, and who would have guessed that they weren't (at least not for my measly brain). Or atleast, not in a way that didn't involve bruteforcing. Therefore, I will leave it as a mystery of the universe, because shortly after confusing myself with all of this information (and more), I decided that I would simply take a break and come back later.
### The Return
  After having a nice lunch plagued by the thoughts of my inadequency, I returned once more to this CTF but this time with a different approach. What if I don't *have* to understand what's going on in order to solve it? After all, option "1" in the menu allows us to input our own encrypted text and tells us the first digit of the decryption, and so that was where I started anew. Instead of working to understand encryption, why not just use whatever decryption they provide and then solve for its variables? Here is the fun chart I made for the decryption function:
  ```mermaid
  graph TD
    classDef default fill:#5978cf,stroke:#000,color:#000
    classDef input fill:#64c452,stroke:#000,color:#000
    classDef function fill:#c97038,stroke:#000,color:#000

    sk:::input --> polymul
    ct1:::input --> polymul
    q:::input --> polymul
    poly_mod:::input --> polymul:::function

    polymul --> polyadd:::function
    ct0:::input --> polyadd
    q:::input ---> polyadd
    poly_mod:::input --> polyadd

    polyadd --> scaled_pt

    t:::input --> decrypted_poly
    q:::input --> decrypted_poly
    scaled_pt --> decrypted_poly

    decrypted_poly --First Index--> return
  ```
  Yet again, it is complicated, but less so, and where did the random variables from the encryption go? The lack of specific key in this decryption gave me hints that all the random number stuff was just to throw me off. However, what is even more exciting about the decryption function is how simple it is, and how when using menu option 1 I am able to determine the first digit of the encryption output. This gave me an idea, if I set ct1 to 0 then the polymod will be a list of 0's, then if I set all of ct0 to be $2^i$ then scaled_pt should be $2^i$. Now, here comes the crucial part. Decrypted_poly is calculated using the following equation:
  
$dp=\frac{(spt \cdot t)}{q}\%t$

Which means that if scaled_pt (spt) is some multiple of q then dp = 0. Now, I did this and bruteforced from 0 to 30, but received unexpected (yet later welcomed) results. Running the brute force function provided this output:
```
FINDING Q AND T
iter:  1        i:  2            True
iter:  2        i:  4            True
iter:  3        i:  8            True
iter:  4        i:  16           True
iter:  5        i:  32           True
iter:  6        i:  64           True
iter:  7        i:  128          True
iter:  8        i:  256          True
iter:  9        i:  512          True
iter:  10       i:  1024         True
iter:  11       i:  2048         True
iter:  12       i:  4096         True
iter:  13       i:  8192         True
iter:  14       i:  16384        True
iter:  15       i:  32768        True
iter:  16       i:  65536        True
iter:  17       i:  131072       True
iter:  18       i:  262144       True
iter:  19       i:  524288       True
iter:  20       i:  1048576      False
iter:  21       i:  2097152      False
iter:  22       i:  4194304      False
iter:  23       i:  8388608      False
iter:  24       i:  16777216     False
iter:  25       i:  33554432     False
iter:  26       i:  67108864     False
iter:  27       i:  134217728    False
iter:  28       i:  268435456    False
iter:  29       i:  536870912    False
iter:  30       i:  1073741824   False
iter:  31       i:  2147483648   False
iter:  32       i:  4294967296   True
```
  It started with all True, turned False, and then turned back True again? Unusual, but expected considering I did some horrible math with the decrypted_poly equation. Nonetheless, for a while I just circumvented this by setting a flag to wait for the first False and then break on the next True statement and return i, and after some tests locally this successfully found Q everytime!
  Moving on to the next variable, I decided to try and find T. Now, I don't know what happened during some of this period, I was losing my sanity more and more with each run of my script; however, I stumbled upon a fun little conincidence (probably backed by math, but I refuse to look at it again). Remember the unusual output from finding Q? Well it turns out that the number of *False* statements is the power of T! How did I figure this out? I don't know, it came to me in a dream (not really, I barely slept last night). Regardless, I went about changing the power of T several times and each time this statement held true. Therefore, I did not question anything and just went with it.
  The next variable (and the most difficult) I decided to find was SK. Now SK is different from Q or T in that it is actually a list of values rather than just a single constant, but ignoring this fact for the moment I used a similar technique for finding Q and T but instead made CT1 all 1's and then made CT0 all 0's. The thought behind this was that if I multiply CT1 by SK it might give me some information on SK. However, what I received after printing scaled_pt locally was that it was all 1's. This made some sense considering polymul is basically a convolution followed by a deconvolution, and so I decided to instead just make 1 element of CT1 a 1, the first element. What I received was the following:
  ```
  SCALED_PT [ 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 ]
  ```
  Now this looked more promising! Comparing it to the actual value of SK I received:
  ```
    SK        [ 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 ]
    SCALED_PT [ 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 ]
  ```
  Noticing something fishy? They're the same! Well, almost. Some of the elements of scaled_pt are lost due to the polynomial division. However, this was good news. The next problem was that I was only able to check the first element of scaled_pt and so I needed some way to shift scaled_pt. Knowing that polymul is basically a convolution, I had a suspicion that shifting the index of CT1 that was a 1 would give me this shift. Thus, I decided to write a script that would output to a file this result for every index of i being set to 1. The results may shock you:
```
SK:
[ 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 ]

SCALED_PT:
[ 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 ]
[ 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 ]
[ 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 ]
[ 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 ]
[ 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 ]
[ 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 ]
[ 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 ]
[ 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 ]
[ 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 ]
[ 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 ]
[ 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 ]
[ 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 ]
[ 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 ]
[ 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 ]
[ 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 ]
[ 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 ]
[ 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 ]
[ 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 ]
[ 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 ]
[ 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 ]
[ 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 ]
[ 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 ]
[ 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 ]
[ 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 ]
[ 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 ]
[ 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 ]
[ 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 ]
[ 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 ]
[ 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 ]
[ 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 ]
[ 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 ]
[ 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 ]
[ 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 ]
[ 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 ]
[ 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 ]
[ 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 ]
[ 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 ]
[ 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 ]
[ 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 ]
[ 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 ]
[ 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 ]
[ 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 ]
[ 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 ]
[ 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 ]
[ 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 ]
[ 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 ]
[ 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 ]
[ 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 ]
[ 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 ]
[ 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 ]
[ 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 ]
[ 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 ]
[ 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 0 1 ]
[ 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 ]
[ 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 1 ]
[ 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 1 ]
[ 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 0 0 0 1 ]
[ 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 ]
[ 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 ]
[ 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 ]
[ 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 1 ]
[ 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 0 0 1 ]
[ 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 ]
[ 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 ]
```
  Now, I'm no genius, but just looking at this pattern and seeing the darker (or lighter for you lightmode freaks) streaks along the diagonal told me that my suspicion was correct. So, I wrote a script to get the first element of each of the above arrays and...
  ```
SK:         [ 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 ]
SCALED_PT:  [ 0 0 1 0 1 1 1 0 0 0 0 1 0 0 0 1 1 0 1 1 1 0 1 0 0 0 1 0 0 0 0 1 0 1 0 0 1 0 1 0 1 1 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 0 0 0 1 1 0 0 ]
  ```
  They don't match? Maybe it just needs to be shifted? I wrote a short program to do this, yet still there were only 32 matching characters for all possible in-order shifts of the scaled_pt. Perhaps in reverse?
 ```
SK:         [ 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 ]
SCALED_PT:  [ 0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0 ]
  ```
  Yes, in reverse. Do not ask me why this works it just did, it came to me in a dream. However, this meant that SK could be found! One small issue though, running the script locally just returned a bunch of 0's. Remeber the modulo function above? Well, numpy.round is called on the result of the entire function and so whatever you input must be greater than 0.5 for oracle (Function that tells you whether the first element is 0 or not) to give you a False return (False -> scaled_pt != 0). So instead of setting to 1, I actually set the value to $Q\*2/3. Why this value you might ask? I do not know, yet again it just felt like a non-problematic value since it was neither Q nor T. Running the program this time resulted in success and I therefore had a method to solve for SK.
  Now, the other remaining variables using in the decrypt function are:
* size
* poly_mod
  However, size is easy to get from the number of values in the encrypted CT they provide, and poly_mod can be calculated from this by making an array of the given size and setting the first and last elements to 1. This means that we successfully found all of the values necessary to decrypt any given cypher!
### Solution
  Now, I will not lie to you when I say that I am new to CTF and unexperienced in pwntools. In fact, I spent ~2-3 hours troubleshooting my pwntools because it kept giving me the wrong answer. After some fun rewriting a few byte conversion methods, automating the menu selection, etc, I had finally made a complete script and it worked! (This was not first try, I was losing years off my life for every failed attempt. I probably won't see 30 at this point). Elated at 7am in the morning I decided it was time to go to sleep; however, perhaps my sanity had decreased to such dangerous levels that I decided to *just take a glance at* Prime Guesser 2 isntead of sleeping.
## Prime Guesser 2
  Looking at Prime Guesser 2, I was expecting a whole bunch of addition to Prime Guesser 1; however, they actually *took away* functionality and removed menu option 0 from Prime Guesser 1. However, my solution for Prime Guesser 1 never used menu option 0, and so after switching over a few constants and running the solution program I was ecstatic to see that my program for Prime Guesser 1 also solved Prime Guesser 2! Well, that was easy.
## Conclusion
This is only my second ever CTF and I have only ever done Crypto challenges (due to inexperience in all the others), but I had a lot of fun with these challenges and would like to thank anyone at KITCTF for putting on the competition.

'If you have any comments or questions shoot me a message, I am writing this on ~4.5 hours of sleep so there are likely to be misunderstandings'
