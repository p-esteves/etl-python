import pandas as pd
import numpy as np
import os, collections, csv
from functions.db import db_connect
import html5lib
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml.html as lh

"""
SCRIPT: Custo Logístico (3PL)
DESCRIÇÃO: Lê dados de arquivo local 'dados.xlsx' (extraído manualmente da fonte 3PL?),
           remove colunas indesejadas e carrega no banco.
"""

# =============================================================================
# PASSO 1: LEITURA DE DADOS
# =============================================================================
#url = "https://www.3plogistics.com/3pl-market-info-resources/3pl-market-information/global-3pl-market-size-estimates/"

# Lê arquivo local (o script assume que este arquivo existe no diretório de execução)
print("Lendo 'dados.xlsx'...")
try:
    df = pd.read_excel("dados.xlsx")
except FileNotFoundError:
    print("ERRO: O arquivo 'dados.xlsx' não foi encontrado.")
    # Poderiamos levantar erro ou sair, mas seguiremos caso o usuário coloque o arquivo
    raise

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO
# =============================================================================

# Remove colunas específicas pelo índice (colunas 6 a 9)
# Provavelmente colunas de cálculo intermediário ou comentários do Excel original
print("Removendo colunas desnecessárias...")
df.drop(df.iloc[:, 6:10], inplace=True, axis=1)

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)

df.to_sql('CUSTO_LOGISTICO', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")
