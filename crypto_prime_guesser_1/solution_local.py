#!/usr/bin/env python3

import numpy as np
from numpy.polynomial import polynomial as poly
import random
from math import log2
import re

def polymul(x, y, modulus, poly_mod):
    return np.int64(
        np.round(poly.polydiv(poly.polymul(x, y) % modulus, poly_mod)[1] % modulus)
    )


def polyadd(x, y, modulus, poly_mod):
    return np.int64(
        np.round(poly.polydiv(poly.polyadd(x, y) % modulus, poly_mod)[1] % modulus)
    )

def gen_binary_poly(size):
    return np.random.randint(0, 2, size, dtype=np.int64)


def gen_uniform_poly(size, modulus):
    return np.random.randint(0, modulus, size, dtype=np.int64)


def gen_normal_poly(size):
    return np.int64(np.random.normal(0, 2, size=size))

def keygen(size, modulus, poly_mod):
    sk = gen_binary_poly(size)
    a = gen_uniform_poly(size, modulus)
    e = gen_normal_poly(size)
    b = polyadd(polymul(-a, sk, modulus, poly_mod), -e, modulus, poly_mod)
    return (b, a), sk

def encrypt(pk, size, q, t, poly_mod, pt):
    m = np.array([pt] + [0] * (size - 1), dtype=np.int64) % t
    delta = q // t
    scaled_m = delta * m  % q
    e1 = gen_normal_poly(size)
    e2 = gen_normal_poly(size)
    u = gen_binary_poly(size)
    ct0 = polyadd(
            polyadd(
                polymul(pk[0], u, q, poly_mod),
                e1, q, poly_mod),
            scaled_m, q, poly_mod
        )
    ct1 = polyadd(
            polymul(pk[1], u, q, poly_mod),
            e2, q, poly_mod
        )
    return (ct0, ct1)


def decrypt(sk, size, q, t, poly_mod, ct):
    scaled_pt = polyadd(
            polymul(ct[1], sk, q, poly_mod),
            ct[0], q, poly_mod
        )
    decrypted_poly = np.round(scaled_pt * t / q) % t
    return int(decrypted_poly[0])

def get_factors(number):
    factors = set()
    for i in [2, 3, 5, 7, 11, 13, 15, 17, 19, 23]:
        if i >= number:
            break
        if (number % i == 0):
            factors.add(i)
            other = number // i
            prime_set = get_factors(other)
            if len(prime_set) == 0:
                factors.add(other)
            else:
                for num in prime_set:
                    factors.add(num)
            
    return factors

# polynomial modulus degree
# n = 2**6
n = 2**8
# ciphertext modulus
# q = 2**20
q = 2**32
# plaintext modulus
# t = 2**10
t = 2**12
# polynomial modulus
poly_mod = np.array([1] + [0] * (n - 1) + [1])
pk, sk = keygen(n, q, poly_mod)


def oracle(c):
    p = decrypt(sk, n, q, t, poly_mod, c)
    print(p == 0)

def smart_enrypt(p):
    if p > 0 and p < 25:
        return encrypt(pk, n, q, t, poly_mod, p)

def loose():
    print("Failed")
    exit()

def outputCipher(c):
    print(''.join([str(l) + "," for l in c[0]])[:-1])
    print(''.join([str(l) + "," for l in c[1]])[:-1])


# MY FUNCTIONS

def findSKLocal(size, q):
    sk_guess_str = ""
    for i in range(size):
        ct = []
        ct.append([0] * size)
        ct.append([0] * size)
        ct[1][i] = int(round(q*2/3))
        orcRes = oracleLocal(ct)
        orc = 1
        if orcRes:
            orc = 0
        # print("iter: ", i, "\t", orcRes, "\t", orc)
        sk_guess_str += str(orc)
        ct[1][i] = 0
    sk_guess_str = sk_guess_str[::-1]
    sk_guess_str = sk_guess_str[-1] + sk_guess_str[0:-1]
    sk_guess = [int(i) for i in sk_guess_str]
    return sk_guess

def findQandT(size, maxI):
    falseFound = False
    Q = -1
    T = -1
    Ti = 0
    for i in [2**i for i in range(1, maxI)]:
        ct = []
        ct.append([0])
        ct.append([0] * size)
        ct[0] = [i]*64
        orcStr = oracleLocalString(ct)
        orc = False
        if orcStr == "True":
            orc = True

        # print("iter: ", int(log2(i)), "\ti: ", i, "\t", orc)
        if not orc and not falseFound:
            falseFound = True
            Ti = int(log2(i))
        if falseFound and orc:
            Q = i
            T = 2**(int(log2(i))-Ti)
            break
    return Q, T

def oracleLocal(c):
    p = decrypt(sk, n, q, t, poly_mod, c)
    return p==0

def oracleLocalString(c):
    p = decrypt(sk, n, q, t, poly_mod, c)
    return str(p==0)

def outputCipherLocal(c):
    ct0_str = ''.join([str(l) + "," for l in c[0]])[:-1]
    ct1_str = ''.join([str(l) + "," for l in c[1]])[:-1]
    return ct0_str, ct1_str

def stringToList(str):
    regex = R"\w*[^[,\s\]]"
    matches = re.findall(regex, str)
    num = [int(m) for m in matches]
    return num

def listToString(list):
    return ''.join([str(i) + "," for i in list])[:-1]


first_iter = True
size_local = 0
q_local = 0
t_local = 0
sk_local = [0]
for _ in range(100):
    f = open("ct_analysis.txt", 'w')
    number = random.randint(11, 200)
    
    ct = encrypt(pk, n, q, t, poly_mod, number)
    ct0_str, ct1_str = outputCipherLocal(ct)
    ct0 = stringToList(ct0_str)
    ct1 = stringToList(ct1_str)
    ct_local = [ct0, ct1]

    assert(ct[0] == ct_local[0]).all()
    assert(ct[1] == ct_local[1]).all()

    if first_iter:
        first_iter = False
        size_local = len(ct1)
        assert n == size_local

        poly_mod_local = np.array([1] + [0] * (size_local-1) + [1])
        assert (poly_mod_local == poly_mod).all()

        q_local, t_local = findQandT(size_local, 40)
        assert q_local == q
        assert t_local == t

        sk_local = findSKLocal(size_local, q)
        assert (sk_local == sk).all()

    number_local = decrypt(sk_local, size_local, q_local, t_local, poly_mod_local, ct_local)
    assert number == number_local
    
    real_factors = get_factors(number)
    factors_local = get_factors(number_local)
    assert real_factors == factors_local

    primes = listToString(list(factors_local)).strip()
    if len(primes) == 0:
        if len(real_factors) == 0:
            continue
        else:
            loose()

    primes_set = set()
    for num in primes.split(","):
        primes_set.add(int(num, 10))
    
    if not (real_factors == primes_set):
        loose()

print("You won: Flag")