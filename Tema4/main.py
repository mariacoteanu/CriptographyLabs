
def create_poly():
    c = []
    for i in range(0, 8):
        if i == 0 or i == 4 or i == 5 or i == 7:
            c.append(1)
        else:
            c.append(0)
    return c


def initialize(c):
    s = []
    for i in range(0, len(c)):
        if c[i] == 1:
            s.append(0)
        else:
            s.append(1)
    return s


def circuit(init, current):
    for i in range(0, len(init)):
        if init[i] != current[i]:
            return 0

    return 1


def new_line(c, old):
    current = []
    for i in range(0, len(c)-1):
        current.append(old[i+1])
    last = 0
    for j in range(0, len(c)):
        last = last + c[j]*old[j]

    current.append(last % 2)

    return current


def lfsr(c, init):
    file = open("LFSR.txt", "w")

    old = init
    pas = 1
    ok = 0
    solution = [init[0]]
    file.write(str(init[0]))
    while pas < 1024:
        current = new_line(c, old)
        print(f'Pas {pas}: {current}')
        if circuit(init, current) == 1 and ok == 0:
            print(f'\n We have circuit with length {pas}\n ')
            ok = 1
        solution.append(current[0])
        file.write(str(current[0]))
        old = current
        pas = pas + 1
    file.close()
    return solution


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    c = create_poly()
    print(c)
    init = initialize(c)
    print(f'Pas 0: {init}')
    print(lfsr(c, init))
    print( 2 ** len(c) - 1)

