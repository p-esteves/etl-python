import pandas as pd
import requests
from functions.db import db_connect

um = "https://inrix.com/wp-content/themes/inrix/assets/data/data.json"
#response
response = requests.get(um)
#'dicionario'
data = response.json()
#dataframe
transito = pd.json_normalize(data['cities'])

transito.columns = ['VL_IMPACTO_RANKING_2020', 'VL_IMPACTO_RANKING_2020', 'VL_RANKING_PAIS_2020',
       'VL_RANKING_PAIS_2019', 'VL_RANKING_HRS_2020', 'COD_PAIS', 'NM_PAIS',
       'NM_AREA_URBANA', 'NM_CONTINENTE', 'VL_DELAY_2020', 'VL_HORAS_SALVAS', 'VL_MUDANÇA_DELAY',
       'VL_CUSTO_POR_MOTORISTA', 'VL_PICO_2018', 'VL_PICO_2019', 'VL_PICO_2020', 'VL_O_PICO_2018',
       'VL_O_PICO_2019', 'VL_0_PICO_2020', 'VL_ULTIMA_MILHA_2018', 'VL_ULTIMA_MILHA_2019',
       'VL_ULTIMA_MILHA_2020', 'VL_CPD_2019', 'VL_POUPADO', 'VL_COLISOES', 'VL_DVMT', 'VL_BICICLETA',
       'VL_TRANSITO']


#transito.to_excel("transito.xlsx")





