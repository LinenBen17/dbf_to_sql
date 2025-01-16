import time
import subprocess
import os

def execute_migration(flag_file):
    """Ejecuta el script migrate_dbf.py y controla la ejecución."""
    try:
        print("Ejecutando migrate_dbf.py...")
        # Crear archivo de marca para evitar colisiones
        with open(flag_file, 'w') as f:
            f.write("Proceso en curso")
        
        subprocess.run(["python", "migrate_dbf.py"], check=True)
        print("Migración ejecutada con éxito.")
    except Exception as e:
        print(f"Error al ejecutar migrate_dbf.py: {e}")
    finally:
        # Eliminar el archivo de marca después de la ejecución
        if os.path.exists(flag_file):
            os.remove(flag_file)

if __name__ == "__main__":
    # Archivo temporal para evitar ejecuciones simultáneas
    flag_file = "process_in_progress.flag"
    # Intervalo en segundos (5 minutos = 300 segundos)
    interval_seconds = 300

    print("Iniciando ejecución periódica cada 5 minutos...")
    try:
        while True:
            # Verificar si no hay otra migración en curso
            if not os.path.exists(flag_file):
                execute_migration(flag_file)
            else:
                print("Proceso en curso, esperando el siguiente intervalo...")
            
            # Esperar el intervalo antes de la siguiente ejecución
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("Ejecución interrumpida por el usuario.")
