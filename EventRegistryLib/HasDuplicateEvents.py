# CODIGO PARA VERIFICAR SE TEM ALGUM URI REPETIDO NOS DADOS COLETADOS
import json
import os

filesNames = os.listdir("BreakingEvents/logs") # pega o nome dos arquivos
urisVector = []

for fileName in filesNames:
    with open('BreakingEvents/logs/' + fileName, 'r') as file: # aqui abre cada arquivo
        print(fileName)
        for line in file: # le linha por linha
            if 'uri' in line: # evita as linhas vazias
                lineJson = json.loads(line) # o line esta em formato de texto, aqui transforma em objeto
                urisVector.append(lineJson['uri']) # pega o uri de cada linha



def tem_duplicados(vetor):
    # Cria um dicionário para contar a frequência dos elementos
    frequencia = {}
    for elemento in vetor:
        if elemento in frequencia:
            print("O elemento duplicado " + elemento + " se encontra no arquivo " + get_file_name(elemento))

            return True
        frequencia[elemento] = 1
    return False

def get_file_name(uri):
    for file_name in filesNames:
        with open('BreakingEvents/logs/' + file_name, 'r') as file:  # aqui abre cada arquivo
            for line in file:  # le linha por linha
                if 'uri' in line:  # evita as linhas vazias
                    lineJson = json.loads(line)  # o line esta em formato de texto, aqui transforma em objeto
                    if lineJson['uri'] == uri:
                        return file_name

    return "Não foi encontrado"

print(tem_duplicados(urisVector))