import pandas as pd
import numpy as np
from functions.db import db_connect

df = pd.read_csv("https://s3.amazonaws.com/datascope-ast-datasets-nov29/datasets/53/data.csv")

df = pd.melt(df,id_vars=['Country ISO3','Country Name','Indicator Id','Indicator','Subindicator Type'], var_name='Periodo', value_name='Valor').sort_values('Country ISO3')
df.columns = ["NM_ISO3_PAIS","NM_PAIS","COD_INDICADOR","NM_INDICADOR","NM_TIPO_SUBINDICADOR","NM_PERIODO","VL_INDICADOR"]
df.reset_index(drop=True,inplace=True)

#conversoes


#inserir
con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)
df.to_sql('INDICE_COMPETITIVIDADE_GLOBAL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

con.close()
