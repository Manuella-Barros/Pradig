import os
import json

from dataclasses import dataclass
from typing import List, Optional

old_data_dir = os.listdir("dados-velhos")
files_names_hashmap = {}

def format_date(date: str):
    ano = date.split("-")[0]
    mes = date.split("-")[1]
    return f"{ano}{mes}"

def event_alread_exists(eventUri):
    return eventUri + ".txt" in old_data_dir

for old_data in old_data_dir:
    correct_data_file = open(f"./dados-novos/arquivos-corretos/{old_data}", "a")
    actual_file_name = old_data.split(".")[0]

    if old_data in files_names_hashmap:
        print("O arquivo " + old_data + " ja existe")
        continue

    files_names_hashmap.update({
        old_data: old_data
    })

print(files_names_hashmap)