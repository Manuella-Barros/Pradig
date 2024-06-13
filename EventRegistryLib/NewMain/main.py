# UTILIZANDO O ENDPOINT https://eventregistry.org/api/v1/minuteStreamEvents
# Pega os artigos que foram adicionados ou atualizados recentemente

from eventregistry import *
import time
import json
import os.path
import argparse

# comando para rodar ->  python main.py -f ./eventos/eventos.txt -e ./logs/
# TODO: levar o código desse crawler para newsanalysis/crawlers/crawler_ldconline.py, REFATORADO e LIMPO

'''
command line example to run 

PYTHONPATH=$PYTHONPATH:/home/paranhos/PycharmProjects/event-registry-python 
python3 EventRegistryCrawler.py 
-f /home/paranhos/PycharmProjects/social-media-data/parser/eventos.txt 
-e /home/paranhos/PycharmProjects/social-media-data/parser/eventos/

'''

def main():
    argument_parser = argparse.ArgumentParser(description="Parser from Event Registry")
    argument_parser.add_argument("-f", "--fileLogEvents", type=str, required=True,
                                 help="File containing the log of the events crawled")
    argument_parser.add_argument("-e", "--eventsDirectory", type=str, required=True, help="Root directory ")
    args = argument_parser.parse_args()

    # eventos = open('/home/paranhos/PycharmProjects/social-media-data/parser/eventos.txt', 'a') #file with the news titles #substituir por argumento da linha de comando
    eventos = open(args.fileLogEvents, 'a')
    # eventsDirectory = '/home/paranhos/PycharmProjects/social-media-data/parser/events/'
    eventsDirectory = args.eventsDirectory

    key = 'a259d829-3579-46ef-9c90-6aab7b4d59a7'

    er = EventRegistry(apiKey=key)

    recentQ = GetRecentEvents(er) # /api/v1/minuteStreamEvents
    starttime = time.time()

    while True:
        print("========================================================================================================")
        print("MINUTES STREAM EVENTS")
        print("========================================================================================================")
        minuteStreamEvents(eventos, eventsDirectory, er, recentQ)

        # wait exactly a minute until next batch of new content is ready
        print("sleeping for 60 seconds...")
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))

        print("========================================================================================================")
        print("BREAKING EVENTS")
        print("========================================================================================================")
        breakingEvents(eventos, eventsDirectory, er)

        # wait exactly a minute until next batch of new content is ready
        print("sleeping for 60 seconds...")
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))


def minuteStreamEvents(eventos, eventsDirectory, er, recentQ):
    ret = recentQ.getUpdates()  # pega os uris dos eventos novos e os que foram atualizados

    try:
        eventos.write("newestUpdate: %s; oldestUpdate: %s; activity: %s\n" % (
            ret["newestUpdate"], ret["oldestUpdate"], selectEnglishEvents(ret["activity"])))
    except KeyError:
        return

    if "eventInfo" in ret and isinstance(ret["eventInfo"], dict):
        print("==========\n%d events updated since last call" % len(selectEnglishEvents(ret["activity"])))

        # get the list of event URIs, sorted from the most recently changed backwards
        activity = ret["activity"]
        englishEvents = selectEnglishEvents(activity)  # pega apenas os uris dos eventos que estão em ingles

        # print(json.dumps(ret))
        # for each updated event print the URI and the title
        # NOTE: the same event can appear multiple times in the activity array - this means that more than one article
        # about it was recently written about it
        for eventUri in englishEvents:
            event = ret["eventInfo"][eventUri]

            print("Event %s\n" % eventUri)

            articleFileName = eventsDirectory + eventUri + '.txt'

            if checkFileExists(articleFileName):
                articleFile = open(articleFileName, 'a')
                fileRead = open(articleFileName, 'r')

                q = QueryEvent(eventUri)
                q.setRequestedResult(
                    RequestEventArticles(
                        lang="eng", count=1, sortBy="date", returnInfo=ReturnInfo(
                            articleInfo=ArticleInfoFlags(
                                title=True, body=True, bodyLen=-1, extractedDates=True, concepts=True,
                                storyUri=True, originalArticle=True, categories=True, location=True, image=True,
                                dates=True, details=True
                            )
                        )
                    )
                )

                res = er.execQuery(q)
                articles = res[eventUri]['articles']['results']

                articleAlreadyExists = False

                for article in articles:
                    for line in fileRead:  # le linha por linha
                        if 'uri' in line:  # evita as linhas vazias
                            lineJson = json.loads(line)

                            if lineJson['uri'] == article['uri']: # se ja tiver esse uri em alguma linha, então não salva
                                articleAlreadyExists = True
                                print("duplicado")

                    if not articleAlreadyExists:
                        articleFile.write(json.dumps(article))
                        articleFile.write("\n")

                    articleAlreadyExists = False

            else:
                articleFile = open(articleFileName, 'w+')
                articleFile.write(json.dumps(event))
                articleFile.write("\n")

                art = QueryEventArticlesIter(eventUri, lang="eng")

                listArticles = art.execQuery(er, returnInfo=ReturnInfo(
                    articleInfo=ArticleInfoFlags(
                        title=True, body=True, bodyLen=-1, location=True, dates=True, extractedDates=True,
                        concepts=True, storyUri=True, originalArticle=True, categories=True, image=True,
                        details=True
                    )
                ))

                for article in listArticles:
                    articleFile.write(json.dumps(article))
                    articleFile.write("\n")

            articleFile.close()

def breakingEvents(eventos, eventsDirectory, er):
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

        if not checkFileExists(articleFileName):
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

        # if checkFileExists(articleFileName):
        #     articleFile = open(articleFileName, 'a')
        #     fileRead = open(articleFileName, 'r')
        #
        #     q2 = QueryEvent(eventUri)
        #     q2.setRequestedResult(
        #         RequestEventArticles(
        #             lang="eng", count=1, sortBy="date", returnInfo=ReturnInfo(
        #                 articleInfo=ArticleInfoFlags(
        #                     location=True, dates=True, extractedDates=True,
        #                     concepts=True, storyUri=True, originalArticle=True, categories=True,
        #                     details=True
        #                 )
        #             )
        #         )
        #     )
        #
        #     res = er.execQuery(q2)
        #     articles = res[eventUri]['articles']['results']
        #
        #     articleAlreadyExists = False
        #
        #     for article in articles:
        #         for line in fileRead:  # le linha por linha
        #             if 'uri' in line:  # evita as linhas vazias
        #                 lineJson = json.loads(line)
        #
        #                 if lineJson['uri'] == article['uri']: # se ja tiver esse uri em alguma linha, então não salva
        #                     articleAlreadyExists = True
        #                     print("duplicado")
        #
        #         if not articleAlreadyExists:
        #             articleFile.write(json.dumps(article))
        #             articleFile.write("\n")
        #
        #         articleAlreadyExists = False
        #
        # else:
        #     articleFile = open(articleFileName, 'w+')
        #     articleFile.write(json.dumps(event))
        #     articleFile.write("\n")
        #
        #     art = QueryEventArticlesIter(eventUri, lang="eng")
        #
        #     listArticles = art.execQuery(er, returnInfo=ReturnInfo(
        #         articleInfo=ArticleInfoFlags(
        #             location=True, dates=True, extractedDates=True,
        #             concepts=True, storyUri=True, originalArticle=True, categories=True,
        #             details=True
        #         )
        #     ))
        #
        #     for article in listArticles:
        #         articleFile.write(json.dumps(article))
        #         articleFile.write("\n")

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