import pandas as pd
import numpy as np
import openpyxl
import xlrd
from functions.db import db_connect

"""
SCRIPT: Projeção de População (IBGE)
DESCRIÇÃO: Extrai dados de projeção populacional (2010-2060) do IBGE, transforma e carrega no banco.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO
# =============================================================================
url = "https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2018/projecoes_2018_populacao_2010_2060_20200406.xls"
print(f"Baixando dados do IBGE: {url}")

# Lê Excel pulando 50 linhas de metadados e ignorando rodapé
df = pd.read_excel(url, skiprows=50, skipfooter=220, sheet_name='BRASIL')

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO (MELT)
# =============================================================================

print("Transformando dados...")
# Transforma colunas de anos em linhas
df = pd.melt(df,id_vars=['GRUPO ETÁRIO'], var_name='ANO', value_name='VL_POP_ESTIMADA').sort_values('ANO')

df.reset_index(drop=True,inplace=True)

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)
df.to_sql('PROJECAO_POPULACAO_IBGE', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")