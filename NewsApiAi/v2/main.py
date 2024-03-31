import json
import os
import requests

filesName = os.listdir("rawData") # pega o nome de todos os arquivos na pasta rawData

for file in filesName:
    with open("./rawData/" + file, "r", encoding="utf8") as f: # pega os arquivos velhos e o uri para renomear
        filePythonObject = json.loads(f.read()) # f é o arquivo, f.read() lê o arquivo, json.loads() pega um json em formato de string e transforma em um objeto python
        uri = filePythonObject["uri"]

        response = requests.get( #pega a requisição da api de acordo com o uri
            'http://eventregistry.org/api/v1/event/getEvent',
            headers={"Content-Type": "application/json"},
            json={
                "apiKey": "365c1d54-dbed-49ad-88d5-076a6b47c17c",
                "eventUri": uri,
                "resultType": "articles",
                "articlesPage": 1,
                "articlesCount": 50,
                "articlesLang": ["eng"],
                "includeArticleCategories": True,
                "includeArticleConcepts": True
            }
        )

        try:
            articles = response.json()[uri]["articles"]["results"]

            with open("./newData/" + uri, "w", encoding="utf8") as w:  # cria um arquivo com o nome igual ao id (uri) do evento
                json.dump(filePythonObject, w)  # escreve o filePythonObject no arquivo w que acabou de ser criado

                for article in articles:  # adiciona os artigos um por um no arquivo para pular dar uma espaço entre eles
                    w.write("\n")
                    json.dump(article, w)

        except Exception as error:
            with open("./dataWithErrors/" + uri, "w", encoding="utf8") as w:  # cria um arquivo com o nome igual ao id (uri) do evento
                json.dump(filePythonObject, w)  # escreve o filePythonObject no arquivo w que acabou de ser criado

# json.dumps(aquivo.json) -> converte um objeto python pra uma string de json
# json.dump(aquivo.json) -> para escrever um objeto python em um arquivo
# json.loads(arquivo.json) -> converte uma string de json para um objeto python
# json.load(arquivo.json) -> converte um objeto json para um objeto python