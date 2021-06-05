import json
import pandas as pd
import numpy as np
from functions.db import db_connect

#baixar e ler

url="https://www.aneel.gov.br/dados/relatorios?p_p_id=dadosabertos_WAR_dadosabertosportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=gerarTarifaMediaFornecimentoJSON&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=1"

df = pd.read_json(url, encoding="Latin1")

df.columns = ["NM_REGIAO","VL_CONSUMO_MWH","ANO","VL_MES", "NM_CLASSE_CONSUMO","ID_LINHA","DT_REGISTRO"]

del df['ID_LINHA']

print(df)

#vl consumo pra float
df["VL_CONSUMO_MWH"] = pd.to_numeric(df["VL_CONSUMO_MWH"], downcast="float")
print(df)

#DT_REGISTRO pra data hora
df["DT_REGISTRO"] = pd.to_datetime(df["DT_REGISTRO"])
print(df)

#vl mes string
#ano p string
df[['ANO','VL_MES']] = df[['ANO','VL_MES']].astype(str)
print(df)

df.NM_CLASSE_CONSUMO.unique()

df['NM_CLASSE_CONSUMO'].replace('Comercial, Serviços e Outras','Comercial e Serviços e Outras',inplace=True)
df['NM_CLASSE_CONSUMO'].replace('Comercial, Serviços e Outras','Comercial e Serviços e Outras',inplace=True)
df['NM_CLASSE_CONSUMO'].replace('Residencia','Residencial',inplace=True)
df['NM_CLASSE_CONSUMO'].replace('Comercial e  Serviços e Outras','Comercial e Serviços e Outras',inplace=True)
df['NM_CLASSE_CONSUMO'].replace('Serviço Público (água, esgoto e saneamento)','Serviço Público (água e esgoto e saneamento)',inplace=True)
df['NM_CLASSE_CONSUMO'].replace('Serviço Público (água e  esgoto e saneamento)','Serviço Público (água e esgoto e saneamento)',inplace=True)
df['NM_CLASSE_CONSUMO'].replace('Totais por Região','Total por Região',inplace=True)

#inserir
con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)
df.to_sql('ENERGIA_TARIFAS_CLASSE_CONSUMO', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')
con.close()
