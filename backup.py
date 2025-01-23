# backup.py
import os
import shutil
from datetime import datetime

def criar_backup(origem, destino):
    # Cria a pasta de destino se não existir
    if not os.path.exists(destino):
        os.makedirs(destino)
    
    # Nome da subpasta de backup com data e hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(destino, f"backup_{timestamp}")
    os.makedirs(backup_folder)

    # Copia todos os arquivos e subpastas da origem para a pasta de backup
    for item in os.listdir(origem):
        s = os.path.join(origem, item)
        d = os.path.join(backup_folder, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)
    
    print(f"Backup criado com sucesso na pasta: {backup_folder}")

if __name__ == "__main__":
    # Diretório do projeto
    diretorio_projeto = "c:/Users/halis/OneDrive/Documentos/Gerar_Escalas"
    
    # Diretório de destino do backup
    diretorio_backup = "c:/Users/halis/OneDrive/Documentos/Backups"

    criar_backup(diretorio_projeto, diretorio_backup)
