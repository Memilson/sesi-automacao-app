import subprocess
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def renomear_computador():
    patrimonio = input("Digite o número do patrimônio: ").strip()
    if not patrimonio.isdigit():
        logging.error("Número de patrimônio inválido!")
        return
    
    novo_nome = f"SSPLAN-N{patrimonio}"
    comando = f'PowerShell Rename-Computer -NewName "{novo_nome}" -Force -Restart'

    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            logging.info(f"Nome do computador alterado para: {novo_nome}. Reiniciando para aplicar mudanças.")
        else:
            logging.error(f"Erro ao renomear: {resultado.stderr}")
    except Exception as e:
        logging.error(f"Erro: {e}")
