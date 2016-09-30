import ballot

__author__ = '@arthurj'


if __name__ == "__main__":
    candidatos_list = ballot.load_candidates()
    votosList = ballot.load_ballot_file()

    qtd_candidatos = len(candidatos_list)
    matrix = ballot.pref_matrix(qtd_candidatos, votosList)

    result = []
    for i in range(qtd_candidatos):
        for j in range(i, qtd_candidatos):
            if i == j:
                continue
            votos = matrix[i, j], matrix[j, i]
            ordem = candidatos_list[i], candidatos_list[j]
            if matrix[i, j] < matrix[j, i]:
                votos = matrix[j, i], matrix[i, j]
                ordem = candidatos_list[j], candidatos_list[i]
            result.append([votos[0]/sum(votos), ordem[0], ordem[1]])

    result = sorted(result, reverse=True)
    for i in result:
        print('{:.3%} {}'.format(i[0], i[1]),
              ''.center(45, '_'), '{}'.format(i[2]))

    # locks = []
    # visited_node = []
    # for i in result:
    #     if i[1] not in visited_node:
    #         visited_node
    #     locks.append()
