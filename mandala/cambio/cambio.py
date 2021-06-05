import pandas as pd
import numpy as np
#from datetime import datetime
from functions.db import db_connect
import ipeadatapy

#atual = datetime.now().year
#prime = atual-10

df = ipeadatapy.timeseries('BM_ERV')

df.to_csv('df.csv',sep=',')
df1 = pd.read_csv('df.csv')

df1.columns = ['DT_DADO','ANO','VL_DIA','VL_MES','NM_CODIGO_API','DT_COMPLETA','VL_TAXA']

df1 = df1[['VL_TAXA','DT_DADO']]

df1['DT_DADO'] = pd.to_datetime(df1['DT_DADO'])
df1['VL_TAXA'] = pd.to_numeric(df1['VL_TAXA'])

#df1['ANO'] = df.loc[df['ANO']>=prime] 

#inserir
con = db_connect(package = 'sqlalchemy')
cols = list(df1.columns)
df1.to_sql('TAXA_CAMBIO_MEDIA_ANUAL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')
con.close()