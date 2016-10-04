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

    ballot.print_matriz(maior_valor, strong_path_matrix, 'Matriz de Preferência:\n')

    print('Lista de Preferências:\n')
    preferencia = []
    for j, i in enumerate(candidate_list):
        porcentagem = qtd_vitorias[i] / (qtd_candidates - 1)
        preferencia.append((porcentagem, j, i))
    preferencia = sorted(preferencia, key=lambda preferencia: preferencia[0], reverse=True)
    [print(p[1:]) for p in preferencia]
    print('\n')


def floyd_warshall_strongest(num_candidatos, matriz_preferencias):
    strong_pth = np.zeros((num_candidatos, num_candidatos), dtype=np.int)
    for i in range(num_candidatos):
        for j in range(num_candidatos):
            if i != j:
                if matriz_preferencias[i, j] > matriz_preferencias[j, i]:
                    strong_pth[i, j] = matriz_preferencias[i, j]

    for i in range(num_candidatos):
        for j in range(num_candidatos):
            if i == j:
                continue
            for k in range(num_candidatos):
                if i != k and j != k:
                    strong_pth[j, k] = max(strong_pth[j, k],
                                           min(strong_pth[j, i],
                                               strong_pth[i, k]))

    return strong_pth


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
