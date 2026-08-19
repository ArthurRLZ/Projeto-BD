import mysql.connector
from mysql.connector import pooling
import os

# Configuração do Pool de Conexões para otimizar acessos ao banco de dados
try:
    dbconfig = {
        "host": "db",
        "user": "root",
        "password": "root",
        "database": "ufape_reserva_db",
        "port": 3306,
        "charset": "utf8mb4"
    }
    
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="ufape_pool",
        pool_size=10, # Mantém 10 conexões abertas
        pool_reset_session=True,
        **dbconfig
    )
    print("Pool de conexões criado com sucesso.")
except mysql.connector.Error as err:
    print(f"Erro ao criar o pool de conexões: {err}")
    connection_pool = None

from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Obtém uma conexão do pool de forma segura com auto-close."""
    conn = None
    try:
        if connection_pool:
            conn = connection_pool.get_connection()
            yield conn
        else:
            raise Exception("Pool de conexões não inicializado.")
    except mysql.connector.Error as err:
        print(f"Erro ao obter conexão do pool: {err}")
        raise err
    finally:
        if conn:
            conn.close()
