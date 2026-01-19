import pandas as pd
import requests
from functions.db import db_connect

"""
SCRIPT: Trânsito (Inrix)
DESCRIÇÃO: Busca dados JSON de tráfego/trânsito do Inrix.
           NOTA: O script está incompleto (não realiza carga no banco).
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO
# =============================================================================
um = "https://inrix.com/wp-content/themes/inrix/assets/data/data.json"
print("Acessando API Inrix...")

response = requests.get(um)
data = response.json()

# Normaliza JSON para DataFrame
transito = pd.json_normalize(data['cities'])

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO
# =============================================================================

# Renomeia colunas
transito.columns = ['VL_IMPACTO_RANKING_2020', 'VL_IMPACTO_RANKING_2020', 'VL_RANKING_PAIS_2020',
       'VL_RANKING_PAIS_2019', 'VL_RANKING_HRS_2020', 'COD_PAIS', 'NM_PAIS',
       'NM_AREA_URBANA', 'NM_CONTINENTE', 'VL_DELAY_2020', 'VL_HORAS_SALVAS', 'VL_MUDANÇA_DELAY',
       'VL_CUSTO_POR_MOTORISTA', 'VL_PICO_2018', 'VL_PICO_2019', 'VL_PICO_2020', 'VL_O_PICO_2018',
       'VL_O_PICO_2019', 'VL_0_PICO_2020', 'VL_ULTIMA_MILHA_2018', 'VL_ULTIMA_MILHA_2019',
       'VL_ULTIMA_MILHA_2020', 'VL_CPD_2019', 'VL_POUPADO', 'VL_COLISOES', 'VL_DVMT', 'VL_BICICLETA',
       'VL_TRANSITO']


#transito.to_excel("transito.xlsx")

# Nota: O código termina aqui sem carregar no banco.
# Se necessário inserir, utilize o padrão:
# con = db_connect(package='sqlalchemy')
# transito.to_sql('NOME_TABELA', con, if_exists='replace', index=False)
# con.close()





