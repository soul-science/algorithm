# O(logn)
def fastMultiplier(a, b):
    s = 0

    while b != 0:
        if b & 1:
            s += a
        a = a << 1
        b = b >> 1

    return s

'''# log(n-1)
def log3Multiplier(a, b):
    len1 = len(str(a))
    len2 = len(str(b))
    a1 = a // (len1 // 2)
    a2 = a % (len1 // 2)
    b1 = b // (len2 // 2)
    b2 = b % (len2 // 2)
    print(fastMultiplier(a1, 10**(len1//2)))
    print(fastMultiplier(fastMultiplier(a1 - a2, b2 - b1)))

    return fastMultiplier(a1, 10**(len1//2)) + fastMultiplier(fastMultiplier(a1 - a2, b2 - b1)+ fastMultiplier(a1, b1) +
fastMultiplier(a2, b2), 10**(len1//2)) + fastMultiplier(a2, b2)
'''
