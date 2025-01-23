# restore_backup.py
import os
import shutil

def restaurar_backup(origem, destino):
    # Confirma se o diretório de origem existe
    if not os.path.exists(origem):
        print(f"O diretório de backup {origem} não existe.")
        return

    # Apaga o conteúdo atual do diretório de destino
    if os.path.exists(destino):
        for item in os.listdir(destino):
            s = os.path.join(destino, item)
            if os.path.isdir(s):
                shutil.rmtree(s)
            else:
                os.remove(s)

    # Copia o conteúdo do backup para o diretório de destino
    for item in os.listdir(origem):
        s = os.path.join(origem, item)
        d = os.path.join(destino, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)
    
    print(f"Restaurado com sucesso a partir do backup: {origem}")

if __name__ == "__main__":
    # Diretório de backup a ser restaurado
    diretorio_backup = "c:/Users/halis/OneDrive/Documentos/Backups/backup_YYYYMMDD_HHMMSS"  # Substitua pelo backup específico que deseja restaurar
    
    # Diretório do projeto
    diretorio_projeto = "c:/Users/halis/OneDrive/Documentos/Gerar_Escalas"

    restaurar_backup(diretorio_backup, diretorio_projeto)
