import json
import time
import requests
# UTILIZANDO O ENDPOINT https://newsapi.org/v2/top-headlines?language=en
#   - Fornece manchetes principais e de última hora ao vivo para um país, categoria específica em um país, fonte única ou fontes múltiplas.

starttime = time.time()

while True:

    response = requests.get("https://newsapi.org/v2/top-headlines?language=en&apikey=e2ad616f2f85423da7f0b4c09dbf5af0")
    articles = response.json()['articles']

    for article in articles:
        currentTimeStamp = str(time.time())

        with open("./data/" + currentTimeStamp, 'w') as f:
            json.dump(article, f)
            print(article)

    print("pausa...")
    time.sleep(30.0 - ((time.time() - starttime) % 30.0))