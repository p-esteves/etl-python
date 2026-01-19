import pandas as pd
import numpy as np
from functions.db import db_connect

"""
SCRIPT: Índice de Competitividade Global (Pilares)
DESCRIÇÃO: Baixa dados de competitividade (CSV), faz unpivot (melt) e carrega no banco.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO
# =============================================================================
url = "https://s3.amazonaws.com/datascope-ast-datasets-nov29/datasets/53/data.csv"
print(f"Baixando dados: {url}")
df = pd.read_csv(url)

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO
# =============================================================================
print("Transformando dados (Melt)...")

# Transforma colunas de período em linhas
df = pd.melt(df,id_vars=['Country ISO3','Country Name','Indicator Id','Indicator','Subindicator Type'], var_name='Periodo', value_name='Valor').sort_values('Country ISO3')

# Renomeia para português
df.columns = ["NM_ISO3_PAIS","NM_PAIS","COD_INDICADOR","NM_INDICADOR","NM_TIPO_SUBINDICADOR","NM_PERIODO","VL_INDICADOR"]

df.reset_index(drop=True,inplace=True)

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)
df.to_sql('INDICE_COMPETITIVIDADE_GLOBAL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")
