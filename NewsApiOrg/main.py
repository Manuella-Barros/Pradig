import json
import time
import requests

response = requests.get("https://newsapi.org/v2/everything?q=a&language=en&apikey=e2ad616f2f85423da7f0b4c09dbf5af0")
articles = response.json()['articles']

for article in articles:
    currentTimeStamp = str(time.time())

    with open("./dataTxt_NewsApiOrg/" + currentTimeStamp, 'w') as f:
        json.dump(article, f)
        print(article)