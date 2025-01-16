from mysql.connector import connect

def connect_to_mysql(host, user, password, database):
    """Conectar a la base de datos MySQL."""
    return connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

def execute_query(cursor, query, data=None):
    """Ejecutar una consulta SQL con o sin datos."""
    cursor.execute(query, data) if data else cursor.execute(query)

def commit_and_close(conn):
    """Confirmar cambios y cerrar la conexión."""
    conn.commit()
    conn.close()
