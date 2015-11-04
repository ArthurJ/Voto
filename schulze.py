import ballot
import numpy as np

__author__ = '@arthurj'


def gen_grafo(candidate_list, preferencias):
    grafo = {i: [] for i in candidate_list}
    qtd_candidatos = len(candidate_list)
    for i in range(qtd_candidatos):
        for j in range(qtd_candidatos):
            if i == j:
                continue
            if preferencias[i, j] > 0:
                grafo[candidate_list[i]].append(candidate_list[j])
    grafo = dict((i, grafo[i]) for i in grafo if len(grafo[i]) > 0)
    return grafo


def result(qtd_candidates, strong_path_matrix, candidate_list):
    path = dict()
    maior_valor = 0
    qtd_vitorias = {i: 0 for i in candidate_list}
    for i in range(qtd_candidates):
        for j in range(i, qtd_candidates):
            if i == j:
                continue
            order = candidate_list[i], candidate_list[j]
            value = strong_path_matrix[i, j]
            if strong_path_matrix[i, j] < strong_path_matrix[j, i]:
                order = candidate_list[j], candidate_list[i]
                value = strong_path_matrix[j, i]
            path[order[0] + ' -> ' + order[1]] = value
            qtd_vitorias[order[0]] += 1
            maior_valor = value if value > maior_valor else maior_valor

    maior_valor = str(len(str(maior_valor)) + 4)
    print('Matriz de preferências:\n')
    for row in strong_path_matrix:
        for val in row:
            print(('{:' + maior_valor + '}').format(val), end='')
        print()
    print('\n\n')

    print('Quantidade de Vitórias:\n')
    for i in candidate_list:
        print(i.ljust(60, '_'),
              str(qtd_vitorias[i]), '({:.3f}%)'.format(100 * qtd_vitorias[i] / (qtd_candidates - 1)))
    print('\n')


def floyd_warshall_strongest(numero_candidatos, matriz_preferencias):
    strong_path = np.zeros((numero_candidatos, numero_candidatos), dtype=np.int)
    for i in range(numero_candidatos):
        for j in range(numero_candidatos):
            if i != j:
                if matriz_preferencias[i, j] > matriz_preferencias[j, i]:
                    strong_path[i, j] = matriz_preferencias[i, j]

    for i in range(numero_candidatos):
        for j in range(numero_candidatos):
            if i == j:
                continue
            for k in range(numero_candidatos):
                if i != k and j != k:
                    strong_path[j, k] = max(strong_path[j, k], min(strong_path[j, i], strong_path[i, k]))

    return strong_path


if __name__ == "__main__":
    candidatos_list = ballot.load_candidates()
    votosList = ballot.load_ballot_file()

    # qtd_vencedores = 2
    qtd_cadidatos = len(candidatos_list)
    matrix = ballot.pref_matrix(qtd_cadidatos, votosList)
    graph = gen_grafo(candidatos_list, matrix)
    excludeList = []

    str_path = floyd_warshall_strongest(qtd_cadidatos, matrix)

    result(qtd_cadidatos, str_path, candidatos_list)
