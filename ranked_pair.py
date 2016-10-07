import ballot
from operator import itemgetter

__author__ = '@arthurj'


if __name__ == "__main__":
    candidatos_list = ballot.load_candidates()
    votosList = ballot.load_ballot_file()

    qtd_candidatos = len(candidatos_list)
    matrix = ballot.pref_matrix(qtd_candidatos, votosList)

    result = dict()
    for i in range(qtd_candidatos):
        for j in range(i, qtd_candidatos):
            if i == j:
                continue
            votos = matrix[i, j], matrix[j, i]
            ordem = candidatos_list[i], candidatos_list[j]
            if matrix[i, j] < matrix[j, i]:
                votos = matrix[j, i], matrix[i, j]
                ordem = candidatos_list[j], candidatos_list[i]
            result.update({(ordem[0], ordem[1]): (votos[0]/sum(votos))})

    # Testar
    # dicionario esperado = {(vencedor, perdedor): margem}
    # resultado esperado, valores ordenados por margem
    # em caso de empate, o desempate se deve pela ordem de maiores margens que forem menores que a de empate
    # Outra forma possivel de desempate:
    # pegue (na lista subsequente) o que tiver maior precedencia (sem empate) entre os empatados)


    def desempate(candidatos_fixados, casos, maioria, resultado, subordem):
        for c in subordem:  # use essa ordenação para desempatar
            adicionar = [caso for caso in casos
                         if caso[1] >= maioria
                         and c[0][0] is caso[0][0]
                         and caso[0][0] not in candidatos_fixados]
            resultado.append(adicionar[0])
            candidatos_fixados.append(c[0][0])


    def ordenar(dicionario):
        casos = [(x, y) for x, y in dicionario.items()]
        maiorias = sorted(list(set([y for x, y in casos])), reverse=True)

        ocorrencias = [0] * len(maiorias)
        for indice, maioria in enumerate(maiorias):
            ocorrencias[indice] = sum([1 for x, y in casos if y == maioria])
        casos = sorted(casos, key=itemgetter(1), reverse=True)

        resultado = list()
        candidatos_fixados = list()
        for indicei, maioria in enumerate(maiorias):
            if ocorrencias[indicei] == 1:
                selecionados = list()
                selecionados.extend([caso for caso in casos
                                     if (caso[1] == maioria)
                                     and caso[0][0] not in candidatos_fixados])
                candidatos_fixados.extend([caso[0][0] for caso in selecionados])
                resultado.extend(selecionados)

            else:  # busque os vencedores empatados
                candidatos_empatados = set([caso[0][0] for caso in casos
                                            if (caso[1] == maioria)
                                            and caso[0][0] not in candidatos_fixados])

                casos_de_candidatos_empatados = [caso for caso in casos
                                                 if caso[0][0] in candidatos_empatados
                                                 and caso[0][1] in candidatos_empatados
                                                 and len(caso) is not 0]

                # Se houver entre os casos de empate um caso em que ambos vitoriosos estejam com suas margens empatadas
                casos_de_candidatos_empatados.extend([caso for caso in casos
                                                      if (caso[1] is not maioria)
                                                      and caso[0][0] not in candidatos_fixados
                                                      and caso[0][0] in candidatos_empatados
                                                      and caso[0][1] in candidatos_empatados])

                analisar_empatados = dict([caso for caso in casos_de_candidatos_empatados])
                if len(analisar_empatados) > 0:
                    subordem = ordenar(analisar_empatados)  # ordene as combinações entre eles
                    desempate(candidatos_fixados, casos, maioria, resultado, subordem)

        if len(resultado) < len(dicionario):
            subordem = ordenar({x: y for x, y in dicionario.items() if x[0] not in candidatos_fixados})
            desempate(candidatos_fixados, casos, maioria, resultado, subordem)

        return sorted(resultado, key=itemgetter(1), reverse=True)


    print('Lista de vencedores:\n')
    for i in ordenar(result):
        print('{0:.2%} {1} {2:_>45}'.format(i[1], i[0][0], i[0][1]))

    print('\n\nTodos os resultados:\n')
    for i in sorted(result.items(), key=itemgetter(1), reverse=True):
        print('{0:.2%} {1} {2:_>45}'.format(i[1], i[0][0], i[0][1]))
