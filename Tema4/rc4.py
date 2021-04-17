import secrets
from random import randrange, random

MOD = 256


def init(key, l):
    S = []
    for i in range(0,255):
        S[i] = i
    j = 0
    for i in range(0, 255):
        j = (j + S[i] + key[i % l]) % MOD
        S[i], S[j] = S[j], S[i]
    return S


def Trans(S):
    i = 0
    j = 0
    while True:
        i = i+1
        j = S[i]
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j])% MOD]
        yield K


def generator(key, l):
    S = init(key, l)
    return Trans(S)


if __name__ == '__main__':
    l = randrange(5, 17)
    print(f'lenght={l}')
    key = secrets.token_bytes(l)
    print(f'key: {key}')
    init(key, l)
