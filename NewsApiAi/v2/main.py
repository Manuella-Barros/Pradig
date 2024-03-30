import json
import os

filesName = os.listdir("rawData") # pega o nome de todos os arquivos na pasta rawData

for file in filesName:
    with open("./rawData/" + file, "r", encoding="utf8") as f: # abre os arquidos de acordo com o caminho passado
        filePythonObject = json.loads(f.read()) # f é o arquivo, f.read() lê o arquivo, json.loads() pega um json em formato de string e transforma em um objeto python
        uri = filePythonObject["uri"]

        with open("./newData/" + uri, "w", encoding="utf8") as w:  # cria um arquivo com o nome igual ao id (uri) do evento
            json.dump(filePythonObject, w) # escreve o filePythonObject no arquivo w que acabou de ser criado


# json.dumps(aquivo.json) -> converte um objeto python pra uma string de json
# json.dump(aquivo.json) -> para escrever um objeto python em um arquivo
# json.loads(arquivo.json) -> converte uma string de json para um objeto python
# json.load(arquivo.json) -> converte um objeto json para um objeto python