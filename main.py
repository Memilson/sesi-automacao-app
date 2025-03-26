import logging
import subprocess
from renomearpc import renomear_computador
from instalar import install_program
from mover_arquivs import move_to_public_desktop
from alterar_registro import apply_policies, remove_policies

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def instalar_programas():
    programs = [
        (r"D:\InstaladorExamsSESI.exe", True),
        (r"D:\SIASetup.exe", True),
        (r"D:\SEB_3.9.0.787_SetupBundle.exe", False),
        (r"D:\Instalador_Absolute\AbsoluteFullAgent.msi", True),
        (r"D:\LibreOffice_24.8.4_Win_x86-64.msi", True)
    ]
    for program, silent in programs:
        logging.info(f"Instalando: {program} (Modo silencioso: {silent})")
        install_program(program, silent)

def copiar_arquivos():
    files_to_move_and_install = [
        r"D:\TOEIC Secure Browser.exe",
        r"D:\Inicia Provas.exe"
    ]
    for file_path in files_to_move_and_install:
        logging.info(f"Copiando: {file_path} para a Área de Trabalho Pública")
        move_to_public_desktop(file_path)

def aplicar_ou_remover_politicas():
    """Pergunta ao usuário se quer aplicar ou remover políticas e executa a ação escolhida."""
    action = input("Digite 'apply' para aplicar políticas ou 'remove' para removê-las: ").strip().lower()
    actions = {
        "apply": apply_policies,
        "remove": remove_policies
    }

    if action in actions:
        actions[action]()
    else:
        logging.error("🚨 Opção inválida! Usando 'apply' por padrão.")
        apply_policies()

def reiniciar_computador():
    logging.info("Reiniciando o computador em 5 segundos...")
    try:
        subprocess.run("shutdown /r /t 5", shell=True, check=True)
    except Exception as e:
        logging.error(f"Erro ao tentar reiniciar: {e}")

def main():
    logging.info("Iniciando configuração do sistema...")
    aplicar_ou_remover_politicas()
    renomear_computador()
    instalar_programas()
    copiar_arquivos()
    logging.info("Configuração finalizada com sucesso!")
    reiniciar_computador()

if __name__ == "__main__":
    main()
