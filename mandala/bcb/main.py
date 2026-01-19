import pandas as pd
import numpy as np
import sgs
from functions.db import db_connect
from datetime import date

"""
SCRIPT: BCB - Séries Temporais (SGS)
DESCRIÇÃO: Busca séries temporais do Sistema Gerenciador de Séries Temporais do Banco Central.
           - Série 20540: Média anual do saldo da carteira de crédito - PJ
           - Série 20784: Spread médio das operações de crédito - PJ
"""

# =============================================================================
# PASSO 1: CONFIGURAÇÃO E EXTRAÇÃO
# =============================================================================
# Define data final como a data de hoje
hj = date.today()
 
print("Consultando séries do SGS/BCB...")

# Extração 1: Média anual do saldo da carteira de crédito - PJ
# Código SGS: 20540
# Início: 01/03/2007
df1 = sgs.time_serie(20540,start="1/3/2007",end=hj)
# Transforma o índice (datas) em coluna e renomeia
df1 = pd.DataFrame({'DT_DADO':df1.index, 'VL_DADO':df1.values})

# Extração 2: Spread médio das operações de crédito - PJ
# Código SGS: 20784
# Início: 01/03/2011
df2 = sgs.time_serie(20784,start="1/3/2011",end=hj)
df2= pd.DataFrame({'DT_DADO':df2.index, 'VL_DADO':df2.values})

# =============================================================================
# PASSO 3: CARGA NO BANCO DE DADOS
# =============================================================================

print("Carregando no banco...")
con = db_connect(package = 'sqlalchemy')

# Carga Tabela 1: BANCO_CENTRAL_MEDIA_SALDO_CREDITO
cols1 = list(df1.columns)
df1.to_sql('BANCO_CENTRAL_MEDIA_SALDO_CREDITO', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols1) + 1)), method = 'multi')

# Carga Tabela 2: BANCO_CENTRAL_SPREAD_OPERACAO_CREDITO
cols2 = list(df2.columns)
df2.to_sql('BANCO_CENTRAL_SPREAD_OPERACAO_CREDITO', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols2) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")

 