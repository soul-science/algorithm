def orderPrimeFilter(numbers):
    primes = []
    for number in numbers:
        flag = False
        for each in range(2, number//2+1):
            if number % each == 0:
                flag = True
                break
        if flag == False:
            primes.append(number)

    return primes



