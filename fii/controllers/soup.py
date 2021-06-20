#!python3
import requests
from bs4 import BeautifulSoup

def get_soap_url(url, parser='html.parser', execute=False, tentativa=0):
    try:

        page = requests.get(url)
        soup = BeautifulSoup(page.content,parser)
        
        return soup

    except Exception as e:
        contagem_tentativas = tentativa + 1

        if contagem_tentativas < 3 and execute:
            get_soap_url(execute=True, tentativa=contagem_tentativas)
        
        pass

