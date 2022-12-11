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
*n
*q
*t
*poly_mod
*pk [List of two lists]
*sk
What I gathered was the following graph for encryption:
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
  Now, this looks quite complicated, and that's because it is. However, this is not even the beginning of the pain that I went through, because in order to calculate ct0 and ct1 three important functions were called: polymul, polydiv, and, polyadd. These functions are almost normal in that they are named after polynomial multiplication, polynomial division, and polynomial addition; however, their implementation is not so simple, and what is even more confusing is that polydiv is *called* in polymul and polyadd. Why is this? I have no clue, and I never did find out why. However, what I did start to attempt was writing down the encryption equations to see if they were solvable, and who would have guessed that they weren't. Or atleast, not in a way that didn't involve bruteforcing. Therefore, I will leave it as a mystery of the universe, because shortly after confusing myself with all of this information and more I decided that I would simply take a break and come back later.
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
  Yet again, it is complicated, but less so, and where did the random variables from the encryption go? The lack of specific key in this decryption gave me hints that all the random number stuff was just to throw me off. However, what is even more exciting about the decryption function is how simple it is, and how when using menu option 1 I am able to determine the first digit of the encryption output. This gave me an idea, if I set ct
## Prime Guesser 2

