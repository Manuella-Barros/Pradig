import os
import json

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Category:
    id: int
    label: str
    uri: str
    wgt: int


@dataclass
class Source:
    id: str
    title: str
    uri: str


@dataclass
class ConceptLabel:
    eng: str


@dataclass
class Concept:
    id: str
    type: str
    label: ConceptLabel
    uri: str
    score: int


@dataclass
class Article:
    id: str
    categories: List[Category]
    date: str
    uri: str
    source: Source
    url: str
    body: str
    dateTime: str
    extractedDates: Optional[str]
    sim: float
    dateCrawl: str
    details: dict
    storyUri: str
    time: str
    lang: str
    eventUri: str
    location: Optional[str]
    concepts: List[Concept]
    image: str
    timeCrawl: str
    isDuplicate: bool
    title: str
    originalArticle: Optional[str]

old_data_dir = os.listdir("dados-velhos")

def format_date(date: str):
    ano = date.split("-")[0]
    mes = date.split("-")[1]
    return f"{ano}{mes}"


for old_data in old_data_dir:
    correct_data_file = open(f"./dados-novos/arquivos-corretos/{old_data}", "a")
    actual_file_name = old_data.split(".")[0]
    id_hashmap = {}

    with open(f"./dados-velhos/{old_data}", "r") as file:
        for index, line in enumerate(file):
            if line.strip() == "":
                continue

            event_info: Article = json.loads(line) if isinstance(line, str) else line

            if actual_file_name in event_info and "articles" in event_info[actual_file_name] and "results" in event_info[actual_file_name]["articles"]: # artigo mal formatado
                event_info = event_info[actual_file_name]["articles"]["results"][0]

            if "lang" in event_info and event_info["lang"] != "eng":
                continue

            if "id" in event_info:
                if event_info["id"] in id_hashmap:
                    continue

                id_hashmap.update({
                    event_info["id"]: event_info["id"]
                })

            if index == 0: # primeira linha, com os dados do evento
                correct_data_file.write(line)
                date_formatted = '201708'# format_date(event_info["eventDate"])
                uri = event_info['uri']
                continue

            if not "storyUri" in event_info or not "eventUri" in event_info: # se não tiver storyUri ou eventUri
                file_name = f"./dados-novos/resto/news-{date_formatted}.txt"
                other_data_file = open(file_name, "a")

                for key in event_info:
                    print("opa")
                    print(event_info)
                    if "newEventUri" in event_info[key] and 'eng' not in event_info[key]['newEventUri']:
                        print(event_info[key])
                        print('n ta em ingles')
                        continue

                    other_data_file.write(line)
                continue

            if event_info["storyUri"] != event_info["eventUri"]: # se for diferente
                file_name = "./dados-novos/arquivos-errados/" + event_info["eventUri"] + "_" + event_info["storyUri"] + ".txt"
                wrong_data_file = open(file_name, "a")
                wrong_data_file.write(line)
                continue

            correct_data_file.write(line) # se for igual