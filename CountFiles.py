import os

# arq = os.listdir("EventRegistryLib/MinuteStreamEvents/logs") # 1332
# arq = os.listdir("EventRegistryLib/BreakingEvents/logs") # 207
# arq = os.listdir("EventRegistryLib/NewMain/logs") #776

# arq = os.listdir("NewsApiOrg/everything/data") #1315
# arq = os.listdir("NewsApiOrg/TopReadlines/data") #957

arq = os.listdir("WorldNewsApi/SearchNews/data") #3163

# arq = os.listdir("logsJunção")

print("quantidade de arquivos ")
print(len(arq))