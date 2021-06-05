import pandas as pd
import numpy as np
from functions.db import db_connect
import eurostat

gas = eurostat.get_data_df('nrg_pc_203', flags=False)
ele = eurostat.get_data_df('nrg_pc_205', flags=False)

#possivel usar for?

gas.rename(columns={ gas.columns[5]: "geotime" }, inplace = True)
#melts
gas = pd.melt(gas,id_vars=['product','consom','unit','tax', 'currency','geotime'], var_name='Semestre', value_name='Valor').sort_values('product')
gas.columns = ['NM_PRODUTO','NM_CONSOM','NM_UNIDADE','NM_TAXA','NM_MOEDA','NM_GEO','NM_SEMESTRE','VALOR_DADO']
#dividir nm semestre por semestre e ano?
#nao sei oq e consom nem geotime
gas.reset_index(drop=True,inplace=True)


ele.rename(columns={ele.columns[5]: "geotime" }, inplace = True)
#melts
ele = pd.melt(ele,id_vars=['product','consom','unit','tax', 'currency','geotime'], var_name='Semestre', value_name='Valor').sort_values('product')
ele.columns = ['NM_PRODUTO','NM_CONSOM','NM_UNIDADE','NM_TAXA','NM_MOEDA','NM_GEO','NM_SEMESTRE','VALOR_DADO']
#dividir nm semestre por semestre e ano?
#nao sei oq e consom nem geotime 
ele.reset_index(drop=True,inplace=True)

#conversoes


#inserir
con = db_connect(package = 'sqlalchemy')

cols = list(gas.columns)
gas.to_sql('TARIFA_MEDIA_OCDE_GAS', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

cols = list(ele.columns)
ele.to_sql('TARIFA_MEDIA_OCDE_ENERGIA', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

con.close()

