import numpy as np
from numpy.polynomial import polynomial as poly
import random
from pwn import *
from math import log2


def printDivider():
    output = ""
    for _ in range(100):
        output += "-"
    print("\n" + output + "\n")

def polymul(x, y, modulus, poly_mod):
    # X Component of multiplication
    # printDivider()
    # print("x: ", x)
    # print("y: ", y)
    # print("modulus: ", modulus)
    # print("poly_mod: ", poly_mod)
    
    # printDivider()

    # step1 = poly.polymul(x, y)
    # step2 = step1 % modulus
    # step3 = poly.polydiv(step2, poly_mod)
    # step4 = step3[1]%modulus
    # step5 = np.round(step4)
    # step6 = np.int64(step5)

    # print("Step 1:", step1)
    # print("Step 2:", step2)
    # print("Step 3:", step3[1])
    # print("Step 4:", step4)
    # print("Step 5:", step5)
    # print("Step 6:", step6)
    # printDivider()

    r =  np.int64(

        np.round(poly.polydiv(poly.polymul(x, y) % modulus, poly_mod)[1] % modulus)
    )

    # assert (r == step6).all()
    return r


def polyadd(x, y, modulus, poly_mod):
    return np.int64(
        np.round(poly.polydiv(poly.polyadd(x, y) % modulus, poly_mod)[1] % modulus)
    )

def gen_binary_poly(size):
    gbp =  np.random.randint(0, 2, size, dtype=np.int64)
    return gbp

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
    # print("m: ", m)
    delta = q // t
    scaled_m = delta * m  % q
    # print("scaled m: ", scaled_m)
    e1 = gen_normal_poly(size)
    e2 = gen_normal_poly(size)
    u = gen_binary_poly(size)

    ct0 = polyadd(
            polyadd(
                polymul(pk[0], u, q, poly_mod),
                e1, q, poly_mod
                ),
            scaled_m, q, poly_mod
        )

    ct1 = polyadd(
            polymul(pk[1], u, q, poly_mod),
            e2, q, poly_mod
        )

    return (ct0, ct1)

def decrypt(sk, size, q, t, poly_mod, ct):
    # printDivider()
    # print("sk: ", sk)
    # print(ct)
    s1 = polymul(ct[1], sk, q, poly_mod)
    # print("s1: ", s1)
    s2 = polyadd(s1, ct[0], q, poly_mod)
    # print("s2: ", s2)
    # scaled_pt = polyadd(
    #         polymul(ct[1], sk, q, poly_mod),
    #         ct[0], q, poly_mod
    #     )
    scaled_pt = s2
    decrypted_poly = np.round(scaled_pt * t / q) % t
    # print(decrypted_poly)
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
n = 2**6 # EXAMPLE !!! ON THE SERVER ARE OTHER NUMBERS
# ciphertext modulus
q = 2**24 # EXAMPLE !!! ON THE SERVER ARE OTHER NUMBERS
# plaintext modulus
t = 2**8 # EXAMPLE !!! ON THE SERVER ARE OTHER NUMBERS
# polynomial modulus
poly_mod = np.array([1] + [0] * (n - 1) + [1])
#print(poly_mod)
# pk1_proc = [295153, 318063, 721550, 125921, 481738, 223528, 574018, 547467, 256646, 962751, 644366, 869489, 868868, 706108, 450994, 825664, 870495, 538100, 567426, 512806, 430994, 832042, 745727, 342709, 866747, 983023, 86920, 374583, 545599, 36003, 857595, 981850, 938277, 1035846, 959352, 592661, 179368, 757498, 142456, 288879, 578995, 22909, 831574, 452067, 508905, 4717, 851791, 114752, 831498, 857001, 802619, 8985, 63489, 681703, 690247, 755253, 27693, 487639, 700663, 784510, 664167, 865831, 269974, 756534]
# pk2_proc = [933562, 404502, 755458, 382077, 647395, 215219, 785923, 12608, 687363, 132288, 468288, 1008616, 265713, 577978, 1017268, 375286, 1015901, 463063, 791722, 195084, 710357, 70173, 308240, 349347, 89492, 539002, 802219, 348837, 907004, 976272, 456965, 660836, 166987, 51094, 6839, 361013, 601012, 362817, 210168, 206540, 935826, 639068, 839885, 560091, 555489, 927414, 479100, 961229, 880993, 1005705, 909482, 566387, 752340, 81081, 639062, 613672, 78853, 723744, 958315, 471187, 1013018, 828324, 511730, 234033]
# sk_proc = [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0]
# pk1 = np.array(pk1_proc,dtype=np.int64)
# pk2 = np.array(pk2_proc,dtype=np.int64)
# pk = [pk1, pk2]
# sk = np.array(sk_proc)
pk, sk = keygen(n, q, poly_mod)

def oracle(c):
    p = decrypt(sk, n, q, t, poly_mod, c)
    return p==0

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

def listToBytes(list):
    output = ""
    for i in range(1, len(list)):
        output += str(list[i]) + ","
    output += str(list[-1])
    return bytes(output, "utf-8")

def oracleLocal(c):
    p = decrypt(sk, n, q, t, poly_mod, c)
    print("p: ", p)
    return p==0

def findQLocal(size, maxI):
    falseFound = False
    Q = 0
    for i in [2**i for i in range(1, maxI)]:
        ct = []
        ct.append([0])
        ct.append([0] * size)
        ct[0] = [i]*64
        orc = oracleLocal(ct)
        print("iter: ", int(log2(i)), "\ti: ", i, "\t", orc)
        if not orc and not falseFound:
            falseFound = True
        if falseFound and orc:
            print("Q = ", i)
            Q = i
            break
    return Q

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
        print("iter: ", i, "\t", orcRes, "\t", orc)
        sk_guess_str += str(orc)
        ct[1][i] = 0
    sk_guess_str = sk_guess_str[::-1]
    sk_guess_str = sk_guess_str[-1] + sk_guess_str[0:-1]
    sk_guess = [int(i) for i in sk_guess_str]
    return sk_guess

def numMatches(sk, sk_guess):
    count = 0
    for s, sg in zip(sk, sk_guess):
        if s == sg:
            count += 1
    return count


def compareStringRing(sk, sk_guess):
    sk_tmp = sk_guess
    matches = []
    for _ in range(len(sk)):
        sk_tmp = sk[-1] + sk[0:-1]
        matches.append(numMatches(sk, sk_tmp))
    print(matches)

def makeListComparable(list):
    output = ""
    for ele in list:
        output += str(ele)
    return output

# TESTS
if __name__ == "__main__":
    # number = 17
    # ct0_proc = [667610, 31041, 171161, 303023, 750048, 753945, 838913, 537618, 325755, 578608, 398466, 912720, 642587, 242804, 877094, 152175, 136101, 511713, 743438, 997632, 39103, 360922, 29456, 361726, 136382, 85215, 185896, 918562, 153974, 301995, 772377, 1038340, 196576, 747717, 181097, 306875, 274612, 1019081, 352025, 1013620, 56240, 683489, 83802, 368410, 692244, 624846, 556969, 354298, 1035558, 910360, 938230, 310424, 644108, 436177, 469068, 177163, 781684, 922129, 220170, 484754, 717648, 365830, 717218, 176830]
    # ct1_proc = [704458, 875906, 851725, 295587, 226517, 396202, 767292, 766820, 585332, 809088, 919595, 624276, 516125, 683687, 25593, 850837, 278074, 960474, 458371, 59643, 100060, 270168, 259519, 357490, 641263, 620749, 294256, 485527, 979297, 809470, 222625, 200148, 1034263, 887474, 3647, 557866, 1000522, 464134, 418303, 95381, 535689, 472322, 357643, 479951, 732627, 770149, 45838, 44661, 175932, 146454, 501815, 608380, 117720, 917388, 879010, 376142, 185298, 740527, 849674, 387961, 892869, 706320, 599212, 845681]
    # ct0 = np.array(ct0_proc, dtype=np.int64)
    # ct1 = np.array(ct1_proc, dtype=np.int64)
    # ct = [ct0, ct1]
    # d = decrypt(sk, n, q, t, poly_mod, ct)
    # findQLocal(64, 30)
    # print(sk)
    # f = open("sk_analysis.txt", 'w')
    # ct = []
    # ct.append([0] * 64)
    # ct.append([0] * 64)
    # output = []
    # sk_guess = ""
    # ds = []
    # for i in range(64):
    #     ct[1][i] = q*2/3

    #     s = polymul(ct[1], sk, q, poly_mod)
    #     s = polyadd(s, ct[0], q, poly_mod)
    #     d = np.round(s*t/q)%t
    #     d = int(d[0])
    #     ds.append(d)
    #     if s[0] > 1:
    #         sk_guess += str(int(s[0]/s[0]))
    #     else:
    #         sk_guess += str(s[0])

    #     curLine = "[ "
    #     for b in s:
    #         if b > 1:
    #             b_new = int(b / b)
    #             curLine += str(b_new) + " "
    #         else:
    #             curLine += str(b) + " "
    #     curLine += "]\n"
    #     output.append(curLine)

    #     ct[1][i] = 0
    # print(ds)
    # sk_out_analysis = "[ "
    # for s in sk:
    #     sk_out_analysis += str(s) + " "
    # sk_out_analysis += "]\n"
    # f.write("SK:\n" + str(sk_out_analysis) + "\n\n")
    # for out in output:
    #     f.write(out)

    # f.close()
    # sk_out = ""
    # for s in sk:
    #     sk_out += str(s)
    # print(sk_out)
    # print(sk_guess[::-1])
    # compareStringRing(sk_out, sk_guess)
    # print(sk)
    # print(test)
    #print(oracleLocal(ct))
    sk_guess = findSKLocal(64, q)
    print(makeListComparable(sk))
    print(makeListComparable(sk_guess))