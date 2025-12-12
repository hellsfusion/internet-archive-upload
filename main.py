import logging
import os
from pathlib import Path
import internetarchive
from dotenv import load_dotenv
import re

load_dotenv()

def simple_upload():
    # Configuración
    access_key = os.getenv("access-key")
    secret_key = os.getenv("secret-key")
    upload_dir = Path(__file__).parent / "upload"
    identifier = input("Ingrese el identificador para la subida: ").strip()
    # remplazar espacios por guiones y eliminar caracteres no alfanuméricos
    identifier = re.sub(r'\s+', '-', identifier)
    identifier = re.sub(r'[^a-zA-Z0-9\-]', '', identifier)
    # concatenar 6 digitos aleatorios al final del identificador
    identifier += '-' + os.getenv("username-username")

    # crear carpeta si no existe
    if not upload_dir.exists():
        upload_dir.mkdir(parents=True)
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Cambiar al directorio de uploads
    os.chdir(upload_dir)
    logging.info(f"Trabajando en directorio: {os.getcwd()}")
    
    # Obtener lista de archivos
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    logging.info(f"Encontrados {len(files)} archivos")
    
    successful = 0
    failed = 0
    
    for filename in files:
        try:
            logging.info(f"------------------------------------------------------")
            logging.info(f"Subiendo: {filename}")
            
            # Subir archivo individual
            internetarchive.upload(
                identifier,
                files=[filename],
                access_key=access_key,
                secret_key=secret_key,
                verbose=True
            )
            
            successful += 1
            logging.info(f"✓ {filename} - OK")
            # esperar 3 segundos entre subidas
            import time
            time.sleep(3)
            logging.info(f"------------------------------------------------------")
            # eliminar archivo local despues de subir
            os.remove(filename)

            
        except Exception as e:
            failed += 1
            logging.error(f"✗ {filename} - ERROR: {str(e)}")
            continue
    
    logging.info(f"RESUMEN: {successful} exitosos, {failed} fallidos")

if __name__ == "__main__":
    simple_upload()