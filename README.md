# Writeup for KITCTF 2022 'Prime Guesser 1' and 'Prime Guesser 2' Challenges
##Introduction
  This is a brief explanation of the process that I went through in order to solve the 'Prime Guesser 1' and 'Prime Guesser 2' challenges for KITCTF 2022. The explanation is simplified and does not discuss all the different tangents I went down to solve these challenges; however, a majority of the work is preserved in the various files of './crypto_prime_guesser_1/' if you would like to explore those yourself. The three "solution" files are working versions of the code solved local, using process, and using remote. Coincidentally, Prime Guesser 1 & 2 have a solution that is the same between them and so my solution for Prime Guesser 1 allowed me to solve Prime Guesser 2 by changing 4 characters between the "solution_remote.py" of each challenge. I'm new to CTFs and this challenge took me a while but it was fun to get through and rewarding at the end, especially whenever the solution applied to both.

##Prime Guesser 1
###Beginning
  As with every CTF challenge, I started Prime Guesser 1 by downloading the relevant server file code and reading it relentllessly to understand what was ocurring in the program. Typically, this is pretty straightforward; however, for this challenge there were a lot of components to keep track of and I spent a while trying to understand each indivdual part in excrutiating detail. What I gathered was the following graph for encryption:
  ```mermaid
graph TD
    size--> m
    pt--> m

    q-->delta
    t-->delta

    m --> scaled_m
    delta --> scaled_m
    q--> scaled_m


    gen_normal_poly --> e1
    gen_normal_poly --> e2
    gen_binary_poly --> u

    pko --> ct0
    u --> ct0
    q --> ct0
    poly_mod --> ct0
    e1 --> ct0
    scaled_m --> ct0

    pk1 --> ct1
    u --> ct1
    q --> ct1
    poly_mod -->ct1
    e2 --> ct1
  ```

##Prime Guesser 2

