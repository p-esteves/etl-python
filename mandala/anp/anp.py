import pandas as pd
import numpy as np
import openpyxl
from functions.db import db_connect

df = pd.read_excel("http://www.anp.gov.br/images/Precos/Mensal2013/MENSAL_MUNICIPIOS-DESDE_Jan2013.xlsx",skiprows=16)

df.columns = ['DT_DADO','NM_PRODUTO','NM_REGIAO','NM_UF','NM_MUN','VL_POSTOS_PESQUISADOS','NM_UNIDADE_MEDIDA',
'VL_MED_REVENDA','VL_DP_REVENDA','VL_MIN_REVENDA','VL_MAX_REVENDA','VL_MARGEM_MED_REVENDA','VL_CV_REVENDA',
'VL_MED_DIST','VL_DP_DIST','VL_MIN_DIST','VL_MAX_DIST','VL_CV_DIST']

#dividir coluna de dado em mes e ano por separador '/'?

#conversao floats
cols = ['VL_MED_REVENDA','VL_DP_REVENDA','VL_MIN_REVENDA','VL_MAX_REVENDA','VL_MARGEM_MED_REVENDA','VL_CV_REVENDA',
'VL_MED_DIST','VL_DP_DIST','VL_MIN_DIST','VL_MAX_DIST','VL_CV_DIST']

df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)

df['DT_DADO'] = pd.to_datetime(df['DT_DADO'])

#inserir
con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)
df.to_sql('LEVANTAMENTO_PRECO_COMBUSTIVEIS', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')
con.close()