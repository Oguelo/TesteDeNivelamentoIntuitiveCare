import pandas as pd
import chardet
import pymysql

def detectar_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def converter_utf8_sem_salvar(input_file):
    encoding = detectar_encoding(input_file)
    df = pd.read_csv(input_file, encoding=encoding, delimiter=';')
    return df  

def inserir_dados_formatados(df, table_name, db_host, db_user, db_pass, db_name):
    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name, charset='utf8mb4')
    cursor = conn.cursor()
    
    if 'Telefone' in df.columns:
        df['Telefone'] = df['Telefone'].apply(lambda x: str(int(float(x))) if pd.notna(x) and isinstance(x, (int, float)) else str(x))
    

    
    if 'data' in df.columns:
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce').dt.strftime('%Y-%m-%d')
        df['data'] = df['data'].apply(lambda x: None if pd.isnull(x) else x)  # Para garantir que as datas inválidas se tornem NULL

    if 'Numero' in df.columns:
        df['Numero'] = df['Numero'].astype(str).str.replace(r'[^0-9A-Za-z.-]', '', regex=True)

    for col in ['VL_SALDO_INICIAL', 'VL_SALDO_FINAL']: 
        if col in df.columns:
            df[col] = df[col].apply(lambda x: str(x).replace(',', '.') if pd.notna(x) else x)

    placeholders = ', '.join(['%s'] * len(df.columns))
    columns = ', '.join([f"`{col}`" for col in df.columns])
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    values = [tuple(str(value).strip() if pd.notna(value) else None for value in row) for row in df.values]

    cursor.executemany(query, values)
    conn.commit()
    conn.close()
