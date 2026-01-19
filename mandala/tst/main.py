import pandas as pd
from functions.db import db_connect

"""
SCRIPT: Indicadores TST (Tribunal Superior do Trabalho)
DESCRIÇÃO: Processa base de dados Excel do TST e carrega no banco.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO (LOCAL)
# =============================================================================
print("Lendo dados do TST...")
df = pd.read_excel("Base de Dados JT.xlsx")

# Renomeia colunas para o banco
df.columns = ['NM_VARIVEL','NM_CLASSE','NM_FASE','NM_ATIVIDADE','NM_ASSUNTO','NM_SOLUCAO','NM_FONTE','NM_CATEGORIA','ANO','VL_MES','NM_INSTANCIA','NM_REGIAO_JUDICIARIA','NM_REGIAO','NM_VARA','NM_JURISDICAO','VL_QUANTIDADE']

# =============================================================================
# PASSO 2: CARGA NO BANCO
# =============================================================================

print("Carga no banco...")
con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)

df.to_sql('INDICADORES_TST', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")