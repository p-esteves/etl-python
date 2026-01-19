import pandas as pd
import numpy as np
import openpyxl
from functions.db import db_connect

"""
SCRIPT: ANP - Preços de Combustíveis
DESCRIÇÃO: Extrai dados mensais de preços de combustíveis da ANP (Excel), processa e salva no banco.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO DE DADOS
# =============================================================================
# URL do arquivo Excel da ANP
url_anp = "http://www.anp.gov.br/images/Precos/Mensal2013/MENSAL_MUNICIPIOS-DESDE_Jan2013.xlsx"

print("Baixando e lendo arquivo Excel da ANP...")
# Lê o Excel pulando as primeiras 16 linhas (cabeçalho/metadados do arquivo original)
df = pd.read_excel(url_anp, skiprows=16)

# Renomeia colunas para o padrão do banco de dados
df.columns = ['DT_DADO','NM_PRODUTO','NM_REGIAO','NM_UF','NM_MUN','VL_POSTOS_PESQUISADOS','NM_UNIDADE_MEDIDA',
'VL_MED_REVENDA','VL_DP_REVENDA','VL_MIN_REVENDA','VL_MAX_REVENDA','VL_MARGEM_MED_REVENDA','VL_CV_REVENDA',
'VL_MED_DIST','VL_DP_DIST','VL_MIN_DIST','VL_MAX_DIST','VL_CV_DIST']

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO
# =============================================================================

print("Formatando colunas numéricas e de data...")

# Lista de colunas numéricas que precisam ser convertidas/coagidas para numeric
cols = ['VL_MED_REVENDA','VL_DP_REVENDA','VL_MIN_REVENDA','VL_MAX_REVENDA','VL_MARGEM_MED_REVENDA','VL_CV_REVENDA',
'VL_MED_DIST','VL_DP_DIST','VL_MIN_DIST','VL_MAX_DIST','VL_CV_DIST']

# Aplica conversão numérica forçando erros a virarem NaN (errors='coerce')
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)

# Converte coluna de data
df['DT_DADO'] = pd.to_datetime(df['DT_DADO'])

# =============================================================================
# PASSO 3: CARGA NO BANCO DE DADOS
# =============================================================================

print("Iniciando carga no banco...")
con = db_connect(package = 'sqlalchemy')
col_names = list(df.columns)

# Insere na tabela LEVANTAMENTO_PRECO_COMBUSTIVEIS
df.to_sql('LEVANTAMENTO_PRECO_COMBUSTIVEIS', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(col_names) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")