#!python3
import sys
import time
from datetime import date
from configs import busca_fiis
from odata import banco
from utils import tratativas
from controllers import soup


#carrega configurações para mapeamento das tags
configs = busca_fiis.get_configs()

# recupera fiis vindos como argumentos de sistema na linha de comando
fiis_escolhidos = sys.argv[1].lower().split(' ')
fiis_visitados = []
dic_fiis = []

def main(execute=False):
    
    time.sleep(1)

    if len(fiis_visitados) < len(fiis_escolhidos):

        indice_atual = len(fiis_visitados)

        print(f'Capturando dados do FII: ' + fiis_escolhidos[indice_atual],end=' => ')

        page_fii = soup.get_soap_url(configs['urlFii'] + fiis_escolhidos[indice_atual])

        titulos_indicadores = page_fii.find_all(configs['elementosDados'], class_=configs['classeTitulosIndicadores'])
        valores_indicadores = page_fii.find_all(configs['elementosDados'], class_=configs['classeValoresIndicadores'])
        valores_preco = page_fii.find_all(configs['elementoPreco'], class_=configs['classeDadosPreco'])
        
        if not (len(titulos_indicadores) > 0):
            fiis_visitados.append( fiis_escolhidos[indice_atual] )
            print('ERRO [Dados não encontrados]')
            main(execute=True)
        
        else:
            try:
                div_dividendos = page_fii.find(id='dividends')
                dados_dy = div_dividendos.table.tbody.find_all('tr')[1].find_all('td')

                dados_fii = {'nome':fiis_escolhidos[indice_atual],'dados':[]}

                for i in range(len(titulos_indicadores)):
                    titulo_indicador = busca_fiis.get_titulo_indicador(titulos_indicadores[i].text)
                    dados_fii['dados'].append({'indicador':titulo_indicador,'valor':valores_indicadores[i].text})

                dados_fii['dados'].append({'indicador':busca_fiis.get_titulo_indicador('preco'),'valor':valores_preco[0].text})
                dados_fii['dados'].append({'indicador':'dy3m','valor':dados_dy[2].text})
                dados_fii['dados'].append({'indicador':'dy6m','valor':dados_dy[3].text})
                dados_fii['dados'].append({'indicador':'dy12m','valor':dados_dy[4].text})

                dados_fii['dados'] = tratativas.tratar_dados_fii(dados_fii['dados'])

                dic_fiis.append( dados_fii )
                
                fiis_visitados.append( fiis_escolhidos[indice_atual] )
                
                time.sleep(1)

                print('OK')
                main(execute=True)

            except Exception as e:
                fiis_visitados.append( fiis_escolhidos[indice_atual] )
                print('ERRO [Dados não encontrados]')
                main(execute=True)

    else:
        atualizar_cotacoes()
#------------------------------------------------------------------------------------

def atualizar_cotacoes():
    
    for dados in dic_fiis:
        
        nome_fii = dados['nome']
        cotacao_fii = ''

        for dados_fii in dados['dados']:
            if dados_fii['indicador'] == 'cotacao':
                cotacao_fii = dados_fii['valor']
                break

        cotacao_fii = float(cotacao_fii)

        sql = "update papel set cotacao=%s where nmPapel=\"%s\" " % (str(cotacao_fii),nome_fii.upper())
        
        if banco.execute_update(sql) == True:
            print(f'Cotacao atualizada com sucesso para o FII {nome_fii}')
        else:
            print(f'Erro ao tentar atualizar o FII {nome_fii}')
    
    
#------------------------------------------------------------------------------------

main()