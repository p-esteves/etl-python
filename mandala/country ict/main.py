import pandas as pd
import numpy as np
import os, collections, csv
from functions.db import db_connect

"""
SCRIPT: ITU - Assinaturas de Banda Larga
DESCRIÇÃO: Baixa dados de assinaturas de banda larga da ITU (International Telecommunication Union),
           transforma de formato wide para long (pivot) e salva no banco.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO DE DADOS
# =============================================================================
url = 'https://www.itu.int/en/ITU-D/Statistics/Documents/statistics/2020/FixedBroadbandSubscriptions_2000-2019.xlsx'
print(f"Baixando dados da ITU: {url}")

df = pd.read_excel(url)

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO (UNPIVOT)
# =============================================================================

# O arquivo original provavelmente tem anos como colunas. 
# Usamos melt para transformar colunas de anos em linhas (formato 'tidy data')
print("Transformando dados (Melt)...")
df = pd.melt(df,id_vars=['Indicator','Country'], var_name='Indicador Ano', value_name='Valor Indicador').sort_values('Country')

# Renomeia para padrão do banco
df.columns = ["NM_VARIAVEL","NM_PAIS","ANO","NM_VALOR_INDICADOR"]

# A coluna "Indicador Ano" (agora ANO) possivelmente vinha com algum sufixo ou formatação com "_"
# O split separa isso.
# Ex: Se vinha "2010_est", pega o "2010" e o "est"
df[['ANO','NM_TIPO_INDICADOR']] = df.ANO.str.split("_",expand=True,)

# Reseta o índice após as operações
df.reset_index(drop=True,inplace=True)

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)

df.to_sql('ASSINATURAS_BANDA_LARGA_MUNDIAL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")
