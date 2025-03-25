
import logging
import os
import shutil
from settings import PASTA_DATA_ZIP, PASTA_PDFS


def compactar_arquivos(pasta_pdfs,tipo_arquivo):
    try:
        caminho_zip = os.path.join(PASTA_DATA_ZIP, tipo_arquivo)
        
        shutil.make_archive(caminho_zip, 'zip', pasta_pdfs)
        logging.info(f"Compactação concluída: {tipo_arquivo}")
    
        
    except Exception as e:
        logging.error(f"Erro ao compactar arquivos: {e}")