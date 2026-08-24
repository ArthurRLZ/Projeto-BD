import mysql.connector
from mysql.connector import pooling
import os
import time

# Configuração do Pool de Conexões para otimizar acessos ao banco de dados
dbconfig = {
    "host": "db",
    "user": "root",
    "password": "root",
    "database": "ufape_reserva_db",
    "port": 3306,
    "charset": "utf8mb4"
}

connection_pool = None


def _criar_pool(tentativas=5, espera_segundos=2):
    """Tenta criar o pool de conexões, com algumas tentativas de retry.
    Isso evita que uma falha temporária (ex: MySQL ainda inicializando)
    deixe o backend permanentemente sem conexão com o banco."""
    global connection_pool
    for tentativa in range(1, tentativas + 1):
        try:
            connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="ufape_pool",
                pool_size=10,  # Mantém 10 conexões abertas
                pool_reset_session=True,
                **dbconfig
            )
            print("Pool de conexões criado com sucesso.")
            return
        except mysql.connector.Error as err:
            print(f"[Tentativa {tentativa}/{tentativas}] Erro ao criar o pool de conexões: {err}")
            if tentativa < tentativas:
                time.sleep(espera_segundos)
    connection_pool = None
    print("Não foi possível criar o pool de conexões após todas as tentativas.")


# Tenta criar o pool assim que o módulo é carregado
_criar_pool()

from contextlib import contextmanager

@contextmanager
def get_db_connection():
    """Obtém uma conexão do pool de forma segura com auto-close.
    Se o pool ainda não existir (ex: falhou na inicialização), tenta recriá-lo
    antes de desistir."""
    global connection_pool
    conn = None
    try:
        if not connection_pool:
            _criar_pool(tentativas=1, espera_segundos=0)

        if connection_pool:
            conn = connection_pool.get_connection()
            yield conn
        else:
            raise Exception("Pool de conexões não inicializado. Verifique se o container do MySQL está de pé.")
    except mysql.connector.Error as err:
        print(f"Erro ao obter conexão do pool: {err}")
        raise err
    finally:
        if conn:
            conn.close()