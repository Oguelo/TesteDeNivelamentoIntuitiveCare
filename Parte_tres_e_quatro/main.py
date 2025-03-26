import os
from settings import CSV_FILE_CADASTRAL, CSV_FILES_CONTAS, DB_HOST, DB_NOME, DB_SENHA, DB_USUARIO
from src.banco_de_dados import criar_db, executar_arquivo_sql, obter_top_operadoras
from src.importador import converter_utf8_sem_salvar, inserir_dados_formatados


print("=== Top 10 Operadoras - Último Trimestre ===")
df_trimestre = obter_top_operadoras(periodo_meses=3)
print(df_trimestre.to_string(index=False))


print("\n=== Top 10 Operadoras - Último Ano ===")
df_ano = obter_top_operadoras(periodo_meses=12)
print(df_ano.to_string(index=False))
