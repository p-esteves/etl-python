import pandas as pd
from functions.db import db_connect

"""
SCRIPT: Encargos Trabalhistas (OECD Wage)
DESCRIÇÃO: Lê arquivo CSV com dados de salários/encargos da OCDE e carrega no banco.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO (ARQUIVO LOCAL)
# =============================================================================
print("Lendo CSV local...")
df = pd.read_csv("AWCOMP_11032021153151077.csv")

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO
# =============================================================================

# Renomeia colunas
df.columns = ['COD_INDICADOR','NM_INDICADOR','COD_TIPO_FAMILIA','NM_TIPO_FAMILIA','COD_PAIS_ISO','NM_PAIS','ANO','DELETAR','COD_UNIDADE_MEDIDA','NM_UNIDADE_MEDIDA','COD_POWERCODE','NM_POWERCODE','COD_PERIODO_REFERENCIA','NM_PERIODO_REFERENCIA','VL_INDICADOR','COD_FLAG','FLAG_INDICADOR']

# Remove coluna marcada para deletar
del df['DELETAR']

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)
df.to_sql('ENCARGOS_MEDIA_OCDE', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")
