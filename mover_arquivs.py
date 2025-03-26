import os
import shutil
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def move_to_public_desktop(file_path):
    try:
        public_desktop = r"C:\Users\Public\Desktop"
        destination_path = os.path.join(public_desktop, os.path.basename(file_path))
        
        if os.path.exists(destination_path):
            logging.info(f"O arquivo já existe na área de trabalho pública: {file_path}")
        else:
            shutil.copy(file_path, destination_path)
            logging.info(f"Arquivo copiado para a área de trabalho pública: {file_path}")
    except Exception as e:
        logging.error(f"Erro ao copiar {file_path}: {e}")
