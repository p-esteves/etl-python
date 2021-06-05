import pandas as pd
import numpy as np
import openpyxl
from functions.db import db_connect

df = pd.read_csv("STP-20210304105835746.csv",sep=";")
df.columns = ['ANO','VL_PIB_RS_CORRENTES']

df = df[df.ANO != "Fonte"]

#inserir
con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)
df.to_sql('PIB_RS_CORRENTES', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')
con.close()