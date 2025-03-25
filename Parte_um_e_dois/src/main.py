import logging
import os
from settings import CAMINHO_ANEXO_UM, PASTA_CSV, PASTA_PDFS, URL, ZIP_NOME, ZIP_NOME_CSV
from scraper.web_scraping_gov import acesso_pagina, busca_arquivos_pdf
from compactor_archives.compactor import compactar_arquivos
from transformation.data_transformation import transformacao_dados_csv

def main():
    while True:
        try:
            opcao = int(input("Digite o número referente à tarefa (0-Sair, 1-Web Scraping, 2-Transformação de dados): "))
        except ValueError:
            logging.error("Entrada inválida. Digite 0, 1 ou 2.")
            continue

        if opcao == 0:
            break
        elif opcao == 1:
            soup = acesso_pagina(URL)
            if soup:
                busca_arquivos_pdf(soup, URL)
                if os.listdir(PASTA_PDFS): 
                    compactar_arquivos(PASTA_PDFS, ZIP_NOME)
                else:
                    logging.warning("Nenhum arquivo foi baixado para compactação.")
                    continue
        elif opcao == 2:
            if os.path.exists(CAMINHO_ANEXO_UM):
                transformacao_dados_csv(CAMINHO_ANEXO_UM)
                compactar_arquivos(PASTA_CSV,ZIP_NOME_CSV)
            else:
                logging.error(f"Arquivo {CAMINHO_ANEXO_UM} não encontrado.")
        else:
            logging.warning("Opção inválida. Digite 0, 1 ou 2.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()