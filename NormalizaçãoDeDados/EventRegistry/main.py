import os
import json

arquivos = os.listdir("./DadosVelhos")

for arquivo in arquivos:
    with open("./DadosVelhos/" + arquivo, "r") as a:
        print(arquivo)
        f = open("./DadosNovos/" + arquivo, "w")

        for linha in a:
            if "storyUri" not in linha:
                print('Não tem story uri') # A primeira linha não tem o story uri pq tem o detalhe do evento
                f.write(linha)
            else:
                storyUri = json.loads(linha)["storyUri"]

                if storyUri + ".txt" == arquivo: #storyUri certo
                    f.write(linha)
                else:
                    print("ta errado")




# import os
# import json
#
# arquivos = os.listdir("./DadosVelhos")
#
# class ArquivosNomes:
#     def __init__(self, nome, uri):
#         self.nome = nome
#         self.uri = uri
#     def __str__(self):
#         return f"nome: {self.nome}, uri: {self.uri}"
#
# nomesVetor = []
#
# for arquivo in arquivos:
#     with open("./DadosVelhos/" + arquivo, "r") as a:
#         conteudo = a.read()
#         uri = json.loads(conteudo)['uri']
#         ar = ArquivosNomes(arquivo, uri)
#         nomesVetor.append(ar)
#
# for nome in nomesVetor:
#     try:
#         os.rename("./DadosVelhos/" + nome.nome, "./DadosVelhos/" + nome.uri + ".txt")
#     except FileExistsError:
#         print("O evento " + nome.uri + "já existe")