import os

# arq = os.listdir("EventRegistryLib/MinuteStreamEvents/logs") # 1332
# arq = os.listdir("EventRegistryLib/BreakingEvents/logs") # 207
# arq = os.listdir("EventRegistryLib/NewMain/logs") #868

# arq = os.listdir("NewsApiOrg/everything/data") #1704
# arq = os.listdir("NewsApiOrg/TopReadlines/data") #1028

arq = os.listdir("WorldNewsApi/SearchNews/data") #3533

# arq = os.listdir("logsJunção")

print("quantidade de arquivos ")
print(len(arq))