listaAberta = []  # Lista com as coordenadas que não tiveram seus vizinhos verificados
listaFechada = []  # Lista com as coordenadas que tiveram seus vizinhos verificados

def printLinha():
    print("-" * 150)

def desenhar(coordenadas, mapa, inicio, final, custototal):
    printLinha()
    print(f"Melhor caminho entre os pontos A e B:")
    print(f"Custo Total: {custototal}.")
    print(f"Coordenadas percorrida pelo caminho {coordDisplay(coordenadas)}")
    printLinha()
    direcao_cima = '^'
    direcao_baixo = 'v'
    direcao_esquerda = '<'
    direcao_direita = '>'
    direcao_obstaculo = '#'  # -1 no mapa
    direcao_livre = "-"
    direcao_inicio = 'A'
    direcao_final = 'B'
    resultado = []

    for i in mapa:
        resultado.append(i)

    atual = inicio
    direcao = ''

    for pos in range(1, len(coordenadas)):
        if (coordenadas[pos] != inicio):
            if atual[0] > coordenadas[pos][0]:
                direcao = direcao_cima
            elif atual[0] < coordenadas[pos][0]:
                direcao = direcao_baixo
            elif atual[1] > coordenadas[pos][1]:
                direcao = direcao_esquerda
            elif atual[1] < coordenadas[pos][1]:
                direcao = direcao_direita

            if coordenadas[pos] == final:
                x = coordenadas[pos - 1][0]
                y = coordenadas[pos - 1][1]
            else:
                x = coordenadas[pos][0]
                y = coordenadas[pos][1]
            resultado[x][y] = direcao
            atual = coordenadas[pos]

    resultado[inicio[0]][inicio[1]] = direcao_inicio
    resultado[final[0]][final[1]] = direcao_final
    for x in range(len(resultado)):
        for y in range(len(resultado[x])):
            if resultado[x][y] == -1:
                resultado[x][y] = direcao_obstaculo  # Custo infinito
            elif str(resultado[x][y]).isnumeric():
                resultado[x][y] = direcao_livre
    return resultado


def recuperar_caminho(atual, inicio):
    global posicoesCalculadas
    percurso = []
    if atual != inicio:
        pontoOrigem = posicoesCalculadas[atual][3]
    else:
        pontoOrigem = inicio

    percurso.append(atual)
    while pontoOrigem != inicio:
        percurso.append(pontoOrigem)
        pontoOrigem = posicoesCalculadas[pontoOrigem][3]
    if inicio not in percurso:
        percurso.append(inicio)

    percurso.reverse()
    return percurso


def encontra_vizinhos(mapa, atual, final, valmax):
    global listaFechada
    vizinhos = []
    linha_matriz = int(atual[0])
    coluna_matriz = int(atual[1])
    linha_final = int(final[0])
    coluna_final = int(final[1])
    if (((linha_matriz - 1) >= 0) and (mapa[linha_matriz - 1][coluna_matriz] != -1 and (
            mapa[linha_matriz - 1][coluna_matriz] <= valmax or (
            linha_matriz - 1 == linha_final and coluna_matriz == coluna_final)))):
        vizinho_cima = (linha_matriz - 1, coluna_matriz)
        if ((vizinho_cima not in listaFechada)):
            vizinhos.append(vizinho_cima)

    if (((linha_matriz + 1) <= len(mapa) - 1) and (mapa[linha_matriz + 1][coluna_matriz] != -1 and (
            mapa[linha_matriz + 1][coluna_matriz] <= valmax or (
            linha_matriz + 1 == linha_final and coluna_matriz == coluna_final)))):
        vizinho_baixo = (linha_matriz + 1, coluna_matriz)
        if ((vizinho_baixo not in listaFechada)):
            vizinhos.append(vizinho_baixo)

    if (((coluna_matriz - 1) >= 0) and (mapa[linha_matriz][coluna_matriz - 1] != -1 and (
            mapa[linha_matriz][coluna_matriz - 1] <= valmax or (
            linha_matriz == linha_final and coluna_matriz - 1 == coluna_final)))):
        vizinho_esquerda = (linha_matriz, coluna_matriz - 1)
        if ((vizinho_esquerda not in listaFechada)):
            vizinhos.append(vizinho_esquerda)

    if (((coluna_matriz + 1) <= len(mapa[0]) - 1) and (mapa[linha_matriz][coluna_matriz + 1] != -1 and (
            mapa[linha_matriz][coluna_matriz + 1] <= valmax or (
            linha_matriz == linha_final and coluna_matriz + 1 == coluna_final)))):
        vizinho_direita = (linha_matriz, coluna_matriz + 1)
        if ((vizinho_direita not in listaFechada)):
            vizinhos.append(vizinho_direita)
    return vizinhos

def calcula_custos(mapa, pai, vizinhos, final):
    global posicoesCalculadas
    for vizinho in vizinhos:
        heuristica = distanciaManhattan(vizinho, final)
        try:
            custo = posicoesCalculadas[pai][1] + mapa[vizinho[0]][
                vizinho[1]] + 1
        except:
            custo = 1
        posicoesCalculadas[vizinho] = (vizinho, custo, heuristica, pai)
    return posicoesCalculadas


def coordDisplay(coordenadas):
    newCoord = []
    for item in coordenadas:
        newItem = "(" + str(item[1]) + ", " + str(item[0]) + ")"
        newCoord.append(newItem)
    return newCoord

def criaMapa():
    matriz = []
    maxValor = 1
    arquivo = open("mapa.txt", "r")
    tamanho = arquivo.readline().strip().split()
    pontoPartida = arquivo.readline().strip().split()
    pontoPartida[0] = int(pontoPartida[0])
    pontoPartida[1] = int(pontoPartida[1])
    pontoPartida.reverse()
    for lin in range(0, int(tamanho[1])):
        linha = arquivo.readline().strip().split()
        matriz.append(linha)

    for i in range(int(tamanho[1])):
        for j in range(int(tamanho[0])):
            elemento = matriz[i][j]
            matriz[i][j] = int(elemento)
            if int(elemento) > maxValor:
                maxValor = matriz[i][j]

    return tamanho, pontoPartida, matriz, maxValor + 1


def distanciaManhattan(atual, final):
    return abs((final[0] - atual[0])) + abs((final[1] - atual[1]))

def buscar(mapa, inicio, final, maxValor):
    encontrado = False
    menorCusto = 100000
    caminhoCusto = []
    for max in range(0, maxValor):
        listaAberta.clear()
        posicoesCalculadas.clear()
        listaAberta.append(inicio)
        listaFechada.clear()
        encontrado = False
        while listaAberta != [] and encontrado == False:
            atual = listaAberta[0]
            vizinhos = encontra_vizinhos(mapa, atual, final, max)
            calcula_custos(mapa, atual, vizinhos, final)
            for vizinho in vizinhos:
                if (vizinho not in listaAberta):
                    listaAberta.append(vizinho)
            listaAberta.remove(atual)
            listaFechada.append(atual)

            if (final in listaFechada):
                encontrado = True
                caminho = recuperar_caminho(atual, inicio)
                custoTrajeto = custo(mapa, caminho)
                if (custoTrajeto < menorCusto):
                    menorCusto = custoTrajeto
                    caminhoCusto = caminho

    resultado = desenhar(caminhoCusto, mapa, inicio, final, menorCusto)
    return resultado

def custo(mapa, caminho):
    valorCusto = 0
    for i in caminho:
        valorCusto += int(mapa[i[0]][i[1]]) + 1
    return valorCusto-1

def entrada_de_dados_final(mapa):
    print("Exemplo de ponto de chegada (x,y): = '0 0'\n")
    while True:
        entrada = input("Entre com o ponto de chegada do trajeto: ")
        argumentos = tuple(entrada.split())
        linha = int(argumentos[1])
        coluna = int(argumentos[0])
        if mapa[linha][coluna] == -1:
            print('\nVocê escolheu um obstaculo como ponto de chegada, escolha novamente\n')
        else:
            final = (linha, coluna)
            return final


def main():
    tamanho, inicio, mapa, maxValor = criaMapa()
    final = entrada_de_dados_final(mapa)
    if (inicio == final):
        print("Você não pode escolher a posição inicial como final, escolha novamente")
    else:
        resultado = buscar(mapa, inicio, final, maxValor)
        for i in resultado:
            for j in i:
                print(j, end=" ")
            print()
        print()

    return 0

inicio = ()
final = ()
posicoesCalculadas = {}
main()