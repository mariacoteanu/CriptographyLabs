import ast

des_config = []


# iau din json perechile nume - matrice
def des_init():
    with open("config.json") as des_param_fisier:
        des_param = ast.literal_eval(des_param_fisier.read())
    des_param_fisier.close()
    return des_param


def blocuri_s(secv):
    bloc = array_split(secv, 6)
    rezultat = []
    for i in range(8):
        s_curent = des_config['S' + chr(ord('0') + i + 1)]
        bloc_curent = bloc[i]
        lin = int(str(bloc_curent[0]) + str(bloc_curent[5]), 2)
        col = int(''.join([str(x) for x in bloc_curent[1:5]]), 2)
        aux = ''.join(format(s_curent[lin][col], '04b'))
        rezultat += [int(x) for x in aux]
    return rezultat


# textul de input e impartit in doua bucati a cate 32, iar o jumate trebuie expandata la 48
# pentru a fi folosita impreuna cu o parte din cheie care e de 48
def expand(bloc):
    return [bloc[poz - 1] for poz in des_config["E"]]


def aplic_xor(lista1, lista2):
    return [a ^ b for a, b in zip(lista1, lista2)]


# cheia suporta o permutare binara, dar trebuie transformata din string in array
def transform_string_in_bitarray(string):
    return list(int(i) for i in (''.join(format(ord(character), '08b') for character in string)))


# apoi, cheia din array o transform inapoi in string
def transform_bitarray_in_string(bitarray):
    split_bit_array = array_split(bitarray, 8)
    return ''.join([chr(int(val, 2)) for val in [''.join([str(bit) for bit in bits]) for bits in split_bit_array]])


# din array-ul mare trebuie sa il impart din pas in pas
def array_split(bitarray, pas):
    return [bitarray[k:k + pas] for k in range(0, len(bitarray), pas)]


# cheia trebuie permutata
def permute(bloc, permutare):
    return [bloc[poz - 1] for poz in permutare]


def permutare_la_stanga(lista1, lista2, pas):
    return lista1[pas:] + lista1[:pas], lista2[pas:] + lista2[:pas]


# primul pas dupa citirea cheii este permutarea ei
def permutarea_cheii(cheia_initiala):
    chei = []
    cheie_bit = permute(cheia_initiala, des_config["PC1"])
    jumate1, jumate2 = array_split(cheie_bit, 28)
    for i in range(16):
        if i in [0, 1, 8, 15]:
            first_half, second_half = permutare_la_stanga(jumate1, jumate2, 1)
        else:
            first_half, second_half = permutare_la_stanga(jumate1, jumate2, 2)
        chei.append(permute(first_half + second_half, des_config["PC2"]))
    return chei


# functia de criptare des
def des_encryption(plaintext, cheie_curenta):
    if len(plaintext) % 8 != 0:
        raise Exception("Textul initial nu e multiplu de 8! Numara caracterele")
    text_blocks = array_split(plaintext, 8)
    cheie_generata = permutarea_cheii(cheie_curenta)
    criptotext = []
    for bloc in text_blocks:
        bloc = transform_string_in_bitarray(bloc)
        bloc = permute(bloc, des_config["IP"])
        jumate1, jumate2 = array_split(bloc, 32)
        for j in range(16):
            nouajumate1 = jumate2
            nouajumate2 = aplic_xor(cheie_generata[j], expand(jumate2))
            nouajumate2 = blocuri_s(nouajumate2)
            nouajumate2 = permute(nouajumate2, des_config["P"])
            nouajumate2 = aplic_xor(nouajumate2, jumate1)
            jumate1 = nouajumate1
            jumate2 = nouajumate2
        criptotext += permute(jumate2 + jumate1, des_config["IP-1"])
    return transform_bitarray_in_string(criptotext)


# functia de decriptarea des
def des_decryption(criptotext, cheie_curenta):
    text_blocks = array_split(criptotext, 8)
    generated_keys = permutarea_cheii(cheie_curenta)
    plaintext = []
    for bloc in text_blocks:
        bloc = transform_string_in_bitarray(bloc)
        bloc = permute(bloc, des_config["IP"])
        jumate1, jumate2 = array_split(bloc, 32)
        for j in range(15, -1, -1):
            nouajumate1 = jumate2
            nouajumate2 = aplic_xor(generated_keys[j], expand(jumate2))
            nouajumate2 = blocuri_s(nouajumate2)
            nouajumate2 = permute(nouajumate2, des_config["P"])
            nouajumate2 = aplic_xor(nouajumate2, jumate1)
            jumate1 = nouajumate1
            jumate2 = nouajumate2
        plaintext += permute(jumate2 + jumate1, des_config["IP-1"])
    return transform_bitarray_in_string(plaintext)


def double_des_encryption(plaintext, cheie1, cheie2):
    criptotext_partial = des_encryption(plaintext, cheie1)
    return des_encryption(criptotext_partial, cheie2)


def double_des_decryption(criptotext, cheie1, cheie2):
    plaintext_partial = des_decryption(criptotext, cheie1)
    return des_decryption(plaintext_partial, cheie2)


if __name__ == "__main__":
    des_config = des_init()   # i receive the dictionary from json
    cheie1 = "cavaleri"
    cheie2 = "cheiescr"
    print("Introduceti textul de criptat(lungime multiplu de 8): ")
    text = input()
    text_criptat = double_des_encryption(text, transform_string_in_bitarray(cheie1), transform_string_in_bitarray(cheie2))
    text_decriptat = double_des_decryption(text_criptat, transform_string_in_bitarray(cheie2), transform_string_in_bitarray(cheie1))
    print("Initial: " + text)
    print("Criptat: " + text_criptat)
    print("Decriptat: " + text_decriptat)
