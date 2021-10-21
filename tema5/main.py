import math
import time
from random import randrange

import Crypto.Util.number

bits = 512


# == FOR ATTACK ==
def rational_to_contfrac(x, y):
    quotient = x // y
    continuous_fraction = [quotient]
    while y * quotient != x:
        x, y = y, x % y
        quotient = x // y
        continuous_fraction.append(quotient)
    return continuous_fraction


def check_criterion(l, d, n, e):
    find_d = {'found': False, 'private': {}}

    if l == 0 or d == 0:
        return find_d

    if d % 2 == 0:
        return find_d

    intermediary = e * d - 1
    if intermediary % l != 0:
        return find_d

    phi = intermediary // l

    a = 1
    b = (-1) * (n - phi + 1)
    c = n

    # x^2 - x * (n - phi + 1) + n
    delta = int(pow(b, 2) - 4 * a * c)
    if delta < 0:
        return find_d

    square_root_of_delta = math.isqrt(delta)
    if square_root_of_delta * square_root_of_delta == delta:
        p = int(-b - square_root_of_delta)
        q = int(-b + square_root_of_delta)
        if p % 2 == 0 and q % 2 == 0 and p > 0 and q > 0:
            p = int(p // 2)
            q = int(q // 2)
            find_d['found'] = True
            find_d['private']['d'] = d

    return find_d


def hack_RSA(e, n):
    found = False
    private_key = {}

    frac = rational_to_contfrac(e, n)
    alpha = [frac[0], frac[0] * frac[1] + 1]
    beta = [1, frac[1]]
    i = 0
    while not found:
        if i > 1:
            alpha.append(frac[i] * alpha[i - 1] + alpha[i - 2])
            beta.append(frac[i] * beta[i - 1] + beta[i - 2])
        l = alpha[i]
        d = beta[i]
        results = check_criterion(l, d, n, e)
        found = results['found']
        private_key = results['private']
        i += 1
    return private_key['d']


# == FOR RSA ==
def cmmdc(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def criptare(N, x, e):
    c = pow(x, e, N)
    return c


# metoda pt TCR
def mod2preExp(a, d, n, p, q):
    d1 = d % (p - 1)
    d2 = d % (q - 1)

    x1 = pow(a % p, d1, p)
    x2 = pow(a % q, d2, q)

    m1_inv = Crypto.Util.number.inverse(p, q)
    w = x1 + p * ((x2 - x1) * m1_inv % q)

    return w


def pereche_vulnerabila():
    p = Crypto.Util.number.getPrime(bits)
    q = Crypto.Util.number.getPrime(bits)
    while p <= q or p >= 2*q:
        p = Crypto.Util.number.getPrime(bits)
    return p, q


if __name__ == '__main__':

    p = Crypto.Util.number.getPrime(bits)
    print("\nRandom 512-bit Prime (p): ", p)
    q = Crypto.Util.number.getPrime(bits)
    print("Random 512-bit Prime (q): ", q)

    N = p * q
    print("N=p*q=", N)

    PHI = (p - 1) * (q - 1)
    print("PHI=(p-1)(q-1)=", PHI)

    e = randrange(1, pow(2, 32))
    while cmmdc(e, N) != 1:
        e = randrange(1, pow(2, 32))

    print("e=", e)
    d = Crypto.Util.number.inverse(e, PHI)
    print("d=", d)

    x = randrange(1, N)
    print("\nmesaj=", x)

    criptotext = criptare(N, x, e)
    print("criptare: ", criptotext)

    start = time.time()
    decriptat = criptare(N, criptotext, d)
    print("decriptare normala: ", decriptat)
    print("in  %.3f secunde." % (time.time() - start))
    start = time.time()

    if p < q:
        decriptare2 = mod2preExp(criptotext, d, N, p, q)
    else:
        decriptare2 = mod2preExp(criptotext, d, N, q, p)
    print("decriptare tip 2: ", decriptare2)
    print("in  %.3f secunde." % (time.time() - start))

    print("\n == WIENER ATTACK ==")
    print("NEW VALUES:")

    new_p, new_q = pereche_vulnerabila()
    print("new_p = ", new_p)
    print("new_q = ", new_q)

    new_n = new_p * new_q
    print("new_n = ", new_n)

    new_phi = (new_p-1)*(new_q-1)
    print("new_phi = ", new_phi)

    new_d = randrange(2, (math.isqrt(math.isqrt(new_n)) // 3))
    val = cmmdc(new_d, new_phi)
    while val != 1:
        new_d = randrange(2, (math.isqrt(math.isqrt(new_n)) // 3))
        val = cmmdc(new_d, new_phi)
    print("new_d = ", new_d)

    new_e = Crypto.Util.number.inverse(new_d, new_phi)
    print("new_e = ", new_e)

    start = time.time()
    hacked_d = hack_RSA(new_e, new_n)
    print("hacked_d = ", hacked_d)

    if new_d == hacked_d:
        print("Hack WORKED!")
    else:
        print("Hack FAILED")
    print("in  %.3f secunde." % (time.time() - start))
    print("----------FINAL---------------")
