import tabula
import pandas as pd
import os
from settings import PASTA_CSV

def transformacao_dados_csv(arquivo_pdf):
    """
    Transforma tabelas do PDF em CSV, substituindo valores E cabeçalhos
    com o mesmo mapeamento.
    """
    os.makedirs(PASTA_CSV, exist_ok=True)
    
    try:
      
        dfs = tabula.read_pdf(
            arquivo_pdf,
            pages="3-181",
            multiple_tables=True,
            lattice=True,
            guess=False
        )
        
        if not dfs:
            print("Nenhuma tabela encontrada no PDF.")
            return False

       
        substituicoes = {
            'OD': 'Seg. Odontológica',
            'AMB': 'Seg. Ambulatória'
        }

        dfs_processados = []
        for df in dfs:
           
            df = df.dropna(how='all').dropna(axis=1, how='all')
            df = df.map(lambda x: str(x).strip() if pd.notna(x) else "")
            
            if not df.empty:
             
                for col_original, substituto in substituicoes.items():
                    if col_original in df.columns:
                        df[col_original] = df[col_original].str.replace(
                            rf'\b{col_original}\b', substituto, regex=True
                        )
                
              
                df.rename(columns=substituicoes, inplace=True)
                
                dfs_processados.append(df)

        if not dfs_processados:
            print("Nenhuma tabela válida após processamento.")
            return False

        df_final = pd.concat(dfs_processados, ignore_index=True)
        
       
        caminho_csv = os.path.join(PASTA_CSV, "dados_consolidados.csv")
        df_final.to_csv(caminho_csv, index=False, encoding='utf-8-sig')
        
        return True

    except Exception as e:
        print(f"Erro: {str(e)}")
        return False