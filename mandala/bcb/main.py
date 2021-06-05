import pandas as pd
import numpy as np
import sgs
from functions.db import db_connect
from datetime import date

hj = date.today()
 
#Média anual do saldo da carteira de crédito - PJ
df1 = sgs.time_serie(20540,start="1/3/2007",end=hj)
df1 = pd.DataFrame({'DT_DADO':df1.index, 'VL_DADO':df1.values})

#Spread médio das operações de crédito - PJ
df2 = sgs.time_serie(20784,start="1/3/2011",end=hj)
df2= pd.DataFrame({'DT_DADO':df2.index, 'VL_DADO':df2.values})

#inserir
con = db_connect(package = 'sqlalchemy')

cols1 = list(df1.columns)
df1.to_sql('BANCO_CENTRAL_MEDIA_SALDO_CREDITO', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols1) + 1)), method = 'multi')

cols2 = list(df2.columns)
df2.to_sql('BANCO_CENTRAL_SPREAD_OPERACAO_CREDITO', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols2) + 1)), method = 'multi')

con.close()

 