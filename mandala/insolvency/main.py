import pandas as pd
import numpy as np
from functions.db import db_connect

df = pd.read_excel("Resolving Insolvency.xlsx")
df.columns = ["REMOVER","NM_REGIAO","VL_RANK_INDICADOR","VL_ESCORE_INDICADOR","VL_TAXA_RECUPERACAO","VL_TEMPO","VL_CUSTO","FLAG_RESULTADO","VL_GRAU_INDICADOR"]

#df.REMOVER.unique()

#filtrar "regiao" primeira col
#df = df.loc[df['DELETAR'] =! "Region"]
#filtrar location primeira col
#df = df.loc[df['DELETAR'] =! "Location"]
#ou apagar linhas 6 e 10....
#deletar primeira coluna

df = df[df['VL_RANK_INDICADOR'].notna()]

del df['REMOVER']

#inserir
con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)
df.to_sql('TAXA_RECUPERACAO_FINANCEIRA', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

con.close()

