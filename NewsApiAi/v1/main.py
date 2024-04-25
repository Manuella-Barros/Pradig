import json
import time
import requests
import os

response = requests.get(
    'http://eventregistry.org/api/v1/event/getEvents',
    headers={"Content-Type": "application/json"},
    json={
      "resultType": "events",
      "eventsPage": 3,
      "eventsCount": 50,
      "apiKey": "9da7934f-bbef-407d-9a1c-87638ab8a447",
      "lang": "eng"
    }
)


events = response.json()["events"]["results"]

for event in events:
    currentTimeStamp = str(time.time())

    with open("./dataTxt_NewsApiAi/" + currentTimeStamp, 'w') as f:
        json.dump(event, f)
        print(event)

# Esse trecho de código abaixo é só para saber quantos arquivo tem
arr = os.listdir("dataTxt_NewsApiAi")

print("quantidade de arquivos ")
print(len(arr))