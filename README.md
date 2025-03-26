# sesi-automacao-app
# **Documentação Técnica do Sistema de Configuração de Máquinas**

Este documento descreve o sistema de automação para configuração de máquinas Windows, utilizado para padronizar instalações em ambientes corporativos ou educacionais. O sistema é composto por módulos Python que realizam:

1. **Aplicação/remoção de políticas de registro**  
2. **Instalação silenciosa de programas**  
3. **Cópia de arquivos para a Área de Trabalho Pública**  
4. **Renomeação de computadores**  

---

## **1. Estrutura do Projeto**
### **Arquivos Principais**
| Arquivo               | Função                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| `main.py`             | Orquestra a execução de todos os módulos                              |
| `alterar_registro.py` | Gerencia políticas do Windows via Registry (HKLM e HKEY_USERS)        |
| `instalar.py`         | Instala programas em modo silencioso (MSI/EXE)                        |
| `mover_arquivs.py`    | Copia arquivos para `C:\Users\Public\Desktop`                         |
| `renomearpc.py`       | Renomeia o computador com base em um patrimônio (ex: `SSPLAN-N123456`) |

---

## **2. Módulos Detalhados**
### **2.1. `alterar_registro.py`**
#### **Funções**
- **`set_registry_value(hive, key_path, name, value)`**  
  Define um valor no registro do Windows.  
  **Parâmetros**:  
  - `hive`: HKEY (ex: `winreg.HKEY_LOCAL_MACHINE`)  
  - `key_path`: Caminho da chave (ex: `Software\Microsoft\Windows\CurrentVersion\Policies`)  
  - `name`: Nome do valor a ser modificado (ex: `NoControlPanel`)  
  - `value`: Valor DWORD (ex: `1` para ativar, `0` para desativar).  

- **`apply_policies()`**  
  Aplica todas as políticas definidas no dicionário `policies` para **HKLM** e **HKEY_USERS**.  

- **`remove_policies()`**  
  Remove as políticas (define valores como `0`).  

#### **Políticas Implementadas**
| Caminho do Registro                                                                 | Política                     | Efeito                                                                 |
|-------------------------------------------------------------------------------------|-----------------------------|-------------------------------------------------------------------------|
| `Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop`                  | `NoChangingWallPaper`       | Bloqueia alteração do papel de parede.                                 |
| `Software\Microsoft\Windows\CurrentVersion\Policies\Explorer`                       | `NoControlPanel`            | Desativa o Painel de Controle.                                         |
| `Software\Microsoft\Windows\CurrentVersion\Policies\System`                         | `NoDispBackgroundPage`      | Oculta a opção de personalização do plano de fundo.                    |

---

### **2.2. `instalar.py`**
#### **Função Principal**
- **`install_program(path, silent=False)`**  
  Instala programas em modo silencioso (suporta `.msi` e `.exe`).  

  **Comportamento**:  
  - Se `silent=True`, usa flags como `/quiet` (EXE) ou `/qn` (MSI).  
  - Verifica se o arquivo existe e se o script está sendo executado como administrador.  

  **Exemplo de Uso**:  
  ```python
  install_program(r"D:\LibreOffice.msi", silent=True)  # Instalação silenciosa
  ```

#### **Tratamento de Erros**
- **`FileNotFoundError`**: Se o instalador não existir.  
- **`CalledProcessError`**: Se a instalação falhar (ex: código de saída ≠ 0).  

---

### **2.3. `mover_arquivs.py`**
#### **Função Principal**
- **`move_to_public_desktop(file_path)`**  
  Copia um arquivo para `C:\Users\Public\Desktop` (acessível a todos os usuários).  

  **Fluxo**:  
  1. Verifica se o arquivo de origem existe.  
  2. Se o arquivo já existir no destino, ignora.  
  3. Usa `shutil.copy` para evitar problemas de permissão.  

  **Exemplo**:  
  ```python
  move_to_public_desktop(r"D:\TOEIC Secure Browser.exe")
  ```

---

### **2.4. `renomearpc.py`**
#### **Função Principal**
- **`renomear_computador()`**  
  Renomeia o computador para `SSPLAN-N<Patrimônio>` e reinicia a máquina.  

  **Fluxo**:  
  1. Solicita um número de patrimônio (6 dígitos).  
  2. Executa o comando PowerShell:  
     ```powershell
     Rename-Computer -NewName "SSPLAN-N123456" -Force -Restart
     ```  
  3. Reinicia o sistema após 5 segundos.  

  **Validações**:  
  - Verifica se o patrimônio tem 6 dígitos.  
  - Exige execução como administrador.  

---

### **2.5. `main.py`**
#### **Fluxo Principal**
1. **Aplica políticas de registro** (`apply_policies()`).  
2. **Renomeia o computador** (aciona reinício automático).  
3. **Instala programas** (em modo silencioso, quando possível).  
4. **Copia arquivos** para a Área de Trabalho Pública.  

#### **Funções Auxiliares**
| Função                        | Descrição                                                                 |
|-------------------------------|---------------------------------------------------------------------------|
| `aplicar_ou_remover_politicas()` | Pergunta ao usuário se deseja aplicar ou remover políticas.               |
| `reiniciar_computador()`        | Força um reinício após 5 segundos (`shutdown /r /t 5`).                   |

---

## **3. Requisitos e Considerações**
### **3.1. Pré-requisitos**
- **Sistema Operacional**: Windows 10/11.  
- **Python**: 3.8+ (testado em 3.11).  
- **Permissões**: Administrador local.  

### **3.2. Estrutura de Diretórios Recomendada**
```
D:\
├── InstaladorExamsSESI.exe
├── SIASetup.exe
├── SEB_3.9.0.787_SetupBundle.exe
├── Instalador_Absolute\
│   └── AbsoluteFullAgent.msi
├── TOEIC Secure Browser.exe
└── Inicia Provas.exe
```

### **3.3. Logs**
- Todos os módulos usam `logging` para registrar ações em tempo real.  
- Formato:  
  ```log
  2024-01-01 12:00:00 - INFO - Instalação concluída: D:\LibreOffice.msi
  ```

---

## **4. Melhorias Futuras**
1. **Adicionar rollback** em caso de falha na instalação.  
2. **Suporte a mais instaladores** (Chocolatey, Winget).  
3. **Configuração via JSON/YAML** para facilitar a manutenção.  

---

## **5. Exemplo de Uso**
```powershell
# Executar como administrador
python main.py
```
**Saída Esperada**:
```log
2024-01-01 12:00:00 - INFO - Iniciando configuração...
2024-01-01 12:00:01 - INFO - Políticas aplicadas!
2024-01-01 12:00:02 - INFO - Computador renomeado para SSPLAN-N123456. Reiniciando...
```

---
