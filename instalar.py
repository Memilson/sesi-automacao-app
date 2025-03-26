import os
import subprocess
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def install_program(path, silent=False):
    try:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"O arquivo não foi encontrado: {path}")

        install_args = [path, "/quiet", "/norestart"] if silent else [path]
        result = subprocess.run(install_args, check=True, capture_output=True, text=True)

        logging.info(f"Instalação concluída: {path}\nSaída: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao instalar {path}: {e.stderr}")
    except Exception as e:
        logging.error(f"Erro ao processar {path}: {e}")
