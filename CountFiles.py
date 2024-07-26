import os

# arq = os.listdir("EventRegistryLib/MinuteStreamEvents/logs") # 1332
# arq = os.listdir("EventRegistryLib/BreakingEvents/logs") # 207
arq = os.listdir("EventRegistryLib/NewMain/logs") #1553

# arq = os.listdir("NewsApiOrg/everything/data") #9512
# arq = os.listdir("NewsApiOrg/TopReadlines/data") #2703

# arq = os.listdir("WorldNewsApi/SearchNews/data") #8037

# arq = os.listdir("logsJunção")

print("quantidade de arquivos ")
print(len(arq))