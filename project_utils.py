import mysql.connector
import config 

def create_connection():
    connection = mysql.connector.connect(
        host = config.HOST,
        port = config.PORT,
        user = config.USER,
        password = config.PASSWORD,
        auth_plugin = config.AUTH_PLUGIN,
        database = config.DATABASE
    )
    return connection

def check_table(connection, table):
    cursor = connection.cursor()
    query = f"SELECT * FROM {table}"
    try:
        _ = cursor.execute(query)
        return True 
    except:
        return False 