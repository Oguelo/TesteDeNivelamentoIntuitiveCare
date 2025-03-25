import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from settings import PASTA_PDFS
import os

os.makedirs(PASTA_PDFS, exist_ok=True)

def acesso_pagina(url):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        return BeautifulSoup(resposta.text, "html.parser")
    except requests.RequestException as e:
        logging.error(f"Erro ao acessar {url}: {e}")
        return None

def busca_arquivos_pdf(soup, base_url):
    pdf_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        nome_arquivo = href.split("/")[-1]
        if nome_arquivo.upper().startswith("ANEXO") and href.endswith(".pdf"):
            pdf_url = urljoin(base_url, href)
            pdf_links.append(pdf_url)
            
            try:
                pdf_resposta = requests.get(pdf_url, stream=True)
                pdf_resposta.raise_for_status()
                
                caminho_arquivo = os.path.join(PASTA_PDFS, nome_arquivo)
                with open(caminho_arquivo, "wb") as pdf_arquivo:
                    for chunk in pdf_resposta.iter_content(chunk_size=8192):
                        pdf_arquivo.write(chunk)
                logging.info(f"Download concluído: {nome_arquivo}")
            except requests.RequestException as e:
                logging.error(f"Erro ao baixar {pdf_url}: {e}")
    
    if not pdf_links:
        logging.warning("Nenhum PDF começando com 'ANEXO' encontrado.")
     


    

