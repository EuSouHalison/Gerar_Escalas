# data_manager.py
import json
import os

def carregar_dados():
    # Verifica se o arquivo existe
    if os.path.exists('dados.json'):
        with open('dados.json', 'r', encoding='utf-8') as file:
            dados = json.load(file)
            turmas = dados.get('turmas', [])
            alunos_por_turma = dados.get('alunos_por_turma', {})
            return turmas, alunos_por_turma
    else:
        return [], {}

def salvar_dados(turmas, alunos_por_turma):
    dados = {
        'turmas': turmas,
        'alunos_por_turma': alunos_por_turma
    }
    with open('dados.json', 'w', encoding='utf-8') as file:
        json.dump(dados, file, ensure_ascii=False, indent=4)
