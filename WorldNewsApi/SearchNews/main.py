import json
import time
import requests

# UTILIZANDO O ENDPOINT https://api.worldnewsapi.com/search-news?language=en
# - Pesquise e filtre notícias por texto, data, local, idioma e muito mais. A API retorna uma lista de artigos de notícias
# que correspondem aos critérios fornecidos.

starttime = time.time()
apiKey = "0d5dad2ce811476c89e12fd2290fe0e9"
number = 100 #quantidade de artigos
offset = 0 #paginas a pular

response = requests.get("https://api.worldnewsapi.com/search-news?api-key=" + apiKey + "&language=en&number=0" + str(number) + "&offset=" + str(offset))
articles = response.json()['news']

for article in articles:
    currentTimeStamp = str(time.time())

    with open("./data/" + currentTimeStamp, 'w') as f:
        json.dump(article, f)
        print(article)

while True:
    response = requests.get("https://api.worldnewsapi.com/search-news?api-key=" + apiKey + "&language=en&number=" + str(number) + "&offset=" + str(offset))
    articles = response.json()['news']

    for article in articles:
        currentTimeStamp = str(time.time())

        with open("./data/" + currentTimeStamp, 'w') as f:
            json.dump(article, f)
            print(article)

    offset += 100
    print("pausa...")
    time.sleep(30.0 - ((time.time() - starttime) % 30.0))