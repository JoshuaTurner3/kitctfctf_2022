

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