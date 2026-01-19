import pandas as pd
import numpy as np
from functions.db import db_connect

"""
SCRIPT: Taxa de Recuperação Financeira (Insolvency)
DESCRIÇÃO: Processa dados de insolvência de arquivo excel local 'Resolving Insolvency.xlsx'.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO
# =============================================================================
print("Lendo 'Resolving Insolvency.xlsx'...")
df = pd.read_excel("Resolving Insolvency.xlsx")

# Renomeia colunas
# Nota: A primeira coluna está marcada para ser removida ("REMOVER")
df.columns = ["REMOVER","NM_REGIAO","VL_RANK_INDICADOR","VL_ESCORE_INDICADOR","VL_TAXA_RECUPERACAO","VL_TEMPO","VL_CUSTO","FLAG_RESULTADO","VL_GRAU_INDICADOR"]

# =============================================================================
# PASSO 2: LIMPEZA
# =============================================================================

# Filtro para manter apenas linhas com Vl_RANK_INDICADOR preenchido (não nulo)
df = df[df['VL_RANK_INDICADOR'].notna()]

# Remove coluna temporária/desnecessária
if 'REMOVER' in df.columns:
    del df['REMOVER']

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)
df.to_sql('TAXA_RECUPERACAO_FINANCEIRA', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")

