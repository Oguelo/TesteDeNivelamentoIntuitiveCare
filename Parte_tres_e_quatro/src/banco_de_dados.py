import datetime
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from settings import DB_HOST, DB_NOME, DB_SENHA, DB_USUARIO

def conectar_mysql():
    """Conecta ao MySQL com SQLAlchemy"""
    engine = create_engine(f"mysql+pymysql://{DB_USUARIO}:{DB_SENHA}@{DB_HOST}/{DB_NOME}")
    return engine.connect()  # Retorna a conexão com o banco de dados

def criar_db():
    """Cria o banco de dados se não existir"""
    conn = pymysql.connect(host=DB_HOST, user=DB_USUARIO, password=DB_SENHA, charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NOME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.commit()
    conn.close()

from sqlalchemy import text

def executar_arquivo_sql(sql_file):
   
    conn = conectar_mysql()  # Conecta usando SQLAlchemy

    with open(sql_file, 'r', encoding='utf-8') as file:
        sql_commands = file.read()

    for command in sql_commands.split(';'):
        command = command.strip()
        if command:  # Verifica se o comando não está vazio
            conn.execute(text(command))  # Usa text() para transformar a string em uma consulta executável
    
    conn.close()  # Fecha a conexão após a execução



def obter_top_operadoras(periodo_meses=12, limite=10):
    conn = conectar_mysql()  # Função para conectar ao banco de dados MySQL
    
    # Definindo as datas de início e fim com base no período de 2023 a 2024
    data_inicio = '2023-01-01'  # Início do ano de 2023
    data_fim = '2024-12-31'     # Fim do ano de 2024
    
    # A consulta com placeholders para a descrição única e as datas
    query = """
    SELECT 
        r.Razao_Social AS Operadora,
        SUM(c.VL_SALDO_FINAL) AS Total_Despesas
    FROM 
        contas c
    JOIN 
        registros_ans r ON c.REG_ANS = r.Registro_ANS
    WHERE 
        c.DESCRICAO LIKE %s
        AND c.DATA BETWEEN %s AND %s
    GROUP BY 
        r.Razao_Social
    ORDER BY 
        Total_Despesas DESC
    LIMIT %s
    """

    # Parâmetro com a descrição única
    params = ('%EVENTOS/ SINISTROS CONHECIDOS%', data_inicio, data_fim, limite)

    try:
        # Usando o read_sql com parâmetros passados corretamente
        df = pd.read_sql(query, conn, params=params)
        return df
    finally:
        conn.close()
