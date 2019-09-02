

def chequear(fila, reinas, n):
    for i in range(fila):
        if ((reinas[i] == reinas[fila])or
                (abs(fila - i) == abs(reinas[fila] - reinas[i]))):
            return False
    return True


def imprimirTablero(reinas):
    for i in range(len(reinas)):
        for j in range(len(reinas)):
            if (reinas[i] == j):
                print("#", end=" ")
            else:
                print("0", end=" ")
        print("\n", end="")


def ponerreina(fila, reinas, n):
    finalizo = False
    if (fila < n):
        print("a")
        while((reinas[fila] < n - 1) and not finalizo):
            print("a")
            reinas[fila] = reinas[fila] + 1
            print(reinas)
            if (chequear(fila, reinas, n)):
                finalizo = ponerreina(fila + 1, reinas, n)
                if not finalizo:
                    reinas[fila + 1] = -1
                    
    else:
        finalizo = True
        imprimirTablero(reinas)
    return finalizo


def Nreinas(n):
    fila = 0
    reinas = []
    for i in range(n):
        reinas = reinas + [-1]
    if n > 0:
        print(reinas)
        ponerreina(fila, reinas, n)


if __name__ == '__main__':
    n = int(input("Ingrese la cantidad de reinas: "))
    Nreinas(n)
    input("esperar")
