# UTILIZANDO O ENDPOINT https://eventregistry.org/api/v1/event/getBreakingEvents
# Pega os artigos dos eventos que:
#   - aconteceram recentemente
#   - teve muitos artigos coletados e pouco tempo
#   - que está sendo muito comentado recentemente

from eventregistry import *
import time
import json
import os.path
import argparse


# comando para rodar ->  python main.py -f ./eventos/eventos.txt -e ./logs/

def main():
    argument_parser = argparse.ArgumentParser(description="Parser from Event Registry")
    argument_parser.add_argument("-f", "--fileLogEvents", type=str, required=True,
                                 help="File containing the log of the events crawled")
    argument_parser.add_argument("-e", "--eventsDirectory", type=str, required=True, help="Root directory ")
    args = argument_parser.parse_args()

    eventos = open(args.fileLogEvents, 'a')
    eventsDirectory = args.eventsDirectory

    key = 'a259d829-3579-46ef-9c90-6aab7b4d59a7' # manu

    er = EventRegistry(apiKey=key)

    starttime = time.time()

    q1 = QueryEvents(lang="eng")
    q1.setRequestedResult( # Aqui você descreve o que precisa estar no retorno da api, passa instancia de alguma classe para isso
        RequestEventsBreakingEvents( # A classe que recebe os parametros do endpoint breaking events
            returnInfo=ReturnInfo(
                articleInfo=ArticleInfoFlags(
                    location=True, dates=True, extractedDates=True,
                    concepts=True, storyUri=True, originalArticle=True, categories=True,
                    details=True
                )
            )
        )
    )

    res = er.execQuery(q1)
    breakingEvents = res['breakingEvents']['results']

    for event in breakingEvents:
        eventUri = event['uri']

        if not isEnglishEvent(eventUri):
            continue

        articleFileName = eventsDirectory + eventUri + '.txt'

        print("Event %s\n" % eventUri)

        if checkFileExists(articleFileName):
            articleFile = open(articleFileName, 'a')
            fileRead = open(articleFileName, 'r')

            q2 = QueryEvent(eventUri)
            q2.setRequestedResult(
                RequestEventArticles(
                    lang="eng", count=1, sortBy="date", returnInfo=ReturnInfo(
                        articleInfo=ArticleInfoFlags(
                            location=True, dates=True, extractedDates=True,
                            concepts=True, storyUri=True, originalArticle=True, categories=True,
                            details=True
                        )
                    )
                )
            )

            res = er.execQuery(q2)
            articles = res[eventUri]['articles']['results']

            for article in articles:
                for line in fileRead:  # le linha por linha
                    if 'uri' in line:  # evita as linhas vazias
                        lineJson = json.loads(line)
                        if lineJson['uri'] == article['uri']:
                            print("duplicado")
                            return

                articleFile.write(json.dumps(article))
                articleFile.write("\n")
        else:
            articleFile = open(articleFileName, 'w+')
            articleFile.write(json.dumps(event))
            articleFile.write("\n")

            art = QueryEventArticlesIter(eventUri, lang="eng")

            listArticles = art.execQuery(er, returnInfo=ReturnInfo(
                articleInfo=ArticleInfoFlags(
                    location=True, dates=True, extractedDates=True,
                    concepts=True, storyUri=True, originalArticle=True, categories=True,
                    details=True
                )
            ))

            for article in listArticles:
                articleFile.write(json.dumps(article))
                articleFile.write("\n")

        articleFile.close()

def selectEnglishEvents(urilist):
    englishArticles = []
    for uri in urilist:
        if 'eng' in uri:
            englishArticles.append(uri)

    return englishArticles

def isEnglishEvent(uri):
    if 'eng' in uri:
        return True

    return False

def checkFileExists(fileName):
    return os.path.exists(fileName)


if __name__ == "__main__":
    main()