import pandas as pd
import numpy as np
import pyodbc
from functions.db import db_connect

#baixar e ler
df = pd.read_csv('http://www.anp.gov.br/arquivos/dadosabertos/anuario2020/anuario-2020-abertos-tabela1.8.csv',sep=';')

df.columns = ["NM_REGIAO","NM_PAIS","VL_CONSUMO_GAS","ANO"]

#vl consumo pra float
df["VL_CONSUMO_GAS"] = pd.to_numeric(df["VL_CONSUMO_GAS"], downcast="float")

#ano p string
df[['ANO']] = df[['ANO']].astype(str)

#inserir
con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)
df.to_sql('CONSUMO_GAS_NATURAL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')
con.close()
