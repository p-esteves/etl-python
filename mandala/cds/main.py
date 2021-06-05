import pandas as pd
from functions.db import db_connect
import requests
from bs4 import BeautifulSoup

url = 'http://www.worldgovernmentbonds.com/cds-historical-data/brazil/5-years/'
html = requests.get(url).content
df_list = pd.read_html(html)

df = df_list[1]

print(df)

df.columns = ['ANO','NM_MUDANÇA','VL_MINIMO','RANGE','VL_MAXIMO']
del df['RANGE']

df["VL_MAXIMO"]= df["VL_MAXIMO"].str.split(" ", n = 1, expand = True)
df["VL_MINIMO"]= df["VL_MINIMO"].str.split(" ", n = 1, expand = True)

#inserir
con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)
df.to_sql('CDS_RISCO_PAIS_BRASIL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

con.close()
