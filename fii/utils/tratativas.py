#!python3
import re

def tratar_dados_fii(dados):
    
    lista = []
    
    for d in dados:
        l = d
        l['valor'] = tratar_numeros(d['valor'])
        lista.append(l)

    return lista


def tratar_numeros(numero):
    return int(re.sub('[^0-9]','',numero))
