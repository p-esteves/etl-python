import pandas as pd
from functions.db import db_connect

df = pd.read_excel("Base de Dados JT.xlsx")

df.columns = ['NM_VARIVEL','NM_CLASSE','NM_FASE','NM_ATIVIDADE','NM_ASSUNTO','NM_SOLUCAO','NM_FONTE','NM_CATEGORIA','ANO','VL_MES','NM_INSTANCIA','NM_REGIAO_JUDICIARIA','NM_REGIAO','NM_VARA','NM_JURISDICAO','VL_QUANTIDADE']

con = db_connect(package = 'sqlalchemy')

cols = list(df.columns)

df.to_sql('INDICADORES_TST', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

con.close()