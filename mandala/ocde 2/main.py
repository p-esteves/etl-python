import pandas as pd
import numpy as np
from functions.db import db_connect

"""
SCRIPT: OCDE - Indicadores PMR (Product Market Regulation)
DESCRIÇÃO: Extrai dados de regulação de mercado (PMR) do Excel da OCDE, seleciona colunas relevantes e carrega no banco.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO
# =============================================================================
url = "https://www.oecd.org/economy/reform/OECD-PMR-Economy%20-Wide%20Indicator%20values-2018.xlsx"
print(f"Baixando dados da OCDE: {url}")

# Pula 4 linhas de cabeçalho
df = pd.read_excel(url, sheet_name='PMR_Total_Eco', skiprows=4)

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO E LIMPEZA
# =============================================================================

print("Limpando dados...")
# Remove as últimas 13 linhas (rodapé/info adicional)
df = df.iloc[:-13]

# Remove as últimas 22 colunas (colunas indesejadas/vazias?)
# Nota: Lógica baseada em posição fixa, pode ser frágil se o layout mudar.
df = df[df.columns[:-22]]

# Renomeia colunas para português
df.columns = ['NM_LOCAL'	,'DT_DADO'	,'VL_INDICADOR_PMR',
              'VL_INTERF_ESTADO'	,'VL_BARREIRAS_ENTRADA',
              'VL_PROPRIEDADE_PUBLICA',	'VL_ENVOLVIMENTO_NEGOCIOS',
              'VL_SIMPLIFICACAO_REGULACOES'	,'VL_STARTUPS'	,'VL_BARREIRAS_SERVICOS_E_REDE',
              'VL_BARREIRA_INVESTIMENTO',	'VL_ESCOPO',	'VL_ENVOLV_GOV_REDE',	'VL_CONTROLE_DIRETO',
              'VL_GOVERNANCA',	'VL_CONTROLE_PRECO',	'VL_COMANDO_CONTROLE_REGULACAO',
              'VL_APROVISIONAMENTO_PUBLICO'	,'VL_AVALIACAO_IMPACTO_COMPETICAO',	'VL_INTERACAO',
              'VL_COMPLEXIDADE_PROCEDIMENTOS'	,'VL_REQUISITOS'	,'VL_LICENCAS',	'VL_BARREIRAS_SERVICOS',
              'VL_BARREIRAS_SETORES_REDE',	'VL_BARREIRAS_FDI','VL_BARREIRAS_TARIFAS',
              'VL_TRATAMENTO_FORNECEDORES',	'VL_BARREIRAS_FACILITACAO']

# Filtra linhas que não são países (remove agregados por estado dos EUA e países não-OCDE se necessário)
df = df[df.NM_LOCAL != 'By US States:']
df = df[df.NM_LOCAL != 'Non-OECD countries']

# =============================================================================
# PASSO 3: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)
df.to_sql('OCDE_INDICADOR_PMR', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")
