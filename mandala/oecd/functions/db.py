import sqlalchemy
import pyodbc
import json

def db_connect(db_name = "DDTM_OBSERVATORIO_2" , credentials_file_path = "parameters/credentials.json", package = 'pyodbc'):

    credentials_file = open(credentials_file_path, 'r').read()
    credentials_file = json.loads(credentials_file)

    if package == 'pyodbc':

        con = pyodbc.connect('Driver={0};Server={1};Database={2};UID={3};PWD={4}'.format(
            credentials_file['driver'],
            credentials_file['server'],
            db_name,
            credentials_file['username'],
            credentials_file['password']))
    
    else:

        con = sqlalchemy.create_engine('mssql+pyodbc://{0}:{1}@{2}/{3}?driver={4}'.format(
            credentials_file['username'],
            credentials_file['password'], 
            credentials_file['server'],
            db_name,
            credentials_file['driver'].replace('{', '').replace('}','')), fast_executemany=True)

        con = con.connect()

    return con

if __name__ == '__main__':

    con = db_connect(db_name = "DDTM_OBSERVATORIO_2" , 
                     credentials_file_path = "parameters/credentials.json", 
                     package = 'sqlalchemy')


