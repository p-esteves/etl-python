import pandas as pd
import numpy as np
import pyodbc
from functions.db import db_connect

"""
SCRIPT: Consumo de Gás Natural (ANP)
DESCRIÇÃO: Extrai dados do anuário da ANP via CSV, formata tipos e carrega no banco.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO
# =============================================================================
url = 'http://www.anp.gov.br/arquivos/dadosabertos/anuario2020/anuario-2020-abertos-tabela1.8.csv'
print(f"Baixando CSV: {url}")

# Lê CSV com separador ';'
df = pd.read_csv(url,sep=';')

# Renomeia colunas
df.columns = ["NM_REGIAO","NM_PAIS","VL_CONSUMO_GAS","ANO"]

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO
# =============================================================================

print("Limpando dados...")
# Conversão do valor de consumo para float
df["VL_CONSUMO_GAS"] = pd.to_numeric(df["VL_CONSUMO_GAS"], downcast="float")

# Conversão do ano para string
df[['ANO']] = df[['ANO']].astype(str)

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)

df.to_sql('CONSUMO_GAS_NATURAL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")
