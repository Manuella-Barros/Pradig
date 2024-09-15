import os
import json

# guarda os arquivos dessa pasta
arquivos = os.listdir("./DadosVelhos")

def tem_duplicados(vetor):
    # Cria um dicionário para contar a frequência dos elementos
    frequencia = {}
    for elemento in vetor:
        if elemento in frequencia:
            print("O elemento duplicado " + elemento)

            return True
        frequencia[elemento] = 1
    return False


for arquivo in arquivos:
    single_id_list = []  # guarda os ids de cada linha para verificar se existe id repetido

    with open("./DadosVelhos/" + arquivo, "r") as a:
        print(arquivo)
        arquivo_artigos_certos = open("./DadosNovos/ArtigosCertos/" + arquivo, "w")

        for index, linha in enumerate(a):
            # guarda o id no vetor de ids
            if 'id' in linha:
                # o line esta em formato de texto, aqui transforma em objeto
                line_json = json.loads(linha)
                # pega o uri de cada linha
                single_id_list.append(line_json['id'])

                # primeira linha com as infos do evento
            if index == 0:
                arquivo_artigos_certos.write(linha)

            # se o id dessa linha ja existe no vetor, não guarda essa linha e se retira o id duplicado no vetor de ids
            elif tem_duplicados(single_id_list):
                single_id_list.pop()

            elif "storyUri" in linha and "eventUri" in linha:
                story_uri = json.loads(linha)["storyUri"]
                event_uri = json.loads(linha)["eventUri"]

                if story_uri == event_uri:  # se o story_uri estiver certo
                    arquivo_artigos_certos.write(linha)

                # se o story_uri estiver errado
                else:
                    arquivo_artigos_errados = open("./DadosNovos/ArtigosErrados/" + event_uri + "_" + story_uri + ".txt", "a")
                    arquivo_artigos_errados.write(linha)

            else:  # se não tiver story_uri ou event_uri, guarda com a data
                date = json.loads(linha)["date"]
                ano = date.split("-")[0]
                mes = date.split("-")[1]
                arquivos_sobra = open("./DadosNovos/ArtigosQueSobraram/news-" + ano + mes + ".txt", "a")
                arquivos_sobra.write(linha)