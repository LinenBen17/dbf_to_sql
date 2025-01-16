import time
from db_utils import connect_to_mysql, execute_query, commit_and_close
from datetime import datetime

def log_message(message):
    """Escribe un mensaje en el archivo log.txt con marca de tiempo."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

def modify_table_structure(cursor):
    """Modificar la estructura de la tabla `envios`."""
    alter_query = "ALTER TABLE envios CHANGE factura no_guia DECIMAL(11, 0);"
    execute_query(cursor, alter_query)

def update_cargacamiones_records(cursor):
    """Actualizar los registros de `cargacamiones`."""
    update_query = """
        UPDATE cargacamiones
        SET guiamadre = REPLACE(guiamadre, 'GU0', '')
        WHERE guiamadre LIKE 'GU0%';
    """
    execute_query(cursor, update_query)

def update_descargacamiones_records(cursor):
    """Actualizar los registros de `descargacamiones`."""
    update_query = """
        UPDATE descargacamiones
        SET escaneo = REPLACE(escaneo, 'GU0', '')
        WHERE escaneo LIKE 'GU0%';
    """
    execute_query(cursor, update_query)

def modify_tables(mysql_config):
    print("==============edit_table==============\n")
    start_time = time.time()
    conn = connect_to_mysql(**mysql_config)
    cursor = conn.cursor()

    # Aplicar modificaciones
    modify_table_structure(cursor)
    update_cargacamiones_records(cursor)
    update_descargacamiones_records(cursor)

    # Confirmar y cerrar conexión
    commit_and_close(conn)
    elapsed_time = time.time() - start_time
    log_message(f"Modificaciones completadas en {elapsed_time:.2f} segundos.")
    print(f"Modificaciones completadas en {elapsed_time:.2f} segundos.")

if __name__ == "__main__":
    # Configuración MySQL
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'laravel11crud'
    }

    modify_tables(mysql_config)
