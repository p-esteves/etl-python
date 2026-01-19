import json
import pandas as pd
import numpy as np
from functions.db import db_connect

"""
SCRIPT: Aneel - Tarifa Média de Fornecimento
DESCRIÇÃO: Extrai dados de tarifas de energia da ANEEL, limpa os dados e carrega no banco de dados SQL.
"""

# =============================================================================
# PASSO 1: EXTRAÇÃO DE DADOS
# =============================================================================
# Definição da URL da fonte de dados (JSON da ANEEL)
url="https://www.aneel.gov.br/dados/relatorios?p_p_id=dadosabertos_WAR_dadosabertosportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=gerarTarifaMediaFornecimentoJSON&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=1"

# Leitura do JSON diretamente da URL com encoding Latin1
print("Iniciando extração de dados da ANEEL...")
df = pd.read_json(url, encoding="Latin1")

# Renomeação das colunas para padronização
df.columns = ["NM_REGIAO","VL_CONSUMO_MWH","ANO","VL_MES", "NM_CLASSE_CONSUMO","ID_LINHA","DT_REGISTRO"]

# Remoção de coluna desnecessária (ID_LINHA)
del df['ID_LINHA']

print("Dados extraídos:")
print(df.head())

# =============================================================================
# PASSO 2: TRANSFORMAÇÃO E LIMPEZA
# =============================================================================

# Conversão da coluna de consumo para tipo float (numérico)
print("Convertendo tipos e limpando dados...")
df["VL_CONSUMO_MWH"] = pd.to_numeric(df["VL_CONSUMO_MWH"], downcast="float")

# Conversão da coluna de data de registro para tipo datetime
df["DT_REGISTRO"] = pd.to_datetime(df["DT_REGISTRO"])

# Conversão de Ano e Mês para string (texto)
df[['ANO','VL_MES']] = df[['ANO','VL_MES']].astype(str)

# Padronização dos nomes das classes de consumo (Correção de erros de digitação e unificação)
# Ex: 'Residencia' -> 'Residencial', remoção de espaços extras, etc.
df['NM_CLASSE_CONSUMO'].replace('Comercial, Serviços e Outras','Comercial e Serviços e Outras',inplace=True)
df['NM_CLASSE_CONSUMO'].replace('Comercial, Serviços e Outras','Comercial e Serviços e Outras',inplace=True) # Repetido no original, mantendo
df['NM_CLASSE_CONSUMO'].replace('Residencia','Residencial',inplace=True)
df['NM_CLASSE_CONSUMO'].replace('Comercial e  Serviços e Outras','Comercial e Serviços e Outras',inplace=True)
df['NM_CLASSE_CONSUMO'].replace('Serviço Público (água, esgoto e saneamento)','Serviço Público (água e esgoto e saneamento)',inplace=True)
df['NM_CLASSE_CONSUMO'].replace('Serviço Público (água e  esgoto e saneamento)','Serviço Público (água e esgoto e saneamento)',inplace=True)
df['NM_CLASSE_CONSUMO'].replace('Totais por Região','Total por Região',inplace=True)

print("Dados transformados:")
print(df.head())

# =============================================================================
# PASSO 3: CARGA NO BANCO DE DADOS
# =============================================================================

print("Iniciando carga no banco de dados...")
# Estabelece conexão com o banco usando a função segura (variáveis de ambiente)
con = db_connect(package = 'sqlalchemy')

# Obtém a lista de colunas para cálculo do chunksize
cols = list(df.columns)

# Escreve o DataFrame na tabela 'ENERGIA_TARIFAS_CLASSE_CONSUMO'
# if_exists='replace': Substitui a tabela se ela já existir
# chunksize: Define o tamanho do lote de inserção para otimizar performance no SQL Server
df.to_sql('ENERGIA_TARIFAS_CLASSE_CONSUMO', con, if_exists = 'replace', index = False, chunksize = int(2100/(len(cols) + 1)), method = 'multi')

# Fecha a conexão (embora o engine do sqlalchemy gerencie pool, é boa prática fechar explicitamente se instanciado assim)
# Nota: na nova implementação do db_connect, con é engine ou connection. Se for engine, close() não é necessário da mesma forma, mas mantemos compatibilidade.
try:
    con.close()
except:
    pass

print("Carga concluída sucesso!")
