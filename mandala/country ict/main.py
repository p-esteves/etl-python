import pandas as pd
import numpy as np
import os, collections, csv
from functions.db import db_connect

df = pd.read_excel('https://www.itu.int/en/ITU-D/Statistics/Documents/statistics/2020/FixedBroadbandSubscriptions_2000-2019.xlsx')

df = pd.melt(df,id_vars=['Indicator','Country'], var_name='Indicador Ano', value_name='Valor Indicador').sort_values('Country')

df.columns = ["NM_VARIAVEL","NM_PAIS","ANO","NM_VALOR_INDICADOR"]

df[['ANO','NM_TIPO_INDICADOR']] = df.ANO.str.split("_",expand=True,)

df.reset_index(drop=True,inplace=True)

con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)

df.to_sql('ASSINATURAS_BANDA_LARGA_MUNDIAL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

con.close()
