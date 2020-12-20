def fastPower(x, n):
    s = 1

    while n != 0:
        if n & 1:
            s *= x
            
        x *= x
        n = n >> 1

    return s


