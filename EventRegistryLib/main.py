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

    print(args.fileLogEvents)
    print(eventsDirectory)



    # key = '28bdc9c2-e717-4ca4-b684-d4744396fe26' #dfaparanhos@cos.ufrj.br ----- bloqueado
    # key = 'a204ebca-0a08-4fb1-82bf-90670cb400c3' #avanderley@cos.ufrj.br ------
    # key = '9c153668-0552-4fa6-bdb6-22027a0459d5' #dlima@cos.ufrj.br -----------
    # key = '44125a48-5ca4-42ee-bd07-80b3430ce68a' #romulo@cos.ufrj.br -----------
    key = '365c1d54-dbed-49ad-88d5-076a6b47c17c'   #manu

    er = EventRegistry(apiKey=key)

    recentQ = GetRecentEvents(er)
    starttime = time.time()

    while True:
        ret = recentQ.getUpdates() # pega os uris dos eventos novos e os que foram atualizados
        try:
            eventos.write("newestUpdate: %s; oldestUpdate: %s; activity: %s\n" % (
            ret["newestUpdate"], ret["oldestUpdate"], selectEnglishEvents(ret["activity"])))
        except KeyError:
            continue

        if "eventInfo" in ret and isinstance(ret["eventInfo"], dict):
            print("==========\n%d events updated since last call" % len(selectEnglishEvents(ret["activity"])))

            # get the list of event URIs, sorted from the most recently changed backwards
            activity = ret["activity"]
            englishEvents = selectEnglishEvents(activity) # pega apenas os uris dos eventos que estão em ingles

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

                    q = QueryEvent(eventUri)
                    q.setRequestedResult(
                        RequestEventArticles(
                            lang="eng", count=1, sortBy="date", returnInfo=ReturnInfo(
                                articleInfo=ArticleInfoFlags(
                                    title=True, body=True, bodyLen=-1, extractedDates=True, concepts=True, storyUri=True, originalArticle=True, categories=True, location=True, image=True, dates=True, details=True
                                )
                            )
                        )
                    )

                    article = er.execQuery(q)
                    articleFile.write(json.dumps(article))
                    articleFile.write("\n")
                else:
                    articleFile = open(articleFileName, 'w+')
                    articleFile.write(json.dumps(event))
                    articleFile.write("\n")

                    art = QueryEventArticlesIter(eventUri, lang="eng")

                    listArticles = art.execQuery(er, returnInfo=ReturnInfo(
                                                        articleInfo=ArticleInfoFlags(
                                                            title=True, body=True, bodyLen=-1, location=True, dates=True, extractedDates=True, concepts=True, storyUri=True, originalArticle=True, categories=True, image=True, details=True
                                                        )
                                                    )
                                                )

                    for article in listArticles:
                        articleFile.write(json.dumps(article))
                        articleFile.write("\n")

                articleFile.close()

        # wait exactly a minute until next batch of new content is ready
        print("sleeping for 60 seconds...")
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))


def selectEnglishEvents(urilist):
    englishArticles = []
    for uri in urilist:
        if 'eng' in uri:
            englishArticles.append(uri)

    return englishArticles


def checkFileExists(fileName):
    return os.path.exists(fileName)


if __name__ == "__main__":
    main()