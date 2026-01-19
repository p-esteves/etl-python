import pandas as pd
import numpy as np
from functions.db import db_connect
import eurostat

"""
SCRIPT: Tarifas de Energia e Gás (Eurostat)
DESCRIÇÃO: Busca dados de tarifas de gás (nrg_pc_203) e eletricidade (nrg_pc_205) do Eurostat.
           Realiza transformação (melt) e carrega no banco.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO (EUROSTAT)
# =============================================================================
print("Extraindo dados do Eurostat...")

# nrg_pc_203: Preços de gás para consumidores domésticos
print("Baixando dados de Gás (nrg_pc_203)...")
gas = eurostat.get_data_df('nrg_pc_203', flags=False)

# nrg_pc_205: Preços de eletricidade para consumidores domésticos
print("Baixando dados de Eletricidade (nrg_pc_205)...")
ele = eurostat.get_data_df('nrg_pc_205', flags=False)

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO - GÁS
# =============================================================================
print("Processando dados de Gás...")

# Renomeia coluna de tempo/geo que vem com nome variável/complexo
gas.rename(columns={ gas.columns[5]: "geotime" }, inplace = True)

# Transforma colunas de tempo em linhas (Melt)
# id_vars: colunas identificadoras
# value_vars: (implícito) todas as outras colunas (datas)
gas = pd.melt(gas,id_vars=['product','consom','unit','tax', 'currency','geotime'], var_name='Semestre', value_name='Valor').sort_values('product')

# Renomeia colunas para o banco
gas.columns = ['NM_PRODUTO','NM_CONSOM','NM_UNIDADE','NM_TAXA','NM_MOEDA','NM_GEO','NM_SEMESTRE','VALOR_DADO']

gas.reset_index(drop=True,inplace=True)

# =============================================================================
# PASSO 3: TRANSFORMAÇÃO - ELETRICIDADE
# =============================================================================
print("Processando dados de Eletricidade...")

# Mesma lógica do Gás
ele.rename(columns={ele.columns[5]: "geotime" }, inplace = True)

ele = pd.melt(ele,id_vars=['product','consom','unit','tax', 'currency','geotime'], var_name='Semestre', value_name='Valor').sort_values('product')

ele.columns = ['NM_PRODUTO','NM_CONSOM','NM_UNIDADE','NM_TAXA','NM_MOEDA','NM_GEO','NM_SEMESTRE','VALOR_DADO']

ele.reset_index(drop=True,inplace=True)

# =============================================================================
# PASSO 4: CARGA NO BANCO
# =============================================================================
print("Carregando no banco...")
con = db_connect(package = 'sqlalchemy')

# Carga Tabela Gás
cols_gas = list(gas.columns)
gas.to_sql('TARIFA_MEDIA_OCDE_GAS', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols_gas) + 1)), method = 'multi')

# Carga Tabela Eletricidade
cols_ele = list(ele.columns)
ele.to_sql('TARIFA_MEDIA_OCDE_ENERGIA', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols_ele) + 1)), method = 'multi')

try:
    con.close()
except:
    pass
print("Concluído.")

