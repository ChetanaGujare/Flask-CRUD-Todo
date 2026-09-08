import mysql.connector
from mysql.connector import pooling
from config import Config

db_config = {
    'host': Config.DB_HOST,
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'database': Config.DB_NAME,
    'pool_name': Config.DB_POOL_NAME,
    'pool_size': Config.DB_POOL_SIZE,
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)

def get_db_connection():
    return connection_pool.get_connection()

def close_connection(conn, cursor=None):
    if cursor:
        cursor.close()
    if conn:
        conn.close()