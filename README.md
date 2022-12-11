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

Which means that if scaled_pt (spt) is some multiple of q then dp = 0. Now, I did this and bruteforced from 0 to 30, but received unexpected (yet later welcomed) results. Running the following function provided this output:
```
FINDING Q AND T
iter:  1        i:  2    True
iter:  2        i:  4    True
iter:  3        i:  8    True
iter:  4        i:  16   True
iter:  5        i:  32   True
iter:  6        i:  64   True
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

## Prime Guesser 2

