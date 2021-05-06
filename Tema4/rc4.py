import codecs
from random import randrange, randint

MOD = 256


def init(key, l):
    S = []
    for i in range(0, 256):
        S.append(i)
    j = 0
    for i in range(0, 256):
        j = (j + S[i] + key[i % l]) % MOD
        S[i], S[j] = S[j], S[i]
    return S


def Trans(S):
    i = 0
    j = 0
    while True:
        i = i + 1
        j = S[i]
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % MOD]
        yield K


def generator(key, l):
    S = init(key, l)
    return Trans(S)


def criptare_plaintext(key, plaintext, l, CONTOR, ok):
    plaintext = [ord(c) for c in plaintext]
    return criptare(key, plaintext, l, CONTOR, ok)


def criptare(key, text, l, CONTOR, ok):
    key = [ord(c) for c in key]
    keystream = generator(key, l)
    res = []
    i = 1
    for c in text:
        x = next(keystream)
        val = ("%02X" % (c ^ x))  # XOR and taking hex
        if ok == 0:
            print(f'val = {val}')
        res.append(str(val))
        if i == 2 and ok == 0:
            ok=1
            if str(val) == str('00'):
                CONTOR = CONTOR+1
        i = i + 1
    return ''.join(res), CONTOR


def decriptare(key, ciphertext, l, CONTOR, ok):
    ciphertext = codecs.decode(ciphertext, 'hex_codec')
    res, CONTOR = criptare(key, ciphertext, l, CONTOR, ok)
    return codecs.decode(res, 'hex_codec').decode('utf-8')


def gen_key(l):
    for i in range(0, l):
        new = randint(0, 1)
        if i == 0:
            key = new
        else:
            key = str(key) + str(new)
    return key


def gen_plain(k):
    for i in range(0, k):
        new = randint(0, 9)
        if i == 0:
            plain = new
        else:
            plain = str(plain) + str(new)
    return plain


if __name__ == '__main__':
    k = randrange(5, 50)
    print(f'k: {k}')
    plaintext = gen_plain(k)
    print(f'plaintext: {plaintext}')
    # pasi = randrange(50, 129)  # cati pasi sa am
    pasi = 1000
    CONTOR = 0
    for i in range(0, pasi):
        print(f'\npas = {i + 1}')
        l = randrange(5, 17)
        print(f'l={l}')
        key = gen_key(l)
        print(f'key: {key}')
        ciphertext, CONTOR = criptare_plaintext(key, plaintext, l, CONTOR, 0)
        print(f'ciphertext: {ciphertext}')
        decodetext = decriptare(key, ciphertext, l, CONTOR, 1)
        print(f'decodetext: {decodetext}')

    print(f'\n Testare: ')
    print(f'1/128 = {1/128}')
    print(f'CONTOR={CONTOR}')
    print(f'pasi={pasi}')
    print(f'contor/pasi = {CONTOR/pasi}')