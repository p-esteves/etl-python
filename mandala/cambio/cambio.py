import pandas as pd
import numpy as np
#from datetime import datetime
from functions.db import db_connect
import ipeadatapy

"""
SCRIPT: Taxa de Câmbio (IPEADATA)
DESCRIÇÃO: Busca dados de taxa de câmbio via API do Ipeadata.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO DO IPEADATA
# =============================================================================
# Código da série: BM_ERV 
print("Extraindo série BM_ERV do Ipeadata...")
df = ipeadatapy.timeseries('BM_ERV')

# Salva temporariamente em CSV e lê novamente (pode ser uma forma de limpar/formatar que o autor original encontrou)
# Idealmente poderiamos trabalhar direto com o df retornado, mas manteremos a lógica original.
df.to_csv('df.csv',sep=',')
df1 = pd.read_csv('df.csv')

# Renomeia colunas
# O CSV gerado pelo ipeadatapy tem estrutura específica
df1.columns = ['DT_DADO','ANO','VL_DIA','VL_MES','NM_CODIGO_API','DT_COMPLETA','VL_TAXA']

# Seleciona apenas colunas de interesse
df1 = df1[['VL_TAXA','DT_DADO']]

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO
# =============================================================================

# Conversão de tipos
df1['DT_DADO'] = pd.to_datetime(df1['DT_DADO'])
df1['VL_TAXA'] = pd.to_numeric(df1['VL_TAXA'])

# Lógica comentada no original mantida como comentário
#df1['ANO'] = df.loc[df['ANO']>=prime] 

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')
cols = list(df1.columns)

# Tabela: TAXA_CAMBIO_MEDIA_ANUAL
df1.to_sql('TAXA_CAMBIO_MEDIA_ANUAL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")