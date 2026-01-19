import pandas as pd
from functions.db import db_connect
import requests
from bs4 import BeautifulSoup

"""
SCRIPT: CDS - Risco País Brasil (5 anos)
DESCRIÇÃO: Realiza web scraping da taxa de risco país (CDS 5 anos) do site World Government Bonds.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO DE DADOS (WEB SCRAPING)
# =============================================================================
url = 'http://www.worldgovernmentbonds.com/cds-historical-data/brazil/5-years/'

print(f"Acessando URL: {url}")
# Realiza a requisição HTTP
html = requests.get(url).content

# Lê as tabelas HTML encontradas na página
print("Lendo tabelas HTML...")
df_list = pd.read_html(html)

# Seleciona a segunda tabela (índice 1) que contém os dados históricos
df = df_list[1]

print("Dados extraídos:")
print(df.head())

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO
# =============================================================================

# Renomeia colunas para português/padrão banco
df.columns = ['ANO','NM_MUDANÇA','VL_MINIMO','RANGE','VL_MAXIMO']

# Remove coluna 'RANGE' que não será utilizada
del df['RANGE']

# Limpeza das colunas de valor (Mínimo e Máximo)
# O split remove sufixos/unidades que possam vir junto com o número (separado por espaço)
df["VL_MAXIMO"]= df["VL_MAXIMO"].str.split(" ", n = 1, expand = True)
df["VL_MINIMO"]= df["VL_MINIMO"].str.split(" ", n = 1, expand = True)

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================

print("Carregando no banco de dados...")
# Conexão segura via variáveis de ambiente
con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)

# Insere na tabela CDS_RISCO_PAIS_BRASIL
df.to_sql('CDS_RISCO_PAIS_BRASIL', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")
