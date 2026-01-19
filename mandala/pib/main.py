import pandas as pd
import numpy as np
import openpyxl
from functions.db import db_connect

"""
SCRIPT: PIB (RS Correntes)
DESCRIÇÃO: Processa dados de PIB de arquivo CSV local e carrega no SQL.
"""

# =============================================================================
# PASSO 1: LEITURA E LIMPEZA
# =============================================================================
# Lê CSV com separador ';'
print("Lendo CSV...")
df = pd.read_csv("STP-20210304105835746.csv",sep=";")

# Renomeia colunas
df.columns = ['ANO','VL_PIB_RS_CORRENTES']

# Remove linhas de metadados/rodapé (onde ANO='Fonte')
df = df[df.ANO != "Fonte"]

# =============================================================================
# PASSO 2: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)
df.to_sql('PIB_RS_CORRENTES', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")