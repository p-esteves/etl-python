import pandas as pd
import numpy as np
import openpyxl
import xlrd
from functions.db import db_connect

df = pd.read_excel("https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2018/projecoes_2018_populacao_2010_2060_20200406.xls",skiprows=50,skipfooter=220,sheet_name='BRASIL')

df = pd.melt(df,id_vars=['GRUPO ETÁRIO'], var_name='ANO', value_name='VL_POP_ESTIMADA').sort_values('ANO')

df.reset_index(drop=True,inplace=True)

#inserir
con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)
df.to_sql('PROJECAO_POPULACAO_IBGE', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')
con.close()