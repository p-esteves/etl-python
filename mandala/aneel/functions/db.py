import sqlalchemy
import pyodbc
import os

def db_connect(db_name="DDTM_OBSERVATORIO_2", package='pyodbc'):
    """
    Estabelece conexao com o banco de dados usando variaveis de ambiente.
    Remove a dependencia de arquivo local 'credentials.json' para seguranca.
    """
    server = os.getenv('DB_SERVER')
    database = db_name
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    driver = os.getenv('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')

    if not all([server, username, password]):
        # Se nao houver credenciais, gera um aviso ou erro, mas nao falha silenciosamente
        print("AVISO: Variaveis de ambiente de banco de dados nao definidas (DB_SERVER, DB_USERNAME, DB_PASSWORD).")
        # raise ValueError("Credenciais ausentes") # Descomentar se quiser forcar o erro

    if package == 'pyodbc':
        connection_string = 'Driver={0};Server={1};Database={2};UID={3};PWD={4}'.format(
            driver, server, database, username, password)
        try:
            con = pyodbc.connect(connection_string)
        except Exception as e:
            print(f"Erro conexao pyodbc: {e}")
            raise e
    
    else:
        # SQLAlchemy connection logic
        # Ajuste para garantir formato correto da URL de conexao
        driver_clean = driver.replace('{', '').replace('}', '')
        connection_url = sqlalchemy.engine.URL.create(
            "mssql+pyodbc",
            username=username,
            password=password,
            host=server,
            database=database,
            query={"driver": driver_clean}
        )
        try:
            con = sqlalchemy.create_engine(connection_url, fast_executemany=True)
            # Testa a conexao
            # con = con.connect() # Nao conectar imediatamente para permitir criar a engine apenas
        except Exception as e:
             print(f"Erro criacao engine sqlalchemy: {e}")
             raise e

    return con

if __name__ == '__main__':
    try:
        con = db_connect(package='sqlalchemy')
        # Tenta conectar
        with con.connect() as connection:
             print("Conexao bem sucedida!")
    except Exception as e:
        print(f"Erro ao conectar: {e}")
