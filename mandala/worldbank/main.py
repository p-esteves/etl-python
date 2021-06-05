import pandas as pd
import numpy as np
import os, collections, csv
from functions.db import db_connect

bases_dic = {
    "Quantidade de negócios abertos":"http://api.worldbank.org/v2/en/indicator/IC.BUS.NREG?downloadformat=excel",
    "Gap do custo de abrir um negócio (%)":"http://api.worldbank.org/v2/en/indicator/IC.REG.COST.PC.ZS?downloadformat=excel",
    "PIB per capita (em dólares)":"http://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=excel",
    "Gap do tempo de abrir um negócio (%)":"http://api.worldbank.org/v2/en/indicator/IC.REG.DURS?downloadformat=excel",
    "PIB per capita PPP, preços constantes":"http://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.PP.KD?downloadformat=excel",
    "Encargos Brasil (porcentagem do PIB)":"http://api.worldbank.org/v2/en/indicator/GC.TAX.TOTL.GD.ZS?downloadformat=excel",
    "Taxa de impostos em relação aos lucros":"http://api.worldbank.org/v2/en/indicator/IC.TAX.TOTL.CP.ZS?downloadformat=excel",
    "Taxa de impostos sobre exportações":"http://api.worldbank.org/v2/en/indicator/GC.TAX.EXPT.ZS?downloadformat=excel",
    "Spread da taxa de juros (lending rate minus deposite rate)":"http://api.worldbank.org/v2/en/indicator/FR.INR.LNDP?downloadformat=excel"
}

con = db_connect(db_name="DDTM_OBSERVATORIO_1")

query = "SELECT NM_PAIS,COD_PAIS_ISOA3 FROM COMEX_PAIS_D"
df_pais = pd.read_sql(query,con)

df={}

for tabela,url in zip(bases_dic.keys(),bases_dic.values()):
    df[tabela] = pd.read_excel(url,sheet_name='Data',skiprows=range(3))
    
    df[tabela]['Indicator Name'] = tabela

    df[tabela] = pd.melt(df[tabela],id_vars=['Country Code','Country Name','Indicator Name','Indicator Code'], var_name='Ano', value_name='Valor').sort_values('Country Name')

    df[tabela].reset_index(drop=True,inplace=True)

    df[tabela] = df[tabela].merge(df_pais,how="left",left_on="Country Code",right_on="COD_PAIS_ISOA3")

    del df[tabela]['COD_PAIS_ISOA3'],df[tabela]['Country Name']

    df[tabela].columns = ["COD_PAIS_ISOA3","NM_INDICADOR","COD_INDICADOR", "ANO","VL_INDICADOR","NM_PAIS"]
    #df[tabela].rename(columns={'Indicator Name':'NM_INDICADOR'},inplace=True)

    df[tabela] = df[tabela][["COD_PAIS_ISOA3","NM_PAIS","COD_INDICADOR","NM_INDICADOR", "VL_INDICADOR","ANO"]]

    #print(df[tabela])

df_final = pd.concat(df.values())

df_final.reset_index(drop=True,inplace=True)

'''
print(df_final)

df_filtrado = df_final.loc[df_final['NM_PAIS'].isna()]
df_filtrado['COD_PAIS_ISOA3'].drop_duplicates()

'''

#INSERIR NO BANCO

con = db_connect(package = 'sqlalchemy')

cols = list(df_final.columns)

df_final.to_sql('INDICADORES_BANCO_MUNDIAL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

con.close()
