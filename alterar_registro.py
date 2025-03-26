import winreg
import os
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def set_registry_value(hive, key_path, name, value):
    try:
        with winreg.CreateKey(hive, key_path) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
            logging.info(f"Configuração aplicada: {key_path} -> {name} = {value}")
    except Exception as e:
        logging.error(f"Erro ao definir {name}: {e}")
policies = {
    "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\ActiveDesktop": {
        "NoChangingWallPaper": 1
    },
    "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer": {
        "NoDriveTypeAutoRun": 0x91,
        "NoThemesTab": 1,
        "NoControlPanel": 1
    },
    "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System": {
        "NoColorChoice": 1,
        "NoVisualStyleChoice": 1,
        "NoSizeChoice": 1,
        "NoDispAppearancePage": 1,
        "NoDispBackgroundPage": 1,
        "NoDispScrSavPage": 1
    }
}
def apply_policies():
    """Aplica as políticas para todos os usuários."""
    for key, values in policies.items():
        for name, value in values.items():
            set_registry_value(winreg.HKEY_LOCAL_MACHINE, key, name, value)
    for user_sid in os.listdir(r'C:\Users'):
        user_profile = os.path.join(r'HKEY_USERS', user_sid)
        for key, values in policies.items():
            for name, value in values.items():
                set_registry_value(winreg.HKEY_USERS, key, name, value)
    logging.info("✅ Políticas aplicadas a todos os usuários!")
def remove_policies():
    """Remove as políticas (definindo os valores como 0)."""
    for key, values in policies.items():
        for name in values.keys():
            set_registry_value(winreg.HKEY_LOCAL_MACHINE, key, name, 0)
    for user_sid in os.listdir(r'C:\Users'):
        user_profile = os.path.join(r'HKEY_USERS', user_sid)
        for key, values in policies.items():
            for name in values.keys():
                set_registry_value(winreg.HKEY_USERS, key, name, 0)
    logging.info("❌ Políticas desativadas para todos os usuários!")
