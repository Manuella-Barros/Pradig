import os
import json

arquivos = os.listdir("./DadosVelhos")

for arquivo in arquivos:
    with open("./DadosVelhos/" + arquivo, "r") as a:
        conteudo = a.read()
        uri = json.loads(conteudo)['uri']
        print(uri)