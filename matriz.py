# coding: utf-8
from __future__ import print_function
from __future__ import division

from sys import stderr

import numpy as np
from itertools import chain
from numpy import array, ones, eye, subtract
from random import choice
from functools import reduce

chosen_type = object

# Sendo n o número de candidatos, p=100 a quantida de números primos, teremos
# `n² - n - 2p = 0` -> |n|<15
# Portanto, suficiente para até 14 candidatos:
_100_primos_ = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
    61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131,
    137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197,
    199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271,
    277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
    367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
    449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]


def fiat_valid_matrix(dim):
    pre = subtract(ones([dim, dim], dtype=chosen_type), eye(dim, dtype=chosen_type))

    for i, linha in enumerate(pre):
        for j, v in enumerate(linha):
            if v == 1 and j > i:
                pre[i, j] = choice([1, 0])
                pre[j, i] = 1 - pre[i, j]

    return pre


def is_valid(matrix, qtd_eleitores=1):
    for i, linha in enumerate(matrix):
        for j, v in enumerate(linha):
            if j != i and j > i:
                if not matrix[i, j] + matrix[j, i] == qtd_eleitores:
                    return False
    return True


def convert_2_number(matrix):
    matrix = array(matrix, dtype=chosen_type)
    primos = iter(_100_primos_)
    for i, linha in enumerate(matrix):
        for j, valor in enumerate(linha):
            if j > i:
                matrix[i, j] = next(primos) ** matrix[i, j]
            else:
                matrix[i, j] = 1
    # print(matrix)
    return reduce(lambda x, y: x * y, chain.from_iterable(matrix))


def decompose(valor):
    compostos = []
    for i in _100_primos_:
        while valor % i == 0:
            valor = valor // i
            compostos.append(i)
        if valor == 1:
            break
    return sorted(compostos)


def convert_2_matrix(escolhas, dim, qtd_eleitores=1):
    pre = ones([dim, dim], dtype=chosen_type)
    primos = iter(_100_primos_)
    clean_escolhas = escolhas[:]

    for i, linha in enumerate(pre):
        for j, coluna in enumerate(linha):
            if i == j:
                pre[i, j] = 0
            if j > i:
                p = next(primos)

                qtd = len([v for v in clean_escolhas if v == p])
                pre[i, j] = p ** qtd
                if pre[i, j] > 1:
                    clean_escolhas = clean_escolhas[qtd:]

                if pre[i, j] not in (0, 1):
                    contador = 0
                    while pre[i, j] % p == 0:
                        pre[i, j] = pre[i, j] // p
                        contador += 1
                    pre[i, j] = contador
                else:
                    pre[i, j] = 0
                pre[j, i] = abs(pre[i, j] - qtd_eleitores)

    return pre


##########################################
## Teste para 1 cédula

cedula = fiat_valid_matrix(5)                           # Cria cédula-matriz aleatória válida
print(cedula)
convertido = convert_2_number(cedula)                   # Converte em cédula-número
print(convertido)

_escolhas_ = decompose(convertido)
print(_escolhas_)                                       # Mostra os primos referentes às escolhas

recuperado = convert_2_matrix(_escolhas_, 5)
print(recuperado)                                       # Mostra cédula-matriz recuperada da cédula-número

assert np.all(recuperado == cedula)                     # Verifica se a cédula-matriz recuperada é identica à original

print('\n', '#'*60, '\n')

##########################################
## Teste para 1 urna

for n in range(100):
    n_candidatos = 14
    n_eleitores = 20

    cedulas = [fiat_valid_matrix(n_candidatos) for k in range(n_eleitores)]
    print(cedulas)

    somatorio = sum(cedulas)
    print(somatorio)

    convertidos = [convert_2_number(cedula) for cedula in cedulas]
    urna_numerica = reduce(lambda x, y: x * y, convertidos)
    print(urna_numerica)

    # if urna_numerica < 0:  # Caso de overflow
    #     exit(0)

    votos_separados = decompose(urna_numerica)
    print(votos_separados)

    recuperado = convert_2_matrix(votos_separados, n_candidatos, qtd_eleitores=n_eleitores)
    print(recuperado)

    print(is_valid(recuperado, qtd_eleitores=n_eleitores))

    try:
        assert np.all(recuperado == somatorio)
    except AssertionError as e:
        print(somatorio == recuperado)
        print(e, file=stderr)
        print(somatorio)
        print(recuperado)
        print(n)
        raise e
