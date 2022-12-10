from pwn import *
import numpy as np
from numpy.polynomial import polynomial as poly
import re
from math import log2

address = "kitctf.me"
port = 4747
conn = remote(address, port)

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

def get_factors_alt(number):
    factors = set()
    for i in range(1, number+1):
        if number%i==0:
            factors.add(i)
    return factors

def polymul(x, y, modulus, poly_mod):
    return np.int64(
        np.round(poly.polydiv(poly.polymul(x, y) % modulus, poly_mod)[1] % modulus)
        )

def polyadd(x, y, modulus, poly_mod):
    return np.int64(
        np.round(poly.polydiv(poly.polyadd(x, y) % modulus, poly_mod)[1] % modulus)
    )

def listToBytes(list):
    output = ''.join([str(l) + "," for l in list])[:-1]
    return bytes(output, "utf-8")

def findQandT(size, maxI):
    falseFound = False
    Q = -1
    T = -1

    Ti = 0
    for i in [2**i for i in range(1, maxI)]:
        conn.sendline(b'0')
        conn.recvline()
        ct = []
        ct.append([0])
        ct.append([0] * size)
        ct[0] = [i]*64
        conn.sendline(listToBytes(ct[0]))
        conn.recvline()
        conn.sendline(listToBytes(ct[1]))
        orcStr = conn.recvline(keepends=False).decode('utf-8')
        orc = False
        if orcStr == "True":
            orc = True

        print("iter: ", int(log2(i)), "\ti: ", i, "\t", orc)
        if not orc and not falseFound:
            falseFound = True
            Ti = int(log2(i))
        if falseFound and orc:
            Q = i
            T = 2**(int(log2(i))-Ti)
            break
        conn.recvline()
    return Q, T

def findSK(size, q):
    sk_guess_str = ""
    for i in range(size):
        conn.sendline(b'0')
        conn.recvline()
        ct = []
        ct.append([0] * size)
        ct.append([0] * size)
        ct[1][i] = int(round(q*2/3))
        conn.sendline(listToBytes(ct[0]))
        conn.recvline()
        conn.sendline(listToBytes(ct[1]))
        orcStr = conn.recvline(keepends=False).decode('utf-8')
        orc = 1
        if orcStr == "True":
            orc = 0
        print("iter: ", i, "\t", orcStr, "\t", orc)
        sk_guess_str += str(orc)
        conn.recvline()
        ct[1][i] = 0
    sk_guess_str = sk_guess_str[::-1]
    sk_guess_str = sk_guess_str[-1] + sk_guess_str[0:-1]
    sk_guess = [int(i) for i in sk_guess_str]
    return sk_guess

def stringToList(str):
    regex = R"\w*[^[,\s\]]"
    matches = re.findall(regex, str)
    num = [int(m) for m in matches]
    return num

def decrypt(sk, size, q, t, poly_mod, ct):
    scaled_pt = polyadd(
        polymul(ct[1], sk, q, poly_mod),
        ct[0], q, poly_mod
    )
    decrypted_poly = np.round(scaled_pt * t / q) % t
    return int(decrypted_poly[0])

def makeListComparable(list):
    output = ""
    for ele in list:
        output += str(ele)
    return output

def listToString(list):
    return ''.join([str(i) + "," for i in list])[:-1]

if __name__ == "__main__":
    # CURRENT ENCRYPTED NUMBER
    ct0_str = conn.recvline(keepends=False).decode('utf-8')
    ct1_str = conn.recvline(keepends=False).decode('utf-8')
    ct0 = stringToList(ct0_str)
    ct1 = stringToList(ct1_str)
    ct = [ct0, ct1]

    arrSize = len(ct1)
    conn.recvline()

    # POLYNOMIAL MOD
    poly_mod = np.array([1] + [0] * (arrSize-1) + [1])

    # FIND Q and T
    print("FINDING Q AND T")
    q, t = findQandT(arrSize, 40)
    print("Q:\t", q)
    print("T:\t", t)
    if q == -1 or t == -1:
        print("Unexpected value of q or t")
        print("\tQ:\t", q)
        print("\tT:\t", t)
        exit()

    # FIND SK
    conn.recvline()
    print("FINDING SK")
    sk = findSK(arrSize, q)
    # print("LEN SK:\t", len(sk))
    print("SK: ",makeListComparable(sk))

    for i in range(100):
        conn.sendline(b'1')
        conn.recvline()
        num = decrypt(sk, arrSize, q, t, poly_mod, ct)
        factors = get_factors(num)
        factors_str = listToString(list(factors))
        print("Factors:\t", factors_str)
        factors_bytes = bytes(factors_str, 'utf-8')
        if i == 99:
            conn.sendline(factors_bytes)
            flag = conn.recvline(keepends=False).decode('utf-8')
            print(flag)
        else:
            conn.sendline(factors_bytes)
            ct0_str = conn.recvline(keepends=False).decode('utf-8')
            ct1_str = conn.recvline(keepends=False).decode('utf-8')
            ct0 = stringToList(ct0_str)
            ct1 = stringToList(ct1_str)
            ct = [ct0, ct1]
            conn.recvline()
