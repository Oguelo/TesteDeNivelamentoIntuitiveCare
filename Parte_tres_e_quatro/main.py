import os
from settings import CSV_FILE_CADASTRAL, CSV_FILES_CONTAS, DB_HOST, DB_NOME, DB_SENHA, DB_USUARIO
from src.banco_de_dados import criar_db, executar_arquivo_sql, obter_top_operadoras
from src.importador import converter_utf8_sem_salvar, inserir_dados_formatados


criar_db()
executar_arquivo_sql("financeiro.sql")  


if os.path.exists(CSV_FILE_CADASTRAL):
    df_cadastral = converter_utf8_sem_salvar(CSV_FILE_CADASTRAL)
    inserir_dados_formatados(df_cadastral, "registros_ans", DB_HOST, DB_USUARIO, DB_SENHA, DB_NOME)

for file in CSV_FILES_CONTAS:
    if os.path.exists(file):
        df_contas = converter_utf8_sem_salvar(file)
        inserir_dados_formatados(df_contas, "contas", DB_HOST, DB_USUARIO, DB_SENHA, DB_NOME)


print("=== Top 10 Operadoras - Último Trimestre ===")
df_trimestre = obter_top_operadoras(periodo_meses=3)
print(df_trimestre.to_string(index=False))

print("\n=== Top 10 Operadoras - Último Ano ===")
df_ano = obter_top_operadoras(periodo_meses=12)
print(df_ano.to_string(index=False))
