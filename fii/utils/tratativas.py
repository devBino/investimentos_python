#!python3

def tratar_dados_fii(dados):
    
    lista = []
    
    for d in dados:
        l = d
        l['valor'] = tratar_numeros(d['valor'])
        lista.append(l)

    return lista


def tratar_numeros(numero):
    
    num = numero.strip()
    chars = '0123456789,'
    novo_num = ''

    for c in num:
        if c in chars:
            novo_num += c
    
    novo_num = novo_num.replace(',','.')

    return novo_num
