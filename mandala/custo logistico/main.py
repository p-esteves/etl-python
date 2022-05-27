import pandas as pd
import numpy as np
import os, collections, csv
from functions.db import db_connect
import html5lib
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml.html as lh

#url = "https://www.3plogistics.com/3pl-market-info-resources/3pl-market-information/global-3pl-market-size-estimates/"

#df.columns = ["NM_VARIAVEL","NM_PAIS","ANO","NM_VALOR_INDICADOR"]

#df.reset_index(drop=True,inplace=True)

df = pd.read_excel("dados.xlsx")

df.drop(df.iloc[:, 6:10], inplace=True, axis=1)

con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)
df.to_sql('CUSTO_LOGISTICO', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')
con.close()
