import pandas as pd
import numpy as np
from functions.db import db_connect

df = pd.read_excel("Historical-data---COMPLETE-dataset-with-scores.xlsx",skiprows=3)

df = pd.melt(df,id_vars=['Country code','Economy','Region','Income group','DB Year'], var_name='NM_INDICADOR', value_name='VL_INDICADOR').sort_values('Economy')

df.reset_index(drop=True,inplace=True)

df.columns = ['COD_ISO_PAIS','NM_PAIS','NM_REGIAO ','NM_GRUPO_RENDA','ANO','NM_INDICADOR','VL_INDICADOR']

#inserir
con = db_connect(package = 'sqlalchemy')

cols = list(df1.columns)
df.to_sql('BANCO_MUNDIAL_PAGAMENTO_IMPOSTOS', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

con.close()
