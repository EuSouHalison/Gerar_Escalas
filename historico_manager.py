import json
import os

def carregar_historico():
    if os.path.exists('historico_escalas.json'):
        with open('historico_escalas.json', 'r', encoding='utf-8') as file:
            historico = json.load(file)
            return historico
    else:
        return {}

def salvar_historico(historico):
    with open('historico_escalas.json', 'w', encoding='utf-8') as file:
        json.dump(historico, file, ensure_ascii=False, indent=4)
