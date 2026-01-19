import pandas as pd
import numpy as np
from functions.db import db_connect

"""
SCRIPT: Banco Mundial - Pagamento de Impostos (Horas de Preparo)
DESCRIÇÃO: Processa arquivo local 'Historical-data...xlsx' do Banco Mundial, 
           transforma dados (melt) e carrega estatísticas de impostos.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO (ARQUIVO LOCAL)
# =============================================================================
file_name = "Historical-data---COMPLETE-dataset-with-scores.xlsx"
print(f"Lendo arquivo: {file_name}")

# Pula as primeiras 3 linhas de cabeçalho
df = pd.read_excel(file_name, skiprows=3)

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO
# =============================================================================

print("Transformando dados (Melt)...")
# Transforma colunas de indicadores variáveis em linhas (unpivot/melt)
# Mantém 'Country code', 'Economy', etc. como identificadores
df = pd.melt(df,id_vars=['Country code','Economy','Region','Income group','DB Year'], var_name='NM_INDICADOR', value_name='VL_INDICADOR').sort_values('Economy')

df.reset_index(drop=True,inplace=True)

# Renomeia colunas para o banco
df.columns = ['COD_ISO_PAIS','NM_PAIS','NM_REGIAO ','NM_GRUPO_RENDA','ANO','NM_INDICADOR','VL_INDICADOR']

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')

# CORREÇÃO: Variável original era 'df1' (que não existia), corrigido para 'df'
cols = list(df.columns)

df.to_sql('BANCO_MUNDIAL_PAGAMENTO_IMPOSTOS', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")
