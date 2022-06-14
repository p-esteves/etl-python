import pandas as pd
import numpy as np
from functions.db import db_connect

df = pd.read_excel("https://www.oecd.org/economy/reform/OECD-PMR-Economy%20-Wide%20Indicator%20values-2018.xlsx",sheet_name='PMR_Total_Eco',skiprows=4)

df = df.iloc[:-13]

df = df[df.columns[:-22]]

#df.to_excel("teste.xlsx")  
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

df = df[df.NM_LOCAL != 'By US States:']
df = df[df.NM_LOCAL != 'Non-OECD countries']

#remover pequena letra da legenda. (?)


#inserir
con = db_connect(package = 'sqlalchemy')
cols = list(df.columns)
df.to_sql('OCDE_INDICADOR_PMR', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')
con.close()
