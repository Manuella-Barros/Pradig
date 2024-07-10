import os

# arq = os.listdir("EventRegistryLib/MinuteStreamEvents/logs") # 1332
# arq = os.listdir("EventRegistryLib/BreakingEvents/logs") # 207
arq = os.listdir("EventRegistryLib/NewMain/logs") #1061

# arq = os.listdir("NewsApiOrg/everything/data") #3528
# arq = os.listdir("NewsApiOrg/TopReadlines/data") #1455

# arq = os.listdir("WorldNewsApi/SearchNews/data") #5386

# arq = os.listdir("logsJunção")

print("quantidade de arquivos ")
print(len(arq))