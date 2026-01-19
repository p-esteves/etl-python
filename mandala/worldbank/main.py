import pandas as pd
import numpy as np
import os, collections, csv
from functions.db import db_connect

"""
SCRIPT: Indicadores Banco Mundial
DESCRIÇÃO: Busca múltiplos indicadores via API do Banco Mundial e cruza com dados de países 
           de outra tabela do banco de dados (DDTM_OBSERVATORIO_1).
"""

# Dicionário de indicadores e seus URLs de download (Excel)
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

# =============================================================================
# PASSO 1: OBTENÇÃO DE DADOS DE PAÍSES (DO BANCO)
# =============================================================================
# Conecta ao banco 'DDTM_OBSERVATORIO_1' para buscar referência de países
print("Buscando lista de países no banco de dados...")
con = db_connect(db_name="DDTM_OBSERVATORIO_1")
query = "SELECT NM_PAIS,COD_PAIS_ISOA3 FROM COMEX_PAIS_D"
df_pais = pd.read_sql(query,con)

# Fecha conexão (será reaberta depois p/ outro banco se necessário, ou mesmo banco)
try:
    con.close()
except:
    pass

# =============================================================================
# PASSO 2: EXTRAÇÃO E TRANSFORMAÇÃO DOS INDICADORES
# =============================================================================
df={}

print("Iniciando loop de download e processamento...")
for tabela,url in zip(bases_dic.keys(),bases_dic.values()):
    print(f"Processando: {tabela}")
    
    # Lê Excel baixado da API
    df[tabela] = pd.read_excel(url,sheet_name='Data',skiprows=range(3))
    
    # Adiciona nome do indicador customizado
    df[tabela]['Indicator Name'] = tabela

    # Melt (Unpivot) para transformar anos em linhas
    df[tabela] = pd.melt(df[tabela],id_vars=['Country Code','Country Name','Indicator Name','Indicator Code'], var_name='Ano', value_name='Valor').sort_values('Country Name')

    df[tabela].reset_index(drop=True,inplace=True)

    # Merge com tabela de países para obter códigos ISO padronizados
    df[tabela] = df[tabela].merge(df_pais,how="left",left_on="Country Code",right_on="COD_PAIS_ISOA3")

    # Limpeza de colunas duplicadas/desnecessárias
    del df[tabela]['COD_PAIS_ISOA3'],df[tabela]['Country Name']

    # Renomeia colunas
    df[tabela].columns = ["COD_PAIS_ISOA3","NM_INDICADOR","COD_INDICADOR", "ANO","VL_INDICADOR","NM_PAIS"]

    # Reordena colunas
    df[tabela] = df[tabela][["COD_PAIS_ISOA3","NM_PAIS","COD_INDICADOR","NM_INDICADOR", "VL_INDICADOR","ANO"]]

# Concatena todos os dataframes do dicionário em um único
print("Consolidando dados...")
df_final = pd.concat(df.values())
df_final.reset_index(drop=True,inplace=True)

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================
print("Carga no banco final...")

# Conecta ao banco principal (default DDTM_OBSERVATORIO_2)
con = db_connect(package = 'sqlalchemy')

cols = list(df_final.columns)

df_final.to_sql('INDICADORES_BANCO_MUNDIAL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")
