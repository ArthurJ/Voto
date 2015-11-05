import numpy as np

__author__ = '@arthurj'


def load_candidates(candidates_file_name='candidatos.txt'):
    candidatos = open(candidates_file_name, 'r')
    candidatos_list = []
    for i in candidatos:
        i = i.rstrip('\n')
        candidatos_list.append(i)
    return candidatos_list


def load_ballot_file(ballot_file_name='votos.txt'):
    votos_in = open(ballot_file_name, 'r')
    votos_list = []
    for i in votos_in:
        i = i.rstrip('\n').split(',')
        i = [int(k.strip()) for k in i if not len(k.strip()) == 0]
        votos_list.append(i)
    return votos_list


def pref_matrix(qtd_candidates, vote_list, exclude_list=list()):
    """
        Cria matriz de preferências com os votos e o número de candidatos.
        Caso haja índices na exclude_list,
            as linhas e colunas correspondentes ficam zeradas
        :param qtd_candidates: Quantidade de candidatos
        :param vote_list: Lista de votos,
            cada item é uma lista ordenada de preferencias com os índices
            do candidato
        :param exclude_list: Lista de índices de candidatos a serem ignorados

        >>> a = pref_matrix(12, \
            [[0], [10, 4, 2, 8, 7], [11, 9, 10, 3, 7, 2, 6, 8], \
            [1, 4, 11, 0, 9, 8, 3, 5, 10, 7, 2, 6], [11, 9, 5, 0], \
            [3, 11, 8, 9, 6, 2, 10, 0, 1, 5, 4, 7]], [10]) ; \
        b = np.array([[0, 3, 3, 3, 3, 3, 3, 4, 3, 2, 0, 1], \
                  [1, 0, 1, 1, 2, 2, 1, 2, 1, 1, 0, 1], \
                  [3, 3, 0, 1, 2, 3, 3, 2, 2, 1, 0, 1],\
                  [2, 2, 3, 0, 2, 3, 3, 3, 2, 1, 0, 1],\
                  [2, 1, 2, 2, 0, 2, 2, 3, 2, 2, 0, 2],\
                  [1, 1, 2, 1, 2, 0, 2, 3, 1, 0, 0, 0],\
                  [2, 2, 1, 0, 2, 2, 0, 1, 1, 0, 0, 0],\
                  [2, 2, 2, 1, 1, 2, 3, 0, 1, 1, 0, 1],\
                  [3, 3, 2, 2, 2, 4, 3, 3, 0, 2, 0, 1],\
                  [3, 3, 4, 3, 3, 4, 4, 4, 3, 0, 0, 0],\
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
                  [4, 3, 4, 3, 3, 4, 4, 4, 4, 4, 0, 0]]) ;\
        (a==b).all()
        True
    """
    matriz = np.zeros((qtd_candidates, qtd_candidates), dtype=np.int)
    for i in vote_list:
        excludes = []
        for j in i:
            excludes.append(j)
            for k in range(qtd_candidates):
                if k not in excludes:
                    matriz[j, k] += 1
    for i in exclude_list:
        matriz[i] = np.zeros(qtd_candidates, dtype=np.int)
        matriz[:, i] = np.zeros(qtd_candidates, dtype=np.int)
    return matriz
