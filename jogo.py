import io
import pandas as pd
import re
from collections import defaultdict
import operator
import requests
from zipfile import ZipFile
import os
from numpy import random

try:
    os.remove("d_lotman.htm")
except OSError:
    pass

r = requests.get('http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotoma.zip')
r.encoding = 'utf-8'
ZipFile(io.BytesIO(r.content)).extractall()

headers = ["Bola1", "Bola2", "Bola3", "Bola4", "Bola5", "Bola6", "Bola7", "Bola8", "Bola9", "Bola10", "Bola11", "Bola12", "Bola13", "Bola14", "Bola15", "Bola16", "Bola17", "Bola18", "Bola19", "Bola20"]
filename = "d_lotman.htm"
html = open(filename, "r", encoding = "ISO-8859-1").read()
#print(html)
df = pd.read_html(html)
table = df[0]

#cont = [0] * 100
cont = defaultdict(int)

for lin in range(0, len(table)) :
    for h in headers:
        #print("Linha {} Col {} Val {}".format(lin, h, table[h][lin]))
        for num in range(0, 99):
            if (table[h][lin] == num):
                #print("Saiu {}".format(num))
                cont[num] += 1

#for num in range(0, 99):
#    print("[{}] = {}".format(num, cont[num]))             

s_cont = sorted(cont.items(), key=operator.itemgetter(1))
s_cont_inv = sorted(cont.items(), key=operator.itemgetter(1), reverse=True)
print("="*10, "Menos Vezes Sorteado (Valor, Jogos q saiu)", "="*10)
print(s_cont[0:50])
print("="*5, "Mais vezes sorteados", "="*5)
print(s_cont_inv[0:50])

cont = defaultdict(int)
for lin in range(0, len(table)) :
    for num in range(0, 99):
        cont[num] += 1
    for h in headers:
        #print("Linha {} Col {} Val {}".format(lin, h, table[h][lin]))
        for num in range(0, 99):
            if (table[h][lin] == num):
                #print("Saiu {}".format(num))
                cont[num] = 0

rally_cont = sorted(cont.items(), key=operator.itemgetter(1), reverse=True)
rally_cont_inv = sorted(cont.items(), key=operator.itemgetter(1), reverse=False)
print("="*10, "Maior Rally (Valor, Jogos sem sair)", "="*10)
print(rally_cont)
print("="*5, "Maiores 50", "="*5)
print(rally_cont[0:50])
print("="*5,"Menores 50", "="*5)
print(rally_cont_inv[0:50])

print("="*10, "ultimo sorteio", "="*10)
ultimo = len(table) - 1

ultimo_jogo = []
for h in headers:
    ultimo_jogo.append(table[h][ultimo])


cont = defaultdict(int)
for lin in range(0, len(table) - 1) :
    for num in range(0, 99):
        cont[num] += 1
    for h in headers:
        #print("Linha {} Col {} Val {}".format(lin, h, table[h][lin]))
        for num in range(0, 99):
            if (table[h][lin] == num):
                #print("Saiu {}".format(num))
                cont[num] = 0
print(ultimo_jogo)    

rally_sorteado = []
for x in ultimo_jogo:
    rally_sorteado.append((x, cont[x]))

print("="*10, "Rally dos sorteados", "="*10)
print(rally_sorteado)    

lista_busca_tot = {
    1: {0:7, 1:18, 2:7, 3:1, 4:2, 5:1, 6:2, 7:7, 8:2, 9:1, 10:2},
    2: {0:10, 1:8, 2:8, 3:5, 4:0, 5:5, 6:0, 7:3, 8:3, 9:0, 10:10}
    }
lista_busca = lista_busca_tot[1]

inv_cont = defaultdict(list)
for num in range(0, 99):
    inv_cont[cont[num]].append(num)

jogo = []
print(inv_cont)
for i in range(0, 11):
    #print("i {} Vou sortear {}".format(i, lista_busca[i]))
    #print("Possiveis {}".format(inv_cont[i]))
    fim = 0
    if lista_busca[i] >  len(inv_cont[i]):
        for j in range(0, len(inv_cont[i])):
            jogo.append(inv_cont[i][j])
    else :
        fim = lista_busca[i]
        #print("Fim {}".format(fim))    
        #tam_jogo = tam_jogo - fim
        for j in range(0, fim):
            sorteio = random.randint(0, fim)
            if inv_cont[i][sorteio] not in jogo:
                jogo.append(inv_cont[i][sorteio])
            else:
                j = j - 1    

print(jogo)
faltou = 50 - len(jogo)
print("Faltou {}".format(faltou))

for j in s_cont_inv:
    if j[0] not in jogo:
        jogo.append(j[0])
    if len(jogo) >= 50 :
        break    

print("="*10, "Jogo Histograma", "="*10)
print(sorted(jogo))
print("="*10, "Jogo Rally", "="*10)
print(sorted([i[0] for i in rally_cont_inv[0:50]]))
print("="*10, "Jogo Mais vezes sorteados", "="*10)
print(sorted([i[0] for i in s_cont_inv[0:50]]))
