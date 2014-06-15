# -*- coding: utf-8 -*-
import math
from generation.models import Prime

def generate_primes(mn, mx):
    primes = Prime.get_values()
    if not primes:
        Prime.objects.get_or_create(value=2)
        primes = [2]
    n = len(primes)

    def is_prime(p):
        for i in primes:
            if i * i > p:
                return True
            if p % i == 0:
                return False
        return True

    x = primes[-1] + 1
    while x < math.sqrt(mx):
        while not is_prime(x):
            x += 2
        primes += [x]
        x += 2

    def sieve(mn, mx):
        f = (mx - mn + 1) * [True]
        if mn == 1:
            f[0] = False
        for p in primes:
            if p ** 2 > mx:
                break
            for i in range(max(2 * p, mn - 1 - (mn - 1) % p + p), mx + 1, p):
                f[i - mn] = False
        return [i for i in range(mn, mx + 1) if f[i - mn]]

    primes += sieve(primes[-1]+1, mx)
    for val in primes[n:]:
        Prime.objects.get_or_create(value=val)
