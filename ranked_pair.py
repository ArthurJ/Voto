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

    # TODO:
    '''
        Definir a lista de preferência sem as repetições, e em caso de empate entre maiorias do candidato A e B,
        usar a referência de A versus B para decidir quem tem a preferência.
        
        from operator import itemgetter
#Testar
# dicionario esperado = {(vencedor, perdedor): margem}
# resultado esperado, valores ordenados por margem
# em caso de empate, o desempate se deve pela ordem de maiores margens que forem menores que a de empate

def ordenar(dicionario):
    casos = [(x, y) for x, y in dicionario.items()]
    maiorias = sorted(list(set([y for x, y in casos])), key=itemgetter(1), reverse=True)
    ocorrencias = [0]*len(maiorias)
    for i, maioria in enumerate(maiorias):    
        ocorrencias[i] = sum([1 for x, y in casos if y == maioria])
    casos = sorted(casos, key=itemgetter(1), reverse=True)
    
    resultado = []

    candidatos_fixados = []
    for i, maioria in enumerate(maiorias):
        if  ocorrencias[i] == 1:
            resultado.append([caso for caso in casos 
                                if (caso[1] == maioria][0]) and caso[0][0] not in candidatos_fixados])
            candidatos_fixados.append(caso[0][0])
            
        else:  # busque os vencedores empatados
            candidatos_empatados = [caso[0][0] for caso in casos 
                                        if (caso[1] == maioria) and caso[0][0] not in candidatos_fixados]
            candidatos_empatados = list(set(candidatos_empatados))

            casos_de_candidatos_empatados = [caso for caso in casos
                                                if (caso[1] < maioria)
                                                    and caso[0][0] in candidatos_empatados 
                                                    and caso[0][1] in candidatos_empatados]
            
            # Se houver entre os casos de empate um caso em que ambos vitoriosos estejam com suas margens empatadas
            casos_de_candidatos_empatados.append([caso for caso in casos 
                                                    if (caso[1] == maioria][0]) 
                                                    and caso[0][0] not in candidatos_fixados
                                                    and caso[0][0] in candidatos_empatados 
                                                    and caso[0][1] in candidatos_empatados])
                                                    
            subordem = ordenar(dict(casos_de_candidatos_empatados))  # ordene as combinações entre eles

            for c in subordem:  # use essa ordenação para desempatar
                resultado.append([caso for caso in casos 
                                    if (caso[1] == maioria][0]) 
                                    and c[0][0] == caso[0][0]
                                    and caso[0][0] not in candidatos_fixados])
                candidatos_fixados.append(c[0][0])

    return resultado


        # ------------------------------------------------------------------------------------------
        # Outra forma possivel de desempate:
        # pegue (na lista subsequente) o que tiver maior precedencia (sem empate) entre os empatados)
    '''

    for i in result:
        print('{:.2%} {}'.format(i[0], i[1]), '{}'.format(i[2]).rjust(45, '_'))

    # locks = []
    # visited_node = []
    # for i in result:
    #     if i[1] not in visited_node:
    #         visited_node
    #     locks.append()
