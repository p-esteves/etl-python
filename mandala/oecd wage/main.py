import pandas as pd
from functions.db import db_connect

df = pd.read_csv("AWCOMP_11032021153151077.csv")

df.columns = ['COD_INDICADOR','NM_INDICADOR','COD_TIPO_FAMILIA','NM_TIPO_FAMILIA','COD_PAIS_ISO','NM_PAIS','ANO','DELETAR','COD_UNIDADE_MEDIDA','NM_UNIDADE_MEDIDA','COD_POWERCODE','NM_POWERCODE','COD_PERIODO_REFERENCIA','NM_PERIODO_REFERENCIA','VL_INDICADOR','COD_FLAG','FLAG_INDICADOR']

del df['DELETAR']

#inserir
con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)
df.to_sql('ENCARGOS_MEDIA_OCDE', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

con.close()
