import time
from dbfread import DBF
from db_utils import connect_to_mysql, execute_query, commit_and_close
import subprocess  # Para ejecutar otro script
from datetime import datetime  # Para agregar marcas de tiempo

def log_message(message):
    """Escribe un mensaje en el archivo log.txt con marca de tiempo."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

def create_table_from_dbf(cursor, table_name, dbf_file):
    """Crear una tabla en MySQL basada en un archivo DBF."""
    drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
    execute_query(cursor, drop_table_query)

    columns = [field.name.lower() + " VARCHAR(255)" for field in dbf_file.fields]
    create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)});"
    execute_query(cursor, create_table_query)

def insert_records_from_dbf(cursor, table_name, dbf_file, batch_size=1000):
    """Insertar registros desde un archivo DBF a MySQL en lotes."""
    records = []
    for record in dbf_file:
        records.append(tuple(record.values()))
        if len(records) >= batch_size:
            placeholders = ', '.join(['%s'] * len(records[0]))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            cursor.executemany(insert_query, records)
            records = []
    # Insertar los registros restantes
    if records:
        placeholders = ', '.join(['%s'] * len(records[0]))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.executemany(insert_query, records)

def migrate_dbf_to_mysql(dbf_files, mysql_config):
    """Migrar múltiples archivos DBF a MySQL de manera optimizada."""
    conn = connect_to_mysql(**mysql_config)
    cursor = conn.cursor()
    conn.start_transaction()  # Iniciar transacción

    try:
        for table_name, dbf_path in dbf_files.items():
            print(f"Migrando {table_name} desde {dbf_path}...")
            start_time = time.time()
            dbf_file = DBF(dbf_path, encoding='latin1')
            create_table_from_dbf(cursor, table_name, dbf_file)
            insert_records_from_dbf(cursor, table_name, dbf_file, batch_size=1000)
            elapsed_time = time.time() - start_time
            log_message(f"Datos de {table_name} migrados exitosamente en {elapsed_time:.2f} segundos.")
            print(f"Datos de {table_name} migrados exitosamente en {elapsed_time:.2f} segundos.\n")
        
        conn.commit()  # Confirmar cambios
    except Exception as e:
        conn.rollback()  # Revertir en caso de error
        log_message(f"Error durante la migración: {e}")
        print(f"Error durante la migración: {e}")
    finally:
        commit_and_close(conn)

if __name__ == "__main__":
    # Configuración MySQL
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'laravel11crud'
    }

    # Archivos DBF a migrar
    dbf_files = {
        'envios': 'envios.dbf',
        'cargacamiones': 'cargacamiones.dbf',
        'descargacamiones': 'descargacamiones.dbf',
        'central': 'CENTRAL.dbf'
    }

    # Ejecutar la migración
    try:
        print("==============migrate_dbf==============\n")
        migrate_dbf_to_mysql(dbf_files, mysql_config)
        log_message("Migración completada con éxito.")
        print("Migración completada con éxito.\n")
        
        # Ejecutar el script edit_table.py
        print("Ejecutando modificaciones en las tablas...")
        start_time = time.time()
        subprocess.run(["python", "edit_table.py"], check=True)
        elapsed_time = time.time() - start_time
        log_message(f"Modificaciones completadas con éxito en {elapsed_time:.2f} segundos.")
        print(f"Modificaciones completadas con éxito en {elapsed_time:.2f} segundos.\n")
    except Exception as e:
        log_message(f"Error durante la migración o modificaciones: {e}")
        print(f"Error durante la migración o modificaciones: {e}")
